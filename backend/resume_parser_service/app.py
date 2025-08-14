from flask import Flask, request, jsonify
import os
import fitz  # PyMuPDF
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # frontend ke liye cross-origin enable

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def extract_text_from_pdf(file_path):
    """PDF se text extract karega"""
    text = ""
    pdf = fitz.open(file_path)
    for page in pdf:
        text += page.get_text()
    return text


def parse_resume(text):
    """Simple parsing example"""
    data = {}
    lines = text.split("\n")

    # Name (first non-empty line)
    for line in lines:
        if line.strip():
            data["name"] = line.strip()
            break

    # Email search
    import re
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
    data["email"] = email_match.group(0) if email_match else None

    # Skills example (ye tum apne keywords list se expand kar sakti ho)
    skills_list = ["Python", "Java", "C++", "HTML", "CSS", "JavaScript", "SQL"]
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    data["skills"] = found_skills

    return data


@app.route("/parse-resume", methods=["POST"])
def parse_resume_api():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Extract text & parse
    text = extract_text_from_pdf(file_path)
    parsed_data = parse_resume(text)

    return jsonify({
        "filename": file.filename,
        "parsed_data": parsed_data
    })


if __name__ == "__main__":
    app.run(port=5001, debug=True)
