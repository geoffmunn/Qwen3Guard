# Qwen3Guard

This project is to demonstrate how the the Qwen3Guard models work. The 'Stream' model in particular is different becaues llama.cpp can't convert it to GGUF files.

Qwen have provided basic CLI scripts to show how it works, and I have converted them into Ollama-compatible versions, and also a webpage that uses the Stream model for moderation.

## Installation

For the non-Ollama scripts, you need these dependencies:

```bash
 pip install transformers
 pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
 pip install accelerate
 ```
The Ollama versions do not need these.

## API Server

The `api_server.py` provides a complete backend API for the Qwen3Guard-Stream model that can be used with the `chat_demo.html` interface.

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
python api_server.py
```

The server will start on `http://localhost:5000` by default.

### Usage

1. Open `chat_demo.html` in a web browser (you may need to serve it from a local web server to avoid CORS issues):
```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000/chat_demo.html`

2. The HTML interface will automatically connect to the API server at `http://localhost:5000/api/chat`

### API Endpoints

- `POST /api/moderate` - Main chat endpoint that moderates user messages (and optionally assistant messages)
  - Accepts: `{"messages": [{"role": "user", "content": "..."}], "stream": true}`
  - Returns: Streaming JSON responses with moderation results

- `GET /health` - Health check endpoint
  - Returns: `{"status": "healthy", "model_loaded": true/false}`
