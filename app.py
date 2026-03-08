from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from pyresparser import ResumeParser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
import os
import nltk
import re

nltk.download('stopwords')

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Initialize OpenAI client (expects OPENAI_API_KEY in environment).
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

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
    jd_raw = request.form['job_description']
    jd = jd_raw.lower()
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Parse resume into structured fields using PyResparser.
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

    # Build a free-text representation of the resume for TF-IDF similarity.
    text_chunks = []
    for key in ['name', 'college_name', 'degree', 'designation', 'company_names']:
        value = data.get(key)
        if isinstance(value, list):
            text_chunks.extend([str(v) for v in value])
        elif value:
            text_chunks.append(str(value))

    skills_list = data.get('skills') or []
    if isinstance(skills_list, list):
        text_chunks.extend(skills_list)
    else:
        text_chunks.append(str(skills_list))

    experience = data.get('experience')
    if isinstance(experience, list):
        text_chunks.extend([str(e) for e in experience])
    elif experience:
        text_chunks.append(str(experience))

    resume_text = " ".join(text_chunks).strip()

    # Compute TF-IDF based semantic similarity score between resume and job description.
    if resume_text and jd_raw.strip():
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_raw])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        tfidf_match_score = round(similarity * 100, 2)
    else:
        tfidf_match_score = 0.0

    # Skill-level overlap (to identify clearly missing skills).
    common_skills = ['python', 'sql', 'pandas', 'numpy', 'tableau', 'excel', 'aws', 'html', 'css', 'javascript', 'react', 'node.js']
    resume_skills = [s.strip().lower() for s in resume.skills.split(',') if s.strip()]
    jd_skills = [skill for skill in common_skills if skill in jd]

    matched_skills = [skill for skill in jd_skills if skill in resume_skills]
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]
    match_percentage = round(len(matched_skills) / len(jd_skills) * 100, 2) if jd_skills else 0
    suggested_skills_sentence = "💡 Consider adding: " + ", ".join(missing_skills) if missing_skills else "✅ You're all set!"

    # Highlight missing skills in the original-cased job description.
    highlighted_jd = jd_raw
    for skill in missing_skills:
        if skill not in matched_skills:
            highlighted_jd = re.sub(
                rf"\b{re.escape(skill)}\b",
                f"<span style='background: yellow'>{skill}</span>",
                highlighted_jd,
                flags=re.IGNORECASE
            )

    # Generate richer resume improvement suggestions via OpenAI (if configured).
    llm_suggestions = None
    if openai_client and resume_text and jd_raw.strip():
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert resume coach helping a candidate tailor their resume "
                            "to a specific job description. Focus on keyword alignment, quantifiable "
                            "impact, and strong action verbs."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Job description:\n{jd_raw}\n\n"
                            f"Extracted resume skills: {', '.join(resume_skills)}\n"
                            f"Matched skills: {', '.join(matched_skills) or 'None'}\n"
                            f"Missing skills: {', '.join(missing_skills) or 'None'}\n"
                            f"TF-IDF match score: {tfidf_match_score}%\n\n"
                            "Give 4–6 bullet points with specific, ATS-friendly suggestions to improve "
                            "this resume for this job. Mention where to add or rephrase content."
                        ),
                    },
                ],
            )
            llm_suggestions = response.choices[0].message.content.strip()
        except Exception:
            llm_suggestions = None

    return render_template(
        'results.html',
        match_percentage=match_percentage,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        suggested_skills_sentence=suggested_skills_sentence,
        highlighted_jd=highlighted_jd,
        tfidf_match_score=tfidf_match_score,
        llm_suggestions=llm_suggestions,
    )

if __name__ == '__main__':
    app.run(debug=True)
