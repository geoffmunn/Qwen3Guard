import torch
from transformers import AutoModel, AutoTokenizer
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for model and tokenizer
model = None
tokenizer = None

def load_model():
    """Load the Qwen3Guard-Stream model and tokenizer"""
    global model, tokenizer
    if model is None or tokenizer is None:
        print("Loading Qwen3Guard-Stream model...")
        model_path = "Qwen/Qwen3Guard-Stream-0.6B"
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        model = AutoModel.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        ).eval()
        print("Model loaded successfully!")

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with streaming moderation"""
    try:
        data = request.json
        messages = data.get('messages', [])
        stream = data.get('stream', True)
        
        if not messages:
            return jsonify({'error': 'No messages provided'}), 400
        
        # Get user and assistant messages (if provided)
        user_message = None
        assistant_message = None
        
        for msg in messages:
            if msg.get('role') == 'user' and user_message is None:
                user_message = msg.get('content')
            elif msg.get('role') == 'assistant' and assistant_message is None:
                assistant_message = msg.get('content')
        
        if not user_message:
            return jsonify({'error': 'No user message found'}), 400
        
        # Prepare messages for moderation (same format as original script)
        if assistant_message:
            moderation_messages = [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_message}
            ]
        else:
            moderation_messages = [{"role": "user", "content": user_message}]
        
        # Apply chat template
        text = tokenizer.apply_chat_template(
            moderation_messages, 
            tokenize=False, 
            add_generation_prompt=False, 
            enable_thinking=False
        )
        model_inputs = tokenizer(text, return_tensors="pt")
        token_ids = model_inputs.input_ids[0]
        
        # Find user message end
        token_ids_list = token_ids.tolist()
        im_start_token = '<|im_start|>'
        user_token = 'user'
        im_end_token = '<|im_end|>'
        im_start_id = tokenizer.convert_tokens_to_ids(im_start_token)
        user_id = tokenizer.convert_tokens_to_ids(user_token)
        im_end_id = tokenizer.convert_tokens_to_ids(im_end_token)
        
        # Find the end of the user message
        try:
            last_start = next(i for i in range(len(token_ids_list)-1, -1, -1) 
                            if token_ids_list[i:i+2] == [im_start_id, user_id])
            user_end_index = next(i for i in range(last_start+2, len(token_ids_list)) 
                                if token_ids_list[i] == im_end_id)
        except StopIteration:
            return jsonify({'error': 'Failed to parse user message'}), 400
        
        if stream:
            return Response(
                stream_moderation(user_message, assistant_message, token_ids, user_end_index),
                mimetype='application/json',
                headers={'Content-Type': 'application/json'}
            )
        else:
            # Non-streaming response
            result = moderate_user_message(token_ids, user_end_index)
            response_text = f"User message moderation: Risk Level: {result['risk_level'][-1]}"
            if result['risk_level'][-1] != "Safe":
                category = result.get('category', ['N/A'])[-1] if 'category' in result else 'N/A'
                response_text += f", Category: {category}"
            
            if assistant_message:
                # Also moderate assistant message
                ass_result = moderate_assistant_message(token_ids, user_end_index)
                response_text += f"\nAssistant message moderation: Risk Level: {ass_result['risk_level'][-1]}"
                if ass_result['risk_level'][-1] != "Safe":
                    category = ass_result.get('category', ['N/A'])[-1] if 'category' in ass_result else 'N/A'
                    response_text += f", Category: {category}"
            
            return jsonify({
                'message': {
                    'role': 'assistant',
                    'content': response_text
                },
                'done': True
            })
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def moderate_user_message(token_ids, user_end_index):
    """Moderate the user message"""
    stream_state = None
    result, stream_state = model.stream_moderate_from_ids(
        token_ids[:user_end_index+1], 
        role="user", 
        stream_state=None
    )
    model.close_stream(stream_state)
    return result

def moderate_assistant_message(token_ids, user_end_index):
    """Moderate the assistant message token-by-token (as in original script)"""
    stream_state = None
    # First moderate user message to get initial stream_state
    _, stream_state = model.stream_moderate_from_ids(
        token_ids[:user_end_index+1], 
        role="user", 
        stream_state=None
    )
    
    # Then moderate assistant tokens one by one
    for i in range(user_end_index + 1, len(token_ids)):
        current_token = token_ids[i]
        result, stream_state = model.stream_moderate_from_ids(
            current_token, 
            role="assistant", 
            stream_state=stream_state
        )
    
    model.close_stream(stream_state)
    return result

def stream_moderation(user_message, assistant_message, token_ids, user_end_index):
    """Stream moderation results (matching original script behavior)"""
    try:
        # First, moderate the user message
        stream_state = None
        result, stream_state = model.stream_moderate_from_ids(
            token_ids[:user_end_index+1], 
            role="user", 
            stream_state=None
        )
        
        # Send user moderation result
        risk_level = result['risk_level'][-1]
        category = result.get('category', ['N/A'])[-1] if 'category' in result else 'N/A'
        
        if risk_level == "Safe":
            response_text = f"User moderation: -> [Risk: {risk_level}]\n"
        else:
            response_text = f"User moderation: -> [Risk: {risk_level} - Category: {category}]\n"
        
        # Stream the user moderation result
        for char in response_text:
            yield json.dumps({
                'message': {
                    'role': 'assistant',
                    'content': char
                },
                'done': False
            }) + '\n'
        
        # If assistant message is provided, moderate it token-by-token
        if assistant_message and len(token_ids) > user_end_index + 1:
            assistant_header = "Assistant streaming moderation:\n"
            for char in assistant_header:
                yield json.dumps({
                    'message': {
                        'role': 'assistant',
                        'content': char
                    },
                    'done': False
                }) + '\n'
            
            # Moderate assistant tokens one by one
            for i in range(user_end_index + 1, len(token_ids)):
                current_token = token_ids[i]
                result, stream_state = model.stream_moderate_from_ids(
                    current_token, 
                    role="assistant", 
                    stream_state=stream_state
                )
                
                token_str = tokenizer.decode([current_token])
                risk_level = result['risk_level'][-1]
                category = result.get('category', ['N/A'])[-1] if 'category' in result else 'N/A'
                
                if risk_level == "Safe":
                    token_result = f"Token: {repr(token_str)} -> [Risk: {risk_level}]\n"
                else:
                    token_result = f"Token: {repr(token_str)} -> [Risk: {risk_level} - Category: {category}]\n"
                
                # Stream the token moderation result
                for char in token_result:
                    yield json.dumps({
                        'message': {
                            'role': 'assistant',
                            'content': char
                        },
                        'done': False
                    }) + '\n'
        
        # Send final message
        yield json.dumps({
            'message': {
                'role': 'assistant',
                'content': ''
            },
            'done': True
        }) + '\n'
        
        # Clean up
        if stream_state:
            model.close_stream(stream_state)
    
    except Exception as e:
        print(f"Error in stream_moderation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        yield json.dumps({
            'message': {
                'role': 'assistant',
                'content': f'Error: {str(e)}'
            },
            'done': True
        }) + '\n'

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    print("Initializing Qwen3Guard-Stream API Server...")
    load_model()
    print("Starting server on http://localhost:5000")
    print("API endpoint: http://localhost:5000/api/chat")
    app.run(host='0.0.0.0', port=5000, debug=False)

