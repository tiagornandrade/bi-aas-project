import os
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from src.utils.db import Base
from datetime import datetime


Base = declarative_base()

DB_URL = os.getenv("TEST_DB_URL", "sqlite:///:memory:")
is_sqlite = "sqlite" in DB_URL


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {} if is_sqlite else {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    event_uuid = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    __table_args__ = {} if is_sqlite else {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    event_uuid = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Merchant(Base):
    __tablename__ = "merchants"
    __table_args__ = {} if is_sqlite else {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    event_uuid = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow, nullable=False)
