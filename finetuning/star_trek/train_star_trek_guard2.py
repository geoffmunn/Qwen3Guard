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
import bitsandbytes as bnb

# ===== CONFIG =====
MODEL_NAME = "Qwen/Qwen3-4B"  # or "Qwen/Qwen3-0.6B" for lower VRAM
DATASET_PATH = "star_trek_guard_dataset.jsonl"
OUTPUT_DIR = "./star_trek_guard_finetuned"
NUM_LABELS = 2
LABEL2ID = {"not_related": 0, "related": 1}
ID2LABEL = {0: "not_related", 1: "related"}
BATCH_SIZE = 4  # reduce to 2 if OOM
GRADIENT_ACCUMULATION = 8
EPOCHS = 3
LEARNING_RATE = 2e-4
MAX_LENGTH = 512

# ===== LOAD DATASET =====
dataset = load_dataset("json", data_files=DATASET_PATH)["train"]
dataset = dataset.map(lambda x: {"labels": LABEL2ID[x["label"]]})
dataset = dataset.train_test_split(test_size=0.1)

# ===== LOAD TOKENIZER & MODEL =====
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

# Quantization (optional: helps on 8–12GB GPU)
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS,
    id2label=ID2LABEL,
    label2id=LABEL2ID,
    trust_remote_code=True,
    torch_dtype=torch.float16,
    quantization_config=quantization_config,
)

# Fix for Qwen padding
model.config.pad_token_id = tokenizer.pad_token_id

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

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["input", "label"]
)

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
    evaluation_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    report_to="none",
    fp16=True,
    optim="paged_adamw_32bit",
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    save_total_limit=2,
)

# ===== TRAINER =====
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
)

# ===== TRAIN =====
print("🚀 Starting fine-tuning...")
trainer.train()

# ===== SAVE =====
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"✅ Model saved to {OUTPUT_DIR}")