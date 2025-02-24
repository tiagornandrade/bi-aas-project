from sqlalchemy import Column, String, Integer, DateTime, JSON
from datetime import datetime
from src.utils.db import Base


class RawDLQEvents(Base):
    __tablename__ = "dlq_events"
    __table_args__ = {"schema": "raw"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    event_uuid = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow, nullable=False)
