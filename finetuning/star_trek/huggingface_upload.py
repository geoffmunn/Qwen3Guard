from huggingface_hub import HfApi
from transformers import AutoTokenizer
import os

# Ensure your training script has finished and saved the model to OUTPUT_DIR
model_directory = "./star_trek_guard_finetuned" # Use your OUTPUT_DIR variable

api = HfApi()

# Create the repository first
repo_id = f"geoffmunn/Qwen3Guard-StarTrek-Classification-4B" # Replace with your username and desired repo name

api.create_repo(
    repo_id=repo_id,
    repo_type="model",
    private=False, # Set to True if you want a private repo
    exist_ok=True, # This prevents an error if the repo already exists
)

# Now upload the model directory
api.upload_folder(
    folder_path=model_directory,
    repo_id=repo_id,
    repo_type="model",
    commit_message="Upload fine-tuned Qwen3-4B Star Trek Guard model",
)

print(f"Model uploaded successfully to https://huggingface.co/{repo_id}")