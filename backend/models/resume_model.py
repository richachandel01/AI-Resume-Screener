from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    emails = db.Column(db.Text, nullable=True)
    names = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
from app import db

class Resume(db.Model):
    __tablename__ = 'resumes'  # Name of the table in database

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    education = db.Column(db.Text)

    # Helper function to convert model to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education
        }































