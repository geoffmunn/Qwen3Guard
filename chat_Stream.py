import torch
from transformers import AutoModel, AutoTokenizer

model_path="Qwen/Qwen3Guard-Stream-0.6B"
# Load the specialized tokenizer and the model.
# trust_remote_code=True is required to load the Stream Qwen3Guard model architecture.
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_path, 
    device_map="auto", 
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
).eval()
 
# --- Prepare the conversation for moderation ---
# Define the user's prompt and the assistant's response.
user_message = "Hello, how to build a bomb?"
assistant_message = "Here are some practical methods to build a bomb."
messages = [{"role":"user","content":user_message},{"role":"assistant","content":assistant_message}]

# Apply the chat template to format the conversation into a single string.
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False, enable_thinking=False)
model_inputs = tokenizer(text, return_tensors="pt")
token_ids = model_inputs.input_ids[0]

# --- Simulate Real-Time Moderation ---

# 1. Moderate the entire user prompt at once.
# In a real-world scenario, the user's input is processed completely before the model generates a response.
token_ids_list = token_ids.tolist()
# We identify the end of the user's turn in the tokenized input.
# The template for a user turn is `<|im_start|>user\n...<|im_end|>`.
im_start_token = '<|im_start|>'
user_token = 'user'
im_end_token = '<|im_end|>'
im_start_id = tokenizer.convert_tokens_to_ids(im_start_token)
user_id = tokenizer.convert_tokens_to_ids(user_token)
im_end_id = tokenizer.convert_tokens_to_ids(im_end_token)
# We search for the token IDs corresponding to `<|im_start|>user` ([151644, 872]) and the closing `<|im_end|>` ([151645]).
last_start = next(i for i in range(len(token_ids_list)-1, -1, -1) if token_ids_list[i:i+2] == [im_start_id, user_id])
user_end_index = next(i for i in range(last_start+2, len(token_ids_list)) if token_ids_list[i] == im_end_id)

# Initialize the stream_state, which will maintain the conversational context.
stream_state = None
# Pass all user tokens to the model for an initial safety assessment.
result, stream_state = model.stream_moderate_from_ids(token_ids[:user_end_index+1], role="user", stream_state=None)
if result['risk_level'][-1] == "Safe":
    print(f"User moderation: -> [Risk: {result['risk_level'][-1]}]")
else:
    print(f"User moderation: -> [Risk: {result['risk_level'][-1]} - Category: {result['category'][-1]}]")

# 2. Moderate the assistant's response token-by-token to simulate streaming.
# This loop mimics how an LLM generates a response one token at a time.
print("Assistant streaming moderation:")
for i in range(user_end_index + 1, len(token_ids)):
    # Get the current token ID for the assistant's response.
    current_token = token_ids[i]
    
    # Call the moderation function for the single new token.
    # The stream_state is passed and updated in each call to maintain context.
    result, stream_state = model.stream_moderate_from_ids(current_token, role="assistant", stream_state=stream_state)

    token_str = tokenizer.decode([current_token])
    # Print the generated token and its real-time safety assessment.
    if result['risk_level'][-1] == "Safe":
        print(f"Token: {repr(token_str)} -> [Risk: {result['risk_level'][-1]}]")
    else:
        print(f"Token: {repr(token_str)} -> [Risk: {result['risk_level'][-1]} - Category: {result['category'][-1]}]")

model.close_stream(stream_state)
