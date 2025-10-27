from flask import Flask
from flask_cors import CORS
from models.resume_model import db
from routes.resume import resume_bp

app = Flask(__name__)
CORS(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/resumes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register blueprint routes
app.register_blueprint(resume_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
