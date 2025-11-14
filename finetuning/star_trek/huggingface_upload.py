from huggingface_hub import HfApi
from transformers import AutoTokenizer
import os

# Ensure your training script has finished and saved the model to OUTPUT_DIR
model_directory = "./star_trek_guard_finetuned" # Use your OUTPUT_DIR variable

api = HfApi()

# Upload the model directory
repo_id = f"geoffmunn/Qwen3guard-StarTrek-stream-0.6B" # Replace with your username and desired repo name
api.upload_folder(
    folder_path=model_directory,
    repo_id=repo_id,
    repo_type="model",
    commit_message="Upload fine-tuned Qwen3-0.6B Star Trek Guard model",
)

print(f"Model uploaded successfully to https://huggingface.co/{repo_id}")
