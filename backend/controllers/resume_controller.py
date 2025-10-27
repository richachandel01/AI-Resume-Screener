from flask import Blueprint, request, jsonify
from models.resume_model import db, Resume

resume_bp = Blueprint('resume_bp', __name__)

# Create new resume (expects JSON)
@resume_bp.route('/api/resumes', methods=['POST'])
def create_resume():
    data = request.get_json() or {}
    try:
        new_resume = Resume(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            skills=data.get('skills'),
            experience=data.get('experience'),
            education=data.get('education')
        )
        db.session.add(new_resume)
        db.session.commit()
        return jsonify({"message": "Resume created successfully!", "id": new_resume.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Get all resumes
@resume_bp.route('/api/resumes', methods=['GET'])
def get_resumes():
    resumes = Resume.query.order_by(Resume.id.desc()).all()
    return jsonify([r.to_dict() for r in resumes])

# Get resume by id
@resume_bp.route('/api/resumes/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    r = Resume.query.get_or_404(resume_id)
    return jsonify(r.to_dict())

# Delete resume
@resume_bp.route('/api/resumes/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    r = Resume.query.get_or_404(resume_id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({"message": "Resume deleted successfully."})
