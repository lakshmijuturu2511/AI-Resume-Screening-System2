# 🧠 AI Resume Screening System
An AI-powered Resume Screening and ATS Analyzer built using FastAPI, Python, SQLite, and Machine Learning concepts.
This system allows users to upload resumes (PDF/TXT), compare them with job descriptions, calculate ATS compatibility scores, and identify matched and missing skills.
---
# 🚀 Features
✅ User Registration & Login  
✅ Session-Based Authentication  
✅ Upload Resume (PDF/TXT)  
✅ ATS Score Calculation  
✅ Resume Parsing  
✅ Skill Matching System  
✅ Missing Skill Detection  
✅ AI-Based Resume Analysis  
✅ Responsive Modern UI  
✅ Database Integration using SQLite  
---
# 🛠️ Tech Stack
## Backend
- FastAPI
- Python
- SQLAlchemy
## Frontend
- HTML
- CSS
## Database
- SQLite
## AI / NLP
- TF-IDF Vectorization
- Cosine Similarity
- Scikit-learn
---
# 📂 Project Structure
```bash
ai_resume_system/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── result.html
│
├── uploads/
│
├── main.py
├── models.py
├── database.py
├── resumes.db
└── README.md

⸻

⚙️ Installation & Setup

1️⃣ Clone Repository

git clone https://github.com/your-username/AI-Resume-Screening-System.git
cd AI-Resume-Screening-System

⸻

2️⃣ Create Virtual Environment

Mac/Linux

python3 -m venv venv
source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate

⸻

3️⃣ Install Dependencies

pip install fastapi uvicorn sqlalchemy jinja2 python-multipart scikit-learn PyPDF2 itsdangerous

⸻

4️⃣ Run Server

uvicorn main:app --reload

⸻

▶️ Open in Browser

http://127.0.0.1:8000

⸻

📄 Supported Resume Formats

✅ PDF
✅ TXT

⸻

🧠 AI Matching Logic

The system uses:

* TF-IDF Vectorization
* Cosine Similarity

to compare:

* Resume Content
* Job Description

and generate:

* ATS Compatibility Score
* Matched Skills
* Missing Skills

⸻

📷 Features Demonstrated

Dashboard

* Upload Resume
* Enter Job Description
* Analyze Resume

Result Page

* ATS Score
* Skill Matching
* Missing Skills
* Progress Visualization

⸻

🔐 Authentication Features

* User Registration
* User Login
* Session Management
* Logout Support

⸻

📈 Future Enhancements

🚀 Resume Ranking System
🚀 AI Suggestions
🚀 Gemini/OpenAI Integration
🚀 Download PDF Report
🚀 Admin Dashboard
🚀 Email Notifications
🚀 Charts & Analytics

⸻

🎯 Learning Outcomes

Through this project, I learned:

* FastAPI Backend Development
* Authentication & Sessions
* File Upload Handling
* PDF Parsing
* Database Management using SQLAlchemy
* NLP-Based Similarity Matching
* Full Stack Web Development
* Git & GitHub Version Control

⸻

