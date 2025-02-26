import os
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from src.utils.db import Base
from datetime import datetime


Base = declarative_base()

DB_URL = os.getenv("TEST_DB_URL", "sqlite:///:memory:")
is_sqlite = "sqlite" in DB_URL


class Policy(Base):
    __tablename__ = "policies"
    __table_args__ = {} if is_sqlite else {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    event_uuid = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Claim(Base):
    __tablename__ = "claims"
    __table_args__ = {} if is_sqlite else {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    event_uuid = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class InsuredEntity(Base):
    __tablename__ = "insured_entities"
    __table_args__ = {} if is_sqlite else {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    event_uuid = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow, nullable=False)
