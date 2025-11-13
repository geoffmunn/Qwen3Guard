# train_star_trek_guard.py
import os
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, TaskType

# ===== CONFIG =====
# Use the smaller 0.6B model for full precision to manage memory
MODEL_NAME = "Qwen/Qwen3-0.6B"
DATASET_PATH = "star_trek_guard_dataset.jsonl"  # Updated to match your file
OUTPUT_DIR = "./star_trek_guard_finetuned"
NUM_LABELS = 2
LABEL2ID = {"not_related": 0, "related": 1}
ID2LABEL = {0: "not_related", 1: "related"}
BATCH_SIZE = 2  # Reduce batch size for full precision
GRADIENT_ACCUMULATION = 16  # Increase gradient accumulation to maintain effective batch size
EPOCHS = 3
LEARNING_RATE = 2e-4
MAX_LENGTH = 512

# ===== LOAD DATASET =====
dataset = load_dataset("json", data_files=DATASET_PATH)["train"]
print("📊 Dataset info:")
print(f"Total samples: {len(dataset)}")
print(f"Sample structure: {dataset[0] if len(dataset) > 0 else 'Empty'}")
print(f"Available columns: {dataset.column_names}")

# Auto-detect label column
possible_label_cols = ["label", "class", "category", "is_related"]
label_col = None
for col in possible_label_cols:
    if col in dataset.column_names:
        label_col = col
        break

if label_col is None:
    raise ValueError(f"❌ Could not find label column. Available: {dataset.column_names}")

dataset = dataset.map(lambda x: {"labels": LABEL2ID[x[label_col]]})
print(f"✅ Using '{label_col}' as label column → mapped to 'labels'")
print(f"Label distribution: {dataset['labels'][:10]}...")

# Split dataset
dataset = dataset.train_test_split(test_size=0.1)
print(f"Train: {len(dataset['train'])}, Test: {len(dataset['test'])}")

# ===== LOAD TOKENIZER & MODEL =====
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Explicitly set BOS/EOS/PAD for Qwen
tokenizer.bos_token = tokenizer.eos_token
tokenizer.bos_token_id = tokenizer.eos_token_id
tokenizer.pad_token_id = tokenizer.eos_token_id

# Load the model in full precision (no 4-bit quantization)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS,
    id2label=ID2LABEL,
    label2id=LABEL2ID,
    trust_remote_code=True,
    torch_dtype=torch.float16, # Use float16 for efficiency while keeping full precision
    device_map="auto" # Use device_map for multi-GPU if available
)

# Align config
model.config.pad_token_id = tokenizer.pad_token_id
model.config.bos_token_id = tokenizer.bos_token_id
model.config.eos_token_id = tokenizer.eos_token_id

# ===== LoRA CONFIG =====
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.SEQ_CLS,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ===== TOKENIZE =====
def tokenize_function(examples):
    return tokenizer(
        examples["input"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
    )

# CRITICAL: Remove BOTH 'input' AND 'label' columns to avoid tensor conversion errors
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["input", "label"],  # ✅ Remove both original columns to prevent tensor error
)
print("🔍 Columns after tokenization:", tokenized_dataset["train"].column_names)

# Verify that only numeric columns remain
assert "labels" in tokenized_dataset["train"].column_names, "💥 'labels' column missing after tokenization!"
assert "label" not in tokenized_dataset["train"].column_names, "💥 Original 'label' column still present! Must be removed."

# ===== TRAINING ARGS =====
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE * 2,
    gradient_accumulation_steps=GRADIENT_ACCUMULATION,
    learning_rate=LEARNING_RATE,
    logging_steps=10,
    save_strategy="epoch",
    eval_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    report_to="none",
    
    # Use fp16 for training to save memory while keeping model precision
    fp16=True,
    
    optim="paged_adamw_32bit",
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    save_total_limit=2,
    remove_unused_columns=False,  # Keep 'labels' column
    dataloader_pin_memory=False,  # Avoid pin_memory warning
    log_level="info",
    logging_first_step=True,
    ddp_find_unused_parameters=False,  # For multi-GPU compatibility
)

# ===== TRAINER =====
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    processing_class=tokenizer,  # ✅ Use 'processing_class' instead of deprecated 'tokenizer'
)

# ===== TRAIN =====
print("🚀 Starting fine-tuning...")
trainer.train()

# ===== SAVE =====
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"✅ Model saved to {OUTPUT_DIR}")

# ===== OPTIONAL: Test the fine-tuned model =====
print("\n🧪 Testing the fine-tuned model...")
test_inputs = [
    "What is the Prime Directive in Star Trek?",
    "What is the capital of France?",
    "How does a warp drive work?",
    "What is 2 + 2?",
]

model.eval()
with torch.no_grad():
    for text in test_inputs:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=MAX_LENGTH
        )
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

        outputs = model(**inputs)
        logits = outputs.logits

        print(f"Raw logits: {logits}")  # Debug

        # Handle nan manually
        if torch.isnan(logits).any():
            print(f"⚠️ NaN detected in logits for input: {text}")
            predicted_class_id = 0
            confidence = 0.0
        else:
            probs = torch.nn.functional.softmax(logits, dim=-1)
            predicted_class_id = probs.argmax().item()
            confidence = probs.max().item()

        predicted_label = ID2LABEL[predicted_class_id]

        print(f"Input: {text}")
        print(f"Prediction: {predicted_label} (confidence: {confidence:.3f})")
        print("---")
