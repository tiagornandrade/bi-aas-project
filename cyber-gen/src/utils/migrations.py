import os
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    DateTime,
    JSON,
    TIMESTAMP,
    Text,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DB_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

tables = [
    "accounts",
    "audits",
    "claims",
    "credit_scores",
    "entities",
    "insured_entities",
    "loans",
    "merchants",
    "payment_methods",
    "payments",
    "policies",
    "portfolios",
    "regulations",
    "risk_assessments",
    "subaccounts",
    "transactions",
    "user_verifications",
    "users",
]


class AuditLogChanges(Base):
    __tablename__ = "changes"
    __table_args__ = {"schema": "audit_log"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String)
    change_type = Column(String)
    record = Column(JSON)
    captured_at = Column(TIMESTAMP, default=datetime.utcnow)


for table_name in tables:
    class_attrs = {
        "__tablename__": table_name,
        "__table_args__": {"schema": "raw"},
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "table_name": Column(String, nullable=False),
        "event_uuid": Column(String, nullable=False),
        "event_type": Column(String, nullable=False),
        "event_timestamp": Column(TIMESTAMP, nullable=False),
        "payload": Column(JSON, nullable=False),
        "ingested_at": Column(TIMESTAMP, default=datetime.utcnow, nullable=False),
    }

    table_class = type(table_name.capitalize(), (Base,), class_attrs)
    globals()[table_name.capitalize()] = table_class


class DlqEvents(Base):
    __tablename__ = "dlq_events"
    __table_args__ = {"schema": "raw"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    event_uuid = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    event_timestamp = Column(TIMESTAMP, nullable=False)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    error_message = Column(Text)


Base.metadata.create_all(engine)

print("Tabelas criadas com sucesso!")
