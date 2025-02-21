from sqlalchemy import Column, String, Integer, TIMESTAMP, BigInteger, Float
from src.utils.db import Base
from datetime import datetime


class Loan(Base):
    __tablename__ = "loans"
<<<<<<< Updated upstream
    __table_args__ = {"extend_existing": True}
=======
>>>>>>> Stashed changes

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    loan_id = Column(String)
    user_id = Column(String)
    amount = Column(Integer)
    interest_rate = Column(Float)
    term = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"
<<<<<<< Updated upstream
    __table_args__ = {"extend_existing": True}
=======

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    payment_id = Column(String)
    loan_id = Column(String)
    amount = Column(Integer)
    date = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawLoan(Base):
    __tablename__ = "raw_loans"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    loan_id = Column(String)
    user_id = Column(String)
    amount = Column(Integer)
    interest_rate = Column(Float)
    term = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawPayment(Base):
    __tablename__ = "raw_payments"
>>>>>>> Stashed changes

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    payment_id = Column(String)
    loan_id = Column(String)
    amount = Column(Integer)
    date = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
