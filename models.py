from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))
    college_name = db.Column(db.String(200))
    degree = db.Column(db.String(200))
    designation = db.Column(db.String(200))
    company_names = db.Column(db.Text)
    skills = db.Column(db.Text)
    total_experience = db.Column(db.Float)

