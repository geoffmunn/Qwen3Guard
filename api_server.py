import torch
from transformers import AutoModel, AutoTokenizer
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import sys

# ============================================================================
# CONFIGURATION - Model Selection
# ============================================================================
# Change this variable to switch between different model sizes:
#   - "0.6B" for Qwen/Qwen3Guard-Stream-0.6B (smallest, fastest)
#   - "4B"   for Qwen/Qwen3Guard-Stream-4B (balanced)
#   - "8B"   for Qwen/Qwen3Guard-Stream-8B (largest, most accurate)
MODEL_SIZE = "0.6B"

# Model path mapping
MODEL_PATHS = {
    "0.6B": "Qwen/Qwen3Guard-Stream-0.6B",
    "4B": "Qwen/Qwen3Guard-Stream-4B",
    "8B": "Qwen/Qwen3Guard-Stream-8B"
}

# Get the model path based on configuration
MODEL_PATH = MODEL_PATHS.get(MODEL_SIZE, MODEL_PATHS["0.6B"])

# ============================================================================

app = Flask(__name__)
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

# Global variables for model and tokenizer
model = None
tokenizer = None

def load_model():
    """Load the Qwen3Guard-Stream model and tokenizer based on configuration"""
    global model, tokenizer
    if model is None or tokenizer is None:
        print(f"Loading {MODEL_PATH} model...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
        model = AutoModel.from_pretrained(
            MODEL_PATH,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        ).eval()
        print(f"Model {MODEL_PATH} loaded successfully!")

def find_user_message_end(token_ids, tokenizer):
    """Find the end index of the user message in tokenized input"""
    token_ids_list = token_ids.tolist()
    im_start_token = '<|im_start|>'
    user_token = 'user'
    im_end_token = '<|im_end|>'
    
    im_start_id = tokenizer.convert_tokens_to_ids(im_start_token)
    user_id = tokenizer.convert_tokens_to_ids(user_token)
    im_end_id = tokenizer.convert_tokens_to_ids(im_end_token)
    
    # Find the last occurrence of <|im_start|>user
    last_start = next(
        i for i in range(len(token_ids_list)-1, -1, -1) 
        if token_ids_list[i:i+2] == [im_start_id, user_id]
    )
    
    # Find the corresponding <|im_end|>
    user_end_index = next(
        i for i in range(last_start+2, len(token_ids_list)) 
        if token_ids_list[i] == im_end_id
    )
    
    return user_end_index

@app.route('/api/moderate', methods=['POST', 'OPTIONS'])
def moderate():
    """Moderate a single user message"""
    if request.method == 'OPTIONS':
        return Response(status=200)
    
    try:
        data = request.json or {}
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'risk_level': 'Safe',
                'category': None,
                'message': ''
            }), 200
        
        # Prepare messages for moderation
        moderation_messages = [{"role": "user", "content": message}]
        
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
        try:
            user_end_index = find_user_message_end(token_ids, tokenizer)
        except StopIteration:
            return jsonify({'error': 'Failed to parse user message'}), 400
        
        # Moderate the user message
        stream_state = None
        result, stream_state = model.stream_moderate_from_ids(
            token_ids[:user_end_index+1],
            role="user",
            stream_state=None
        )
        model.close_stream(stream_state)
        
        risk_level = result['risk_level'][-1]
        category = result.get('category', [None])[-1] if 'category' in result and result['category'] else None
        
        return jsonify({
            'risk_level': risk_level,
            'category': category,
            'message': message
        })
    
    except Exception as e:
        print(f"Error in moderate endpoint: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/moderate_conversation', methods=['POST', 'OPTIONS'])
def moderate_conversation():
    """Moderate a full conversation (user + assistant messages)"""
    if request.method == 'OPTIONS':
        return Response(status=200)
    
    try:
        data = request.json or {}
        messages = data.get('messages', [])
        stream = data.get('stream', False)
        
        if not messages:
            return jsonify({'error': 'No messages provided'}), 400
        
        # Extract user and assistant messages
        user_message = None
        assistant_message = None
        
        for msg in messages:
            if msg.get('role') == 'user' and user_message is None:
                user_message = msg.get('content', '')
            elif msg.get('role') == 'assistant' and assistant_message is None:
                assistant_message = msg.get('content', '')
        
        if not user_message:
            return jsonify({'error': 'No user message found'}), 400
        
        # Prepare messages for moderation
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
        try:
            user_end_index = find_user_message_end(token_ids, tokenizer)
        except StopIteration:
            return jsonify({'error': 'Failed to parse user message'}), 400
        
        if stream:
            return Response(
                stream_moderation_results(token_ids, user_end_index, assistant_message is not None),
                mimetype='application/json',
                headers={'Content-Type': 'application/json'}
            )
        else:
            return moderate_conversation_non_streaming(token_ids, user_end_index, assistant_message is not None)
    
    except Exception as e:
        print(f"Error in moderate_conversation endpoint: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def moderate_conversation_non_streaming(token_ids, user_end_index, has_assistant_message):
    """Non-streaming moderation of conversation"""
    results = {}
    
    # 1. Moderate user message
    stream_state = None
    user_result, stream_state = model.stream_moderate_from_ids(
        token_ids[:user_end_index+1],
        role="user",
        stream_state=None
    )
    
    user_risk = user_result['risk_level'][-1]
    user_category = user_result.get('category', [None])[-1] if 'category' in user_result and user_result['category'] else None
    
    results['user'] = {
        'risk_level': user_risk,
        'category': user_category
    }
    
    # 2. If assistant message exists, moderate it token-by-token
    if has_assistant_message and len(token_ids) > user_end_index + 1:
        assistant_results = []
        
        for i in range(user_end_index + 1, len(token_ids)):
            current_token = token_ids[i]
            result, stream_state = model.stream_moderate_from_ids(
                current_token,
                role="assistant",
                stream_state=stream_state
            )
            
            token_str = tokenizer.decode([current_token])
            risk_level = result['risk_level'][-1]
            category = result.get('category', [None])[-1] if 'category' in result and result['category'] else None
            
            assistant_results.append({
                'token': token_str,
                'risk_level': risk_level,
                'category': category
            })
        
        # Get the overall risk level from the last token
        if assistant_results:
            results['assistant'] = {
                'risk_level': assistant_results[-1]['risk_level'],
                'category': assistant_results[-1]['category'],
                'tokens': assistant_results
            }
        else:
            results['assistant'] = {
                'risk_level': 'Safe',
                'category': None,
                'tokens': []
            }
        
        model.close_stream(stream_state)
    else:
        model.close_stream(stream_state)
    
    return jsonify(results)

def stream_moderation_results(token_ids, user_end_index, has_assistant_message):
    """Stream moderation results matching chat_Stream_8B.py logic"""
    try:
        stream_state = None
        
        # 1. Moderate user message
        result, stream_state = model.stream_moderate_from_ids(
            token_ids[:user_end_index+1],
            role="user",
            stream_state=None
        )
        
        risk_level = result['risk_level'][-1]
        category = result.get('category', [None])[-1] if 'category' in result and result['category'] else None
        
        if risk_level == "Safe":
            user_output = f"User moderation: -> [Risk: {risk_level}]\n"
        else:
            user_output = f"User moderation: -> [Risk: {risk_level} - Category: {category}]\n"
        
        # Stream user moderation result
        for char in user_output:
            yield json.dumps({
                'type': 'user_moderation',
                'content': char,
                'risk_level': risk_level,
                'category': category,
                'done': False
            }) + '\n'
        
        # 2. Moderate assistant message token-by-token if it exists
        if has_assistant_message and len(token_ids) > user_end_index + 1:
            assistant_header = "Assistant streaming moderation:\n"
            for char in assistant_header:
                yield json.dumps({
                    'type': 'assistant_header',
                    'content': char,
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
                category = result.get('category', [None])[-1] if 'category' in result and result['category'] else None
                
                if risk_level == "Safe":
                    token_output = f"Token: {repr(token_str)} -> [Risk: {risk_level}]\n"
                else:
                    token_output = f"Token: {repr(token_str)} -> [Risk: {risk_level} - Category: {category}]\n"
                
                # Stream token moderation result
                for char in token_output:
                    yield json.dumps({
                        'type': 'token_moderation',
                        'content': char,
                        'token': token_str,
                        'risk_level': risk_level,
                        'category': category,
                        'done': False
                    }) + '\n'
        
        # Clean up
        if stream_state:
            model.close_stream(stream_state)
        
        # Send final message
        yield json.dumps({
            'type': 'done',
            'content': '',
            'done': True
        }) + '\n'
    
    except Exception as e:
        print(f"Error in stream_moderation_results: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        yield json.dumps({
            'type': 'error',
            'content': f'Error: {str(e)}',
            'done': True
        }) + '\n'

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'model_name': MODEL_PATH if model is not None else None,
        'model_size': MODEL_SIZE
    })

@app.route('/', methods=['GET'])
def index():
    """API information endpoint"""
    return jsonify({
        'name': 'Qwen3Guard-Stream API Server',
        'version': '1.0',
        'endpoints': {
            '/api/moderate': 'POST - Moderate a single user message',
            '/api/moderate_conversation': 'POST - Moderate a conversation (user + assistant)',
            '/health': 'GET - Health check'
        },
        'model': MODEL_PATH,
        'model_size': MODEL_SIZE
    })

if __name__ == '__main__':
    print(f"Initializing Qwen3Guard-Stream API Server (Model: {MODEL_PATH})...")
    load_model()
    print("Starting server on http://localhost:5000")
    print("API endpoints:")
    print("  - POST /api/moderate - Moderate a single message")
    print("  - POST /api/moderate_conversation - Moderate a conversation")
    print("  - GET /health - Health check")
    app.run(host='0.0.0.0', port=5000, debug=False)

