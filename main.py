from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from database import SessionLocal, engine
from models import Base, User, Resume

import shutil
import PyPDF2

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

Base.metadata.create_all(bind=engine)

app = FastAPI()

# SESSION
app.add_middleware(SessionMiddleware, secret_key="secret")

# STATIC FILES
app.mount("/static", StaticFiles(directory="static"), name="static")

# TEMPLATES
templates = Jinja2Templates(directory="templates")


# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


# HOME
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# REGISTER PAGE
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


# REGISTER USER
@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...)
):

    db = get_db()

    existing_user = db.query(User).filter(
        User.username == username
    ).first()

    if existing_user:

        return HTMLResponse("""
        <h2>User already exists ❌</h2>
        <a href='/register'>Go Back</a>
        """)

    new_user = User(
        username=username,
        password=password
    )

    db.add(new_user)
    db.commit()

    return RedirectResponse(
        "/login",
        status_code=303
    )


# LOGIN PAGE
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


# LOGIN USER
@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    db = get_db()

    user = db.query(User).filter(
        User.username == username,
        User.password == password
    ).first()

    if user:

        request.session["user"] = username

        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    return HTMLResponse("""
    <h2>Invalid Username or Password ❌</h2>
    <a href='/login'>Try Again</a>
    """)


# DASHBOARD
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    username = request.session.get("user")

    if not username:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username
        }
    )


# ANALYZE RESUME
@app.post("/analyze", response_class=HTMLResponse)
async def analyze_resume(
    request: Request,
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    username = request.session.get("user")

    if not username:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    # SAVE FILE
    filepath = f"uploads/{resume.filename}"

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(
            resume.file,
            buffer
        )

    resume_text = ""

    # PDF SUPPORT
    if resume.filename.endswith(".pdf"):

        with open(filepath, "rb") as file:

            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:

                text = page.extract_text()

                if text:

                    resume_text += text.lower()

    # TXT SUPPORT
    elif resume.filename.endswith(".txt"):

        with open(filepath, "r", errors="ignore") as file:

            resume_text = file.read().lower()

    else:

        return HTMLResponse("""
        <h2>Only PDF and TXT files are supported ❌</h2>
        <a href='/dashboard'>Go Back</a>
        """)

    # AI MATCHING
    documents = [
        resume_text,
        job_description.lower()
    ]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )

    score = round(
        similarity[0][0] * 100,
        2
    )

    # SIMPLE SKILL MATCHING
    jd_words = set(job_description.lower().split())

    resume_words = set(resume_text.split())

    matched = jd_words.intersection(resume_words)

    missing = jd_words - resume_words

    # SAVE TO DATABASE
    db = get_db()

    new_resume = Resume(
        username=username,
        filename=resume.filename,
        score=str(score)
    )

    db.add(new_resume)
    db.commit()

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "score": score,
            "matched": list(matched)[:15],
            "missing": list(missing)[:15],
            "filename": resume.filename,
            "username": username
        }
    )


# LOGOUT
@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        "/",
        status_code=303
    )