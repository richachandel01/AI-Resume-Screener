from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    skills = db.Column(db.Text)
    education = db.Column(db.Text)
    experience = db.Column(db.Text)

    def __init__(self, name, email, phone, skills, education, experience):
        self.name = name
        self.email = email
        self.phone = phone
        self.skills = skills
        self.education = education
        self.experience = experience

    def __repr__(self):
        return f"<Resume {self.name}>"
