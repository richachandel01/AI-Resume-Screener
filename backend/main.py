from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# FastAPI NLP Service ka URL
NLP_SERVICE_URL = "http://127.0.0.1:5002/extract"

@app.route('/')
def home():
    return jsonify({"message": "Flask server is running 🚀"})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith(('.pdf', '.docx')):
        return jsonify({"error": "File type not allowed"}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    with open(filepath, "rb") as f:
        files = {"file": (file.filename, f, file.mimetype)}
        try:
            response = requests.post(NLP_SERVICE_URL, files=files)
            nlp_result = response.json()
        except Exception as e:
            return jsonify({"error": f"Failed to connect to NLP service: {str(e)}"}), 500

    return jsonify({
        "message": "File uploaded successfully",
        "path": filepath,
        "nlp_result": nlp_result
    })
if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(debug=True, host="127.0.0.1", port=5001)
