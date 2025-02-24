from sqlalchemy import Column, String, Integer, DateTime, Float
from src.utils.db import Base
from datetime import datetime


class RawLoan(Base):
    __tablename__ = "loans"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(String)
    user_id = Column(String)
    amount = Column(Integer)
    interest_rate = Column(Float)
    term = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawPayment(Base):
    __tablename__ = "payments"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(String)
    loan_id = Column(String)
    amount = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
