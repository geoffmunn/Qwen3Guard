# Qwen3Guard

This project is to demonstrate how the the Qwen3Guard models work. The 'Stream' model in particular is different becaues llama.cpp can't convert it to GGUF files.

Qwen have provided basic CLI scripts to show how it works, and I have converted them into Ollama-compatible versions, and also a webpage that uses the Stream model for moderation.

## CLI demonstrations

These are demonstrations to show how the basic interactions work. The API server examples are based on these.

### Installation

For the non-Ollama scripts, you need these dependencies:

```bash
 pip install transformers
 pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
 pip install accelerate
 ```
The Ollama versions do not need these.

## Fine tuning

## Fine-Tuning

This project includes an example of fine-tuning the Qwen3-4B model for custom classification tasks. The example demonstrates fine-tuning for Star Trek-related content classification.

### Dataset Format

The fine-tuning process uses a JSONL (JSON Lines) dataset format where each line contains:
```json
{"input": "Your text input here", "label": "related"}
```

The dataset should be placed in `finetuning/star_trek/star_trek_guard_dataset.jsonl`. The labels are binary classification: `"related"` or `"not_related"`.

### Generating a Dataset

You can generate a Star Trek dataset using the provided script:
```bash
python generate_star_trek_questions.py
```

This will create a dataset file with 2,500 Star Trek-related questions labeled as `"related"`. You can modify this script to generate datasets for your own domain.

### Training Configuration

The fine-tuning script (`finetuning/star_trek/train_star_trek_guard.py`) uses:
- **Base Model**: Qwen3-4B
- **Method**: LoRA (Low-Rank Adaptation) for efficient fine-tuning
- **Training Parameters**:
  - Batch size: 2
  - Gradient accumulation: 16 (effective batch size: 32)
  - Epochs: 3
  - Learning rate: 2e-4
  - Max sequence length: 512
- **LoRA Configuration**:
  - Rank (r): 16
  - Alpha: 32
  - Dropout: 0.05
  - Target modules: attention and MLP layers

### Running Fine-Tuning

1. Install additional dependencies:
```bash
pip install datasets peft
```

2. Navigate to the fine-tuning directory:
```bash
cd finetuning/star_trek
```

3. Ensure your dataset file (`star_trek_guard_dataset.jsonl`) is in the current directory

4. Run the training script:
```bash
python train_star_trek_guard.py
```

The fine-tuned model will be saved to `./star_trek_guard_finetuned/` directory. The script will:
- Load and tokenize the dataset
- Split into train/test sets (90/10)
- Apply LoRA fine-tuning
- Save the model and tokenizer
- Run test predictions on sample inputs

### Customizing Fine-Tuning

To fine-tune for your own use case:
1. Modify the `MODEL_NAME` variable to use a different base model
2. Update `LABEL2ID` and `ID2LABEL` dictionaries for your classification labels
3. Adjust training hyperparameters (batch size, learning rate, epochs) based on your dataset size and hardware
4. Create your own dataset in the JSONL format

## Uploading to Hugging Face

After fine-tuning, you can upload your model to Hugging Face Hub for easy sharing and deployment.

### Prerequisites

1. Install the Hugging Face Hub library:
```bash
pip install huggingface_hub
```

2. Authenticate with Hugging Face:
```bash
huggingface-cli login
```
Enter your Hugging Face token when prompted. You can get a token from https://huggingface.co/settings/tokens

### Upload Process

1. Navigate to the fine-tuning directory:
```bash
cd finetuning/star_trek
```

2. Edit `huggingface_upload.py` to set your repository ID:
```python
repo_id = f"your-username/your-model-name"
```

3. Ensure the model directory path matches your training output directory (default: `./star_trek_guard_finetuned`)

4. Run the upload script:
```bash
python huggingface_upload.py
```

The script will:
- Create a new repository on Hugging Face (or use existing if `exist_ok=True`)
- Upload all model files, tokenizer files, and configuration files
- Make the model publicly available (or private if `private=True`)

After upload, your model will be available at `https://huggingface.co/your-username/your-model-name` and can be loaded using:
```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained("your-username/your-model-name")
tokenizer = AutoTokenizer.from_pretrained("your-username/your-model-name")
```

## API Server

### Stream model
The `qwen-stream-api_server.py` provides a complete backend API for the Qwen3Guard-Stream model that can be used with the `qwen_stream_chat.html` interface.

### Classification model
The Star Trek classification examples show how to use the fine-tuned Star Trek example. This is NOT a stream model so it doesn't use the same interface as the standard `qwen-steam-api_server.py` example.

You can connect to it via the `star_trek_chat.html` interface and the `star_trek_api_server.py` server.

### Setup

1. Install the required dependencies:
2. 
```bash
pip install flask
pip install flask_cors
pip install accelerate
```

2. Start the API server:
```bash
python qwen_stream_api_server.py
```
Or use the Star Trek version if required.

The server will start on `http://localhost:5000` by default.

### Usage

1. Open `qwen_stream_chat.html` in a web browser (you may need to serve it from a local web server to avoid CORS issues):
```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000/qwen_stream_chat.html`

2. The HTML interface will automatically connect to the API server at `http://localhost:5000/api/chat`

### API Endpoints

- `POST /api/moderate` - Main chat endpoint that moderates user messages (and optionally assistant messages)
  - Accepts: `{"messages": [{"role": "user", "content": "..."}], "stream": true}`
  - Returns: Streaming JSON responses with moderation results

- `GET /health` - Health check endpoint
  - Returns: `{"status": "healthy", "model_loaded": true/false}`


