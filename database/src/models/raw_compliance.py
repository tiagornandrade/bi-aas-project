from sqlalchemy import Column, String, DateTime, Integer
from src.utils.db import Base
from datetime import datetime


class RawRegulation(Base):
    __tablename__ = "regulations"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    regulation_id = Column(String)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    jurisdiction = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawUserVerification(Base):
    __tablename__ = "regulations"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    verification_id = Column(String)
    user_id = Column(String)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
