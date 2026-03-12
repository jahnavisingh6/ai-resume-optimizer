# 🧠 AI-Powered Resume Optimizer

Associated with **Arizona State University**

An AI-driven resume optimization tool that analyzes resumes against job descriptions and generates **ATS-style improvement suggestions**.

> Built a full-stack AI-driven resume optimization tool designed to analyze resumes against job descriptions and generate actionable improvement suggestions.

---

## 🚀 Features

- **NLP-based resume–job matching**: Uses TF–IDF vectorization and cosine similarity to compute an overall match score between the resume and job description.
- **Structured resume parsing**: Uses PyResparser (built on spaCy) to extract skills, education, experience, and contact details from PDF/DOCX resumes.
- **Skill gap analysis**: Compares skills mentioned in the job description to those found in the resume, highlighting matched and missing skills.
- **Actionable suggestions**:
  - Keyword-based suggestions (which skills to add).
  - Optional ChatGPT/OpenAI-powered suggestions for phrasing and impact (when an API key is provided).
- **Web-based interface**: Simple Flask app where users upload a resume and paste a job description, then see scores, gaps, and suggestions.
- **Persistent storage**: Stores parsed resume data in SQLite by default, or PostgreSQL via environment configuration.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **NLP & Matching**: PyResparser, spaCy, scikit-learn (TF–IDF, cosine similarity), NLTK
- **Database**: SQLite by default, PostgreSQL optional
- **AI Suggestions (optional)**: OpenAI/ChatGPT APIs
- **Frontend**: Flask templates (HTML + CSS)

---

## 📊 How It Works

1. **Upload & input**  
   - User uploads a resume (PDF/DOCX) and pastes a job description in the web form.

2. **Resume parsing**  
   - PyResparser extracts:
     - Name, email, phone
     - Education and degrees
     - Experience and company names
     - Skills and total experience

3. **Storage**  
   - Parsed data is saved as a `Resume` record in PostgreSQL using SQLAlchemy.

4. **TF–IDF + cosine similarity**  
   - The app builds a free-text representation of the resume from parsed fields.
   - Uses `TfidfVectorizer` to vectorize both the resume text and the job description.
   - Uses `cosine_similarity` to compute an **overall match score (%)**.

5. **Skill overlap analysis**  
   - Uses a curated list of common technical skills (e.g., Python, SQL, Pandas, Tableau, AWS, etc.).
   - Checks which of these appear in:
     - The job description, and
     - The parsed resume skills.
   - Computes:
     - **Matched skills**
     - **Missing skills**
     - A **skill match percentage** based on overlap.
   - Highlights missing skills directly in the rendered job description text.

6. **Suggestions**  
   - Always shows a keyword-based suggestion sentence (e.g., “Consider adding: Python, Tableau”).
   - If an OpenAI API key is configured, it also calls the ChatGPT API to generate **4–6 bullet points** of tailored resume improvement suggestions (e.g., where to add keywords, how to strengthen bullet phrasing).

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/jahnavisingh6/ai-resume-optimizer.git
cd ai-resume-optimizer
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# On Windows (PowerShell):
# .venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes PyResparser, spaCy, scikit-learn, Flask, SQLAlchemy, and the OpenAI client.  
Make sure the `en_core_web_sm` spaCy model is installed (the file already references a wheel URL).

### 4. Configure the database

The app now works out of the box with a local SQLite file. No extra setup is required for local development.

To use PostgreSQL instead, export either `DATABASE_URL` or the individual `DB_*` environment variables before starting the app.

### 5. Initialize the database tables

Create tables once with:

```bash
python init_db.py
```

### 6. (Optional) Configure OpenAI / ChatGPT

Set your OpenAI API key as an environment variable (you can do this later; the app works without it):

```bash
export OPENAI_API_KEY="your_api_key_here"  # macOS/Linux
# On Windows PowerShell:
# $env:OPENAI_API_KEY="your_api_key_here"
```

If this is not set, the app will still run and show all non-LLM features.

### 7. Run the Flask app

```bash
python app.py
```

By default, the app runs on `http://127.0.0.1:5000/`.

If `pyresparser` or its NLP models are missing, the app will still load and return limited analysis instead of crashing.

### 8. Deploying on Vercel + Supabase

- Host the Flask app on Vercel.
- Use Supabase PostgreSQL for `DATABASE_URL`.
- For Vercel/serverless deployments, create tables ahead of time with `python init_db.py` instead of creating them at startup.
- Add `SECRET_KEY`, `DATABASE_URL`, and optionally `OPENAI_API_KEY` as environment variables.
- Use the Supabase pooled connection string when possible.

Open that URL in your browser, upload a resume, paste a job description, and view:
- Overall TF–IDF similarity score
- Skill match percentage
- Matched vs missing skills
- Keyword-based suggestions
- (Optionally) ChatGPT-powered bullet suggestions.

---

## 🧩 Project Structure

```text
app.py              # Flask app, routes, TF–IDF & similarity logic, OpenAI integration
config.py           # PostgreSQL connection configuration
models.py           # SQLAlchemy Resume model
templates/
  ├─ index.html     # Upload form & information sections
  └─ results.html   # Match scores, skills, suggestions, highlighted JD
static/
  └─ style.css      # Styling for the web UI
requirements.txt    # Python dependencies
```

---

## 🎯 How to Describe This on Your Resume

**AI-Powered Resume Optimizer – Arizona State University**  
Built a full-stack AI-driven resume optimization tool that analyzes resumes against job descriptions using TF–IDF vectorization and cosine similarity, computes match scores, identifies missing skills, and generates actionable improvement suggestions. Parsed resumes with PyResparser and spaCy, stored structured data in PostgreSQL via SQLAlchemy, and integrated optional OpenAI/ChatGPT APIs for ATS-friendly, bullet-point resume recommendations.

**Skills:** Python, Flask, PostgreSQL, SQLAlchemy, spaCy, PyResparser, scikit-learn, NLP, OpenAI/ChatGPT APIs

---

## 👩‍💻 Author

**Jahnavi Singh**

- M.S. Information Technology @ ASU
- Data Scientist | Analyst | Software Developer
- 🌐 Portfolio: https://jahnavi-theta.vercel.app/
- 💼 LinkedIn: https://www.linkedin.com/in/jahnavisingh6/
- 📧 Email: jahnavisingh6@gmail.com
