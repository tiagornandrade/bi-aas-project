from src.utils.db import Base
from sqlalchemy import Column, String, Integer


class Entity(Base):
    __tablename__ = "entities"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String)
    name = Column(String)
