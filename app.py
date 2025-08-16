from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from pyresparser import ResumeParser
import os
import nltk
import re

nltk.download('stopwords')

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    jd = request.form['job_description'].lower()
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    data = ResumeParser(file_path).get_extracted_data()
    resume = Resume(
        name=data.get('name', ''),
        email=data.get('email', ''),
        mobile_number=data.get('mobile_number', ''),
        college_name=', '.join(data.get('college_name', [])) if data.get('college_name') else '',
        degree=', '.join(data.get('degree', [])) if data.get('degree') else '',
        designation=', '.join(data.get('designation', [])) if data.get('designation') else '',
        company_names=', '.join(data.get('company_names', [])) if data.get('company_names') else '',
        skills=', '.join(data.get('skills', [])) if data.get('skills') else '',
        total_experience=data.get('total_experience', 0.0)
    )
    db.session.add(resume)
    db.session.commit()

    common_skills = ['python', 'sql', 'pandas', 'numpy', 'tableau', 'excel', 'aws', 'html', 'css', 'javascript', 'react', 'node.js']
    resume_skills = [s.strip().lower() for s in resume.skills.split(',')]
    jd_skills = [skill for skill in common_skills if skill in jd]

    matched_skills = [skill for skill in jd_skills if skill in resume_skills]
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]
    match_percentage = round(len(matched_skills) / len(jd_skills) * 100, 2) if jd_skills else 0
    suggested_skills_sentence = "💡 Consider adding: " + ", ".join(missing_skills) if missing_skills else "✅ You're all set!"

    # Highlight missing skills in JD
    highlighted_jd = jd
    for skill in missing_skills:
        if skill not in matched_skills:  # prevents false highlighting
            highlighted_jd = re.sub(
                rf"\b{re.escape(skill)}\b",
                f"<span style='background: yellow'>{skill}</span>",
                highlighted_jd,
                flags=re.IGNORECASE
        )
    return render_template('results.html',
        match_percentage=match_percentage,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        suggested_skills_sentence=suggested_skills_sentence,
        highlighted_jd=highlighted_jd
    )

if __name__ == '__main__':
    app.run(debug=True)
