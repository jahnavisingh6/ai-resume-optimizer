from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from markupsafe import escape
from werkzeug.utils import secure_filename
import os
import re

from models import Resume, db

try:
    from pyresparser import ResumeParser
except Exception:
    ResumeParser = None

# Initialize OpenAI client (expects OPENAI_API_KEY in environment).
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

COMMON_SKILLS = [
    "python",
    "sql",
    "pandas",
    "numpy",
    "tableau",
    "excel",
    "aws",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
]
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def safe_join(value) -> str:
    if not value:
        return ""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if item)
    return str(value)


def extract_resume_data(file_path: str, manual_name: str = ""):
    parser_warning = None
    data = {}

    if ResumeParser is None:
        parser_warning = "PyResparser is not installed. Showing limited results without resume parsing."
    else:
        try:
            data = ResumeParser(file_path).get_extracted_data() or {}
        except Exception:
            parser_warning = "Resume parsing failed. Showing limited results without parsed resume details."
            data = {}

    if manual_name and not data.get("name"):
        data["name"] = manual_name.strip()

    return data, parser_warning


def build_resume_text(data: dict) -> str:
    text_chunks = []
    for key in ["name", "college_name", "degree", "designation", "company_names"]:
        value = data.get(key)
        if isinstance(value, list):
            text_chunks.extend(str(v) for v in value if v)
        elif value:
            text_chunks.append(str(value))

    skills = data.get("skills") or []
    if isinstance(skills, list):
        text_chunks.extend(str(skill) for skill in skills if skill)
    elif skills:
        text_chunks.append(str(skills))

    experience = data.get("experience")
    if isinstance(experience, list):
        text_chunks.extend(str(item) for item in experience if item)
    elif experience:
        text_chunks.append(str(experience))

    return " ".join(text_chunks).strip()


def highlight_missing_skills(job_description: str, missing_skills: list[str]) -> str:
    highlighted = escape(job_description)
    for skill in missing_skills:
        highlighted = re.sub(
            rf"\b{re.escape(skill)}\b",
            f"<span class='skill-highlight'>{escape(skill)}</span>",
            str(highlighted),
            flags=re.IGNORECASE,
        )
    return highlighted


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/upload_resume", methods=["POST"])
    def upload_resume():
        file = request.files.get("resume")
        jd_raw = request.form.get("job_description", "").strip()
        manual_name = request.form.get("manual_name", "").strip()

        if not file or not file.filename:
            return render_template("results.html", error_message="Please upload a resume file."), 400
        if not jd_raw:
            return render_template("results.html", error_message="Please paste a job description."), 400
        if not allowed_file(file.filename):
            return render_template("results.html", error_message="Please upload a PDF, DOC, or DOCX file."), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        try:
            data, parser_warning = extract_resume_data(file_path, manual_name=manual_name)
        finally:
            try:
                os.remove(file_path)
            except OSError:
                pass

        resume = Resume(
            name=data.get("name", manual_name),
            email=data.get("email", ""),
            mobile_number=data.get("mobile_number", ""),
            college_name=safe_join(data.get("college_name")),
            degree=safe_join(data.get("degree")),
            designation=safe_join(data.get("designation")),
            company_names=safe_join(data.get("company_names")),
            skills=safe_join(data.get("skills")),
            total_experience=float(data.get("total_experience") or 0.0),
        )
        db.session.add(resume)
        db.session.commit()

        resume_text = build_resume_text(data)

        if resume_text:
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform([resume_text, jd_raw])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            tfidf_match_score = round(similarity * 100, 2)
        else:
            tfidf_match_score = 0.0

        jd_lower = jd_raw.lower()
        resume_skills = [s.strip().lower() for s in resume.skills.split(",") if s.strip()]
        jd_skills = [skill for skill in COMMON_SKILLS if skill in jd_lower]
        matched_skills = [skill for skill in jd_skills if skill in resume_skills]
        missing_skills = [skill for skill in jd_skills if skill not in resume_skills]
        match_percentage = round(len(matched_skills) / len(jd_skills) * 100, 2) if jd_skills else 0
        suggested_skills_sentence = (
            "Consider adding: " + ", ".join(missing_skills) if missing_skills else "No obvious skill gaps found."
        )
        highlighted_jd = highlight_missing_skills(jd_raw, missing_skills)

        llm_suggestions = None
        if openai_client and jd_raw:
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
                                f"Extracted resume skills: {', '.join(resume_skills) or 'None'}\n"
                                f"Matched skills: {', '.join(matched_skills) or 'None'}\n"
                                f"Missing skills: {', '.join(missing_skills) or 'None'}\n"
                                f"TF-IDF match score: {tfidf_match_score}%\n\n"
                                "Give 4-6 bullet points with ATS-friendly suggestions to improve the resume. "
                                "Mention where to add or rephrase content."
                            ),
                        },
                    ],
                )
                llm_suggestions = response.choices[0].message.content.strip()
            except Exception:
                llm_suggestions = None

        return render_template(
            "results.html",
            error_message=None,
            parser_warning=parser_warning,
            match_percentage=match_percentage,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            suggested_skills_sentence=suggested_skills_sentence,
            highlighted_jd=highlighted_jd,
            tfidf_match_score=tfidf_match_score,
            llm_suggestions=llm_suggestions,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
