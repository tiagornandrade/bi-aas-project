from sqlalchemy import Column, String, TIMESTAMP, BigInteger
from src.utils.db import Base
from datetime import datetime


class Entity(Base):
    __tablename__ = "entities"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    entity_id = Column(String)
    name = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawEntity(Base):
    __tablename__ = "raw_entities"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    entity_id = Column(String)
    name = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
