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

# ===== CONFIGURATION =====
MODEL_NAME = "Qwen/Qwen3-0.6B"  # or "Qwen/Qwen3-0.6B" for lower VRAM
DATASET_PATH = "star_trek_guard_dataset.jsonl"
OUTPUT_DIR = "./star_trek_guard_finetuned"
NUM_LABELS = 2
LABEL2ID = {"not_related": 0, "related": 1}
ID2LABEL = {0: "not_related", 1: "related"}
BATCH_SIZE = 1           # Reduce if OOM
GRADIENT_ACCUMULATION = 8
EPOCHS = 3
LEARNING_RATE = 2e-4
MAX_LENGTH = 256         # Lower = less memory
WARMUP_RATIO = 0.1

# ===== LOAD DATASET =====
print("📥 Loading dataset...")
dataset = load_dataset("json", data_files=DATASET_PATH)["train"]
dataset = dataset.map(lambda x: {"labels": LABEL2ID[x["label"]]}, batched=False)
dataset = dataset.train_test_split(test_size=0.1, seed=42)

print(f"✅ Loaded {len(dataset['train'])} training and {len(dataset['test'])} validation examples.")

# ===== LOAD TOKENIZER & MODEL =====
print("🔧 Loading tokenizer and model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token  # Qwen uses eos_token as pad

# Quantization config for 4-bit (saves ~75% VRAM)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS,
    id2label=ID2LABEL,
    label2id=LABEL2ID,
    trust_remote_code=True,
    torch_dtype=torch.float16,
    quantization_config=bnb_config,
    device_map="auto",  # Automatically uses GPU if available
)

# Fix padding token
model.config.pad_token_id = tokenizer.pad_token_id
# The warning about score.weight is expected for a new classification head.
# The warning about cache config is also expected if the model config doesn't have it.
# We do not need to set use_cache=False here as it's not a TrainingArguments parameter.

# ===== LoRA CONFIGURATION =====
print("⚡ Applying LoRA fine-tuning...")
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

# ===== TOKENIZE DATASET =====
def tokenize_function(examples):
    return tokenizer(
        examples["input"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
    )

print("🧮 Tokenizing dataset...")
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["input", "label"]
)

# ===== TRAINING ARGUMENTS =====
print("⚙️ Setting training arguments...")
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE * 2,
    gradient_accumulation_steps=GRADIENT_ACCUMULATION,
    learning_rate=LEARNING_RATE,
    warmup_ratio=WARMUP_RATIO,
    logging_steps=10,
    save_strategy="epoch",
    eval_strategy="epoch",  # ✅ Now supported in modern transformers
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    report_to="none",  # Disable wandb/MLflow
    fp16=True,
    optim="paged_adamw_32bit",
    lr_scheduler_type="cosine",
    save_total_limit=2,
    dataloader_pin_memory=False,  # ✅ Prevents memory leak on CPU
    # gradient_checkpointing=True,  # <- Keep commented out initially if facing errors
)

# ===== TRAINER =====
print("🚀 Initializing trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,  # Still valid in most versions
    # processing_class=tokenizer,  # Also include for forward compatibility if Trainer accepts it
)

# ===== TRAIN =====
print("🔥 Starting training...")
trainer.train()

# ===== SAVE FINAL MODEL =====
print("💾 Saving fine-tuned model...")
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"\n🎉 SUCCESS! Model saved to: {OUTPUT_DIR}")
print("✅ Next steps:")
print("   1. Test with: python test_model.py")
print("   2. Deploy with: Hugging Face Inference API or FastAPI")
