from sqlalchemy import Column, String, DateTime, Integer
from src.utils.db import Base
from datetime import datetime


class Regulation(Base):
    __tablename__ = "regulations"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    regulation_id = Column(String)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    jurisdiction = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserVerification(Base):
    __tablename__ = "user_verifications"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    verification_id = Column(String)
    user_id = Column(String)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
