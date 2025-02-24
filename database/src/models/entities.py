from sqlalchemy import Column, String, Integer, DateTime
from src.utils.db import Base
from datetime import datetime


class Entity(Base):
    __tablename__ = "entities"
    __table_args__ = {"schema": "public"}
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawEntity(Base):
    __tablename__ = "entities"
    __table_args__ = {"schema": "raw"}
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
