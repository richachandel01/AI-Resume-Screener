from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import requests
from datetime import datetime

# Initialize app and database
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Resume model
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    phone = db.Column(db.String(64))
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    education = db.Column(db.Text)
    filename = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills.split(",") if self.skills else [],
            "experience": self.experience,
            "education": self.education,
            "filename": self.filename,
            "created_at": self.created_at.isoformat()
        }

# Ensure upload folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

NLP_SERVICE_URL = "http://127.0.0.1:5002/extract"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        with open(filepath, "rb") as f:
            resp = requests.post(NLP_SERVICE_URL, files={"file": f}, timeout=30)
            resp.raise_for_status()
            parsed = resp.json()
    except Exception as e:
        return jsonify({"error": f"NLP service failed: {str(e)}"}), 500

    name = parsed.get("names", [None])[0] if parsed.get("names") else None
    email = parsed.get("emails", [None])[0] if parsed.get("emails") else None
    phone = parsed.get("phone", None)
    skills = ",".join(parsed.get("skills", [])) if parsed.get("skills") else None
    experience = parsed.get("experience", None)
    education = parsed.get("education", None)

    resume = Resume(
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        experience=experience,
        education=education,
        filename=file.filename
    )
    db.session.add(resume)
    db.session.commit()

    return jsonify({
        "message": "✅ File uploaded and saved successfully!",
        "resume_id": resume.id,
        "data": parsed
    }), 200


@app.route("/resumes", methods=["GET"])
def list_resumes():
    resumes = Resume.query.order_by(Resume.id.desc()).all()
    return jsonify([r.to_dict() for r in resumes])


@app.route("/resumes/<int:resume_id>", methods=["GET"])
def get_resume(resume_id):
    r = Resume.query.get_or_404(resume_id)
    return jsonify(r.to_dict())


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
