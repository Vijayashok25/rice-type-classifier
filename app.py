import os
import io
import json
import base64
from PIL import Image
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from backend.db import init_db, insert_prediction, get_all_predictions, delete_all_predictions
from predict import predict_rice_image, get_predictor

app = Flask(__name__, static_folder='frontend/public', static_url_path='')
CORS(app)

# Initialize Database on server startup
init_db()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """
    Endpoint: POST /predict
    Accepts multipart/form-data with file key 'image'.
    Performs CNN classification, saves to SQLite database, returns prediction payload.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided in request. Key must be "image".'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename submitted.'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': f'Unsupported file format. Allowed extensions: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
    try:
        # Read image stream into PIL Image
        image_bytes = file.read()
        pil_img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Perform Model Prediction
        result = predict_rice_image(pil_img)
        
        # Generate base64 thumbnail for UI history display
        thumb = pil_img.copy()
        thumb.thumbnail((120, 120))
        buffered = io.BytesIO()
        thumb.save(buffered, format="JPEG", quality=80)
        img_b64 = "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Insert record into SQLite DB
        db_entry = insert_prediction(
            filename=file.filename,
            predicted_class=result['predicted_class'],
            confidence=result['confidence'],
            image_data=img_b64
        )
        
        response_payload = {
            'success': True,
            'id': db_entry['id'],
            'filename': file.filename,
            'predicted_class': result['predicted_class'],
            'confidence': result['confidence'],
            'probabilities': result['probabilities'],
            'timestamp': db_entry['timestamp'],
            'image_data': img_b64
        }
        return jsonify(response_payload), 200

    except Exception as e:
        print(f"[ERROR] Prediction failed: {str(e)}")
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/history', methods=['GET'])
def history_get_endpoint():
    """
    Endpoint: GET /history
    Retrieves all past predictions from SQLite database with distribution stats.
    """
    try:
        records = get_all_predictions()
        total = len(records)
        class_counts = {}
        if total > 0:
            for r in records:
                cls = r['predicted_class']
                class_counts[cls] = class_counts.get(cls, 0) + 1
                
        return jsonify({
            'success': True,
            'count': total,
            'class_distribution': class_counts,
            'history': records
        }), 200
    except Exception as e:
        return jsonify({'error': f'Database fetch error: {str(e)}'}), 500

@app.route('/history', methods=['DELETE'])
def history_delete_endpoint():
    """
    Endpoint: DELETE /history
    Clears all stored prediction records from SQLite database.
    """
    try:
        delete_all_predictions()
        return jsonify({'success': True, 'message': 'Prediction history cleared successfully.'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to delete history: {str(e)}'}), 500

@app.route('/metrics', methods=['GET'])
def metrics_endpoint():
    """
    Endpoint: GET /metrics
    Returns model metrics, confusion matrix, classification report, and plots.
    """
    try:
        model_dir = 'model'
        report = ""
        report_file = os.path.join(model_dir, 'classification_report.txt')
        if os.path.exists(report_file):
            with open(report_file, 'r') as f:
                report = f.read()
                
        has_plot = os.path.exists(os.path.join(model_dir, 'accuracy_loss_plot.png'))
        has_cm = os.path.exists(os.path.join(model_dir, 'confusion_matrix.png'))
        
        return jsonify({
            'success': True,
            'classification_report': report,
            'has_accuracy_loss_plot': has_plot,
            'has_confusion_matrix': has_cm
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/model-files/<path:filename>')
def serve_model_files(filename):
    """Serves generated model evaluation files (plots, confusion matrix)."""
    return send_from_directory('model', filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serves static project assets (samples, screenshots)."""
    return send_from_directory('assets', filename)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'online',
        'app': 'Rice Type Classifier REST API',
        'classes': ['Arborio', 'Basmati', 'Ipsala', 'Jasmine', 'Karacadag']
    }), 200

@app.route('/')
def index():
    """Serves the React Web Application Frontend."""
    return send_from_directory('frontend/public', 'index.html')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("RICE TYPE CLASSIFIER FLASK REST SERVER")
    print("="*50)
    print("REST API Endpoints:")
    print(" - POST   /predict   (Upload & Classify image)")
    print(" - GET    /history   (Fetch SQLite prediction history)")
    print(" - DELETE /history   (Clear prediction history)")
    print(" - GET    /metrics   (View model graphs & classification report)")
    print(" - GET    /health    (Health status check)")
    print("Web UI Dashboard: http://127.0.0.1:5000/")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
