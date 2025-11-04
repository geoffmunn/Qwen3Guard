import requests
import json

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate" # Or /api/chat for message format
MODEL_NAME = "Qwen3-4B-SafeRL-f16:Q5_K_M" # The name you gave it in Ollama

# Prepare the prompt (similar to the original script)
prompt = "Give me a short introduction to large language model."

# --- Option 1: Using /api/generate ---
# This endpoint takes a single string prompt.

payload_generate = {
    "model": MODEL_NAME,
    "prompt": prompt, # Ollama handles basic templating if no custom template is set
    "stream": False, # Set to True if you want streaming responses
    "options": {
        # Note: Ollama parameters might differ slightly from transformers
        # max_new_tokens is not directly available, use num_predict instead
        "num_predict": 32768, # Equivalent to max_new_tokens in transformers
        "temperature": 0.7,   # Example, adjust as needed
    }
}

try:
    response = requests.post(OLLAMA_API_URL, json=payload_generate)
    response.raise_for_status() # Raise an error for bad status codes

    result = response.json()
    generated_text = result['response'] # The generated text from Ollama

    print("Generated content:", generated_text)

    # Note: Ollama does NOT automatically parse specific tokens like </think>
    # If the model outputs <think>...</think> blocks, you'll need to parse them manually
    # from the 'generated_text' string using standard Python string methods.
    # This is different from the original script which used tokenizer.decode
    # and relied on specific token IDs (151668).

except requests.exceptions.RequestException as e:
    print(f"Error calling Ollama API: {e}")
except KeyError as e:
    print(f"Error parsing Ollama response: {e}")
    print(f"Full response: {response.text}")


# --- Option 2: Using /api/chat (often preferred for chat models) ---
# This endpoint takes a list of message dictionaries.

# OLLAMA_CHAT_API_URL = "http://localhost:11434/api/chat"

# messages = [
#     {"role": "user", "content": prompt}
# ]

# payload_chat = {
#     "model": MODEL_NAME,
#     "messages": messages,
#     "stream": False, # Set to True for streaming
#     "options": {
#         "num_predict": 32768, # Equivalent to max_new_tokens
#         "temperature": 0.7,
#     }
# }

# try:
#    response_chat = requests.post(OLLAMA_CHAT_API_URL, json=payload_chat)
#     response_chat.raise_for_status()

#     result_chat = response_chat.json()
#     generated_text_chat = result_chat['message']['content'] # Extract content from the message object

#     print("\nGenerated content (via /api/chat):", generated_text_chat)

#     # Parsing <think> blocks (if present) still needs to be done manually here as well.

except requests.exceptions.RequestException as e:
    print(f"Error calling Ollama Chat API: {e}")
except KeyError as e:
    print(f"Error parsing Ollama Chat response: {e}")
    print(f"Full response: {response_chat.text}")
