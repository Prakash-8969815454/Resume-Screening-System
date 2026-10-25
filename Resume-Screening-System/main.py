from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import shutil

from config import UPLOAD_DIR
from database import Base, engine, get_db
from DB_model import EvaluationRecord
from parsar import parse_resume
from nlp_engine import extract_email, extract_phone, calculate_match_score

# Initialize DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ATS Resume Screener", version="1.0.0")

@app.get("/")
def serve_home():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

@app.post("/api/v1/screen")
async def screen_resume(
    job_description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate File Extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in [".pdf", ".docx"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Upload PDF or DOCX.")

    # Save uploaded file locally
    saved_file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(saved_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Parse Text
        resume_text = parse_resume(saved_file_path)

        # Extract Info & Calculate TF-IDF Score
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)
        analysis_result = calculate_match_score(resume_text, job_description)

        # Save to SQLite Database
        record = EvaluationRecord(
            filename=file.filename,
            email=email,
            phone=phone,
            match_score=analysis_result["match_score"],
            matched_skills=", ".join(analysis_result["matched_skills"]),
            missing_skills=", ".join(analysis_result["missing_skills"])
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "status": "success",
            "candidate_info": {"email": email, "phone": phone},
            "match_score": analysis_result["match_score"],
            "matched_skills": analysis_result["matched_skills"],
            "missing_skills": analysis_result["missing_skills"],
            "record_id": record.id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))