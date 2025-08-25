# 🧠 AI Resume Optimizer  

An **AI-powered Resume Matching & Optimization Tool** that analyzes resumes against job descriptions and provides **ATS-style feedback** with improvement suggestions.  

---

## 🚀 Features
- 📄 **Resume Parsing**: Extracts structured information (skills, education, experience) using `spaCy` + `pyresparser`  
- 🧾 **Job Description Analysis**: Identifies key requirements and matches them against resume content  
- ⚡ **ATS Scoring**: Generates a similarity score showing how well the resume fits the role  
- 💡 **Improvement Suggestions**: Highlights missing keywords, skills, and formatting issues  
- 🌐 **Web + CLI**: Works as both a Python CLI tool and a web app (Next.js frontend + FastAPI backend)  
- ☁️ **Deployable**: Built to run locally or host easily on platforms like Vercel/Docker  

---

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, spaCy, scikit-learn, pyresparser  
- **Frontend**: Next.js, React  
- **Database**: PostgreSQL  
- **Other**: Docker, GitHub Actions (CI/CD), Vercel  

---

## 📊 How It Works
1. Upload your resume (PDF/DOCX) + paste a job description  
2. Resume is parsed into structured JSON format  
3. Job description is analyzed for keywords and requirements  
4. NLP model computes **semantic similarity score**  
5. System outputs **ATS match % + personalized suggestions**  

---

## 📸 Demo
Screenshots and UI previews will be added soon.  
In the meantime, here’s an example of CLI usage:  

```bash
python main.py --resume sample_resume.pdf --jd job_description.txt
````

**Output Example:**

```
ATS Match Score: 78%
Missing Keywords: Python, Tableau
Suggestions: Add relevant projects under 'Experience'
```

---

## ⚡ Quick Start

Clone the repo and run locally:

```bash
git clone https://github.com/jahnavisingh6/ai-resume-optimizer.git
cd ai-resume-optimizer
pip install -r requirements.txt
python main.py --resume sample_resume.pdf --jd job_description.txt
```

For the web app:

```bash
npm install
npm run dev
```

---

## 🎯 Use Cases

* Job seekers improving resumes for ATS systems
* Recruiters screening candidates quickly
* Universities & career centers offering resume feedback

---

## 📌 Roadmap

* [ ] Add LinkedIn profile parsing
* [ ] Integrate with LLMs (OpenAI API / LangChain) for deeper suggestions
* [ ] Multi-language resume support
* [ ] Cloud deployment (AWS/Supabase)
* [ ] PDF preview + copyable recommendations

---

## 👩‍💻 Author

**Jahnavi Singh**

* M.S. Information Technology @ ASU
* Data Scientist | Analyst | Software Developer
* 🌐 [Portfolio](https://jahnavi-theta.vercel.app/)
* 💼 [LinkedIn](https://www.linkedin.com/in/jahnavisingh6/)
* 📧 [Email](mailto:jahnavisingh6@gmail.com)

```

