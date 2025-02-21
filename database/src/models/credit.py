from sqlalchemy import Column, String, Integer, TIMESTAMP, BigInteger
from src.utils.db import Base
from datetime import datetime


class CreditScore(Base):
    __tablename__ = "credit_scores"
<<<<<<< Updated upstream
    __table_args__ = {"extend_existing": True}
=======
>>>>>>> Stashed changes

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    score_id = Column(String)
    user_id = Column(String)
    score = Column(Integer)
    last_updated = Column(TIMESTAMP, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
<<<<<<< Updated upstream
    __table_args__ = {"extend_existing": True}
=======

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    assessment_id = Column(String)
    user_id = Column(String)
    risk_level = Column(String)
    details = Column(String)
    date = Column(TIMESTAMP, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawCreditScore(Base):
    __tablename__ = "raw_credit_scores"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    score_id = Column(String)
    user_id = Column(String)
    score = Column(Integer)
    last_updated = Column(TIMESTAMP, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawRiskAssessment(Base):
    __tablename__ = "raw_risk_assessments"
>>>>>>> Stashed changes

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    assessment_id = Column(String)
    user_id = Column(String)
    risk_level = Column(String)
    details = Column(String)
    date = Column(TIMESTAMP, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
