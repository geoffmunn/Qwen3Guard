import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================
MODEL_PATH = "geoffmunn/Qwen3Guard-StarTrek-stream-0.6B"
MAX_LENGTH = 512
ID2LABEL = {0: "not_related", 1: "related"}

# ============================================================================

app = Flask(__name__)
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

# Global variables for model and tokenizer
model = None
tokenizer = None

def load_model():
    """Load the Qwen3Guard-StarTrek model and tokenizer"""
    global model, tokenizer
    if model is None or tokenizer is None:
        print(f"Loading {MODEL_PATH} model...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Determine appropriate dtype based on device support
        # Use float16 for GPU, float32 for CPU (more compatible than bfloat16)
        if torch.cuda.is_available():
            dtype = torch.float16
            print("Using float16 precision (GPU)")
        else:
            dtype = torch.float32
            print("Using float32 precision (CPU)")
        
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_PATH,
            device_map="auto",
            dtype=dtype,
            trust_remote_code=True,
        ).eval()
        print(f"Model {MODEL_PATH} loaded successfully!")
        
        # Check model config for label mappings
        if hasattr(model.config, 'id2label'):
            print(f"Model labels: {model.config.id2label}")

@app.route('/api/moderate', methods=['POST', 'OPTIONS'])
def moderate():
    """Moderate a single user message using Qwen3Guard-StarTrek model"""
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.json or {}
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'risk_level': 'Safe',
                'category': None,
                'message': '',
                'predicted_label': 'not_related',
                'confidence': 0.0
            }), 200
        
        # Tokenize the input text
        inputs = tokenizer(
            message,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=MAX_LENGTH
        )
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Get model prediction
        model.eval()
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            
            # DEBUG: Print raw model outputs
            print(f"\n{'='*60}")
            print(f"DEBUG: Moderation Request")
            print(f"{'='*60}")
            print(f"Input message: {repr(message)}")
            print(f"Raw logits: {logits}")
            print(f"Logits values: {logits.cpu().numpy().flatten()}")
            
            # Handle NaN manually (as shown in training code)
            if torch.isnan(logits).any():
                print(f"⚠️ NaN detected in logits for input: {message}")
                predicted_class_id = 0
                confidence = 0.0
                probs = None
            else:
                probs = torch.nn.functional.softmax(logits, dim=-1)
                predicted_class_id = probs.argmax().item()
                confidence = probs.max().item()
                print(f"Probabilities after softmax: {probs.cpu().numpy().flatten()}")
                print(f"Predicted class ID: {predicted_class_id}")
                print(f"Confidence: {confidence:.4f}")
        
        # Get predicted label - use class ID directly since model config has generic labels
        # The model config has LABEL_0/LABEL_1, but we know from training:
        # 0 = "not_related", 1 = "related"
        if hasattr(model.config, 'id2label') and model.config.id2label:
            print(f"Model config id2label: {model.config.id2label}")
        
        # Use our known label mapping based on class ID
        predicted_label = ID2LABEL.get(predicted_class_id, "not_related")
        print(f"Predicted label (from class ID {predicted_class_id}): {predicted_label}")
        
        # Map to risk level: "related" = Safe (Star Trek related), "not_related" = potentially unsafe
        if predicted_label == "related":
            risk_level = "Safe"
            category = "Star Trek Related"
        else:
            risk_level = "Unsafe"
            category = "Not Star Trek Related"
        
        print(f"Final risk_level: {risk_level}")
        print(f"Final category: {category}")
        print(f"{'='*60}\n")
        
        # Build response with debug info
        response = {
            'risk_level': risk_level,
            'category': category,
            'message': message,
            'confidence': float(confidence),
            'predicted_label': predicted_label,
            'predicted_class_id': int(predicted_class_id)
        }
        
        # Add debug info if available
        if probs is not None:
            response['probabilities'] = probs.cpu().numpy().flatten().tolist()
        if hasattr(model.config, 'id2label') and model.config.id2label:
            response['model_id2label'] = model.config.id2label
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in moderate endpoint: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'model_name': MODEL_PATH if model is not None else None
    })

@app.route('/', methods=['GET'])
def index():
    """API information endpoint"""
    return jsonify({
        'name': 'Qwen3Guard-StarTrek API Server',
        'version': '2.0',
        'endpoints': {
            '/api/moderate': 'POST - Moderate a single user message',
            '/health': 'GET - Health check'
        },
        'model': MODEL_PATH
    })

if __name__ == '__main__':
    print(f"Initializing Qwen3Guard-StarTrek API Server (Model: {MODEL_PATH})...")
    load_model()
    print("Starting server on http://localhost:5000")
    print("API endpoints:")
    print("  - POST /api/moderate - Moderate a single message")
    print("  - GET /health - Health check")
    app.run(host='0.0.0.0', port=5000, debug=False)

