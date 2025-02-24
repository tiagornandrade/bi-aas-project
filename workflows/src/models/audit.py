from sqlalchemy import Column, String, DateTime, Integer
from src.utils.db import Base
from datetime import timezone
from datetime import datetime


class Audit(Base):
    __tablename__ = "audits"
    __table_args__ = {"schema": "public"}
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    audit_id = Column(String, unique=True, nullable=False)
    entity_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    findings = Column(String, nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
