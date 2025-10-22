from flask import Blueprint, request, jsonify
from app import db
from models.resume_model import Resume

# Create a blueprint for resume routes
resume_routes = Blueprint('resume_routes', __name__)

# POST route to add a new resume
@resume_routes.route('/api/resumes', methods=['POST'])
def add_resume():
    data = request.get_json()
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
    return jsonify({"message": "Resume added successfully!"}), 201

# GET route to fetch all resumes
@resume_routes.route('/api/resumes', methods=['GET'])
def get_resumes():
    resumes = Resume.query.all()
    return jsonify([r.to_dict() for r in resumes])
