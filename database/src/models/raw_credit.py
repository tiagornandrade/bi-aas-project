from sqlalchemy import Column, String, Integer, DateTime
from src.utils.db import Base
from datetime import datetime


class RawCreditScore(Base):
    __tablename__ = "credit_scores"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    score_id = Column(String)
    user_id = Column(String)
    score = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawRiskAssessment(Base):
    __tablename__ = "risk_assessments"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(String)
    user_id = Column(String)
    risk_level = Column(String)
    details = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
