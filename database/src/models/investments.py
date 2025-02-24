from sqlalchemy import Column, String, Integer, DateTime
from src.utils.db import Base
from datetime import datetime


class Portfolio(Base):
    __tablename__ = "portfolios"
    __table_args__ = {"schema": "public"}
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = Column(String)
    user_id = Column(String)
    total_value = Column(Integer)
    risk_profile = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawPortfolio(Base):
    __tablename__ = "portfolios"
    __table_args__ = {"schema": "raw"}
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = Column(String)
    user_id = Column(String)
    total_value = Column(Integer)
    risk_profile = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
