from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from database import Base

class EvaluationRecord(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    filename = Column(String(255), nullable=False)
    match_score = Column(Float, nullable=False)
    matched_skills = Column(Text, nullable=True)   # Comma separated
    missing_skills = Column(Text, nullable=True)   # Comma separated
    created_at = Column(DateTime, default=datetime.utcnow)