from datetime import timezone
from sqlalchemy import Column, String, TIMESTAMP, BigInteger
from src.utils.db import Base
from datetime import datetime


class Audit(Base):
    __tablename__ = "audits"
<<<<<<< Updated upstream
    __table_args__ = {"extend_existing": True}
=======

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    audit_id = Column(String, unique=True, nullable=False)
    entity_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    findings = Column(String, nullable=False)
    date = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawAudit(Base):
    __tablename__ = "raw_audits"
>>>>>>> Stashed changes

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    audit_id = Column(String, unique=True, nullable=False)
    entity_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    findings = Column(String, nullable=False)
    date = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
