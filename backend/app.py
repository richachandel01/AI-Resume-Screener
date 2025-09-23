import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Send file to NLP service
    with open(filepath, 'rb') as f:
        response = requests.post("http://127.0.0.1:5002/extract", files={"file": f})

    if response.status_code == 200:
        extracted_data = response.json()
        return jsonify({
            "filename": file.filename,
            "message": "File uploaded and parsed successfully!",
            "data": extracted_data
        })
    else:
        return jsonify({"error": "NLP service failed"}), 500
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
