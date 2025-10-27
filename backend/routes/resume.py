from flask import Blueprint, jsonify, request
from models.resume_model import db, Resume

resume_bp = Blueprint('resume_bp', __name__, url_prefix='/api/resumes')

@resume_bp.route('/', methods=['GET'])
def get_resumes():
    resumes = Resume.query.all()
    result = [
        {
            "id": r.id,
            "name": r.name,
            "email": r.email,
            "skills": r.skills
        } for r in resumes
    ]
    return jsonify(result)

@resume_bp.route('/', methods=['POST'])
def add_resume():
    data = request.get_json()
    new_resume = Resume(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone', ''),
        skills=data.get('skills', ''),
        education=data.get('education', ''),
        experience=data.get('experience', '')
    )
    db.session.add(new_resume)
    db.session.commit()
    return jsonify({"message": "Resume added successfully!"}), 201

@resume_bp.route('/<int:id>', methods=['DELETE'])
def delete_resume(id):
    resume = Resume.query.get(id)
    if not resume:
        return jsonify({"message": "Resume not found"}), 404
    db.session.delete(resume)
    db.session.commit()
    return jsonify({"message": "Resume deleted successfully!"})
