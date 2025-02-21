from sqlalchemy import Column, String, Integer, TIMESTAMP, BigInteger
from src.utils.db import Base
from datetime import datetime


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    portfolio_id = Column(String)
    user_id = Column(String)
    total_value = Column(Integer)
    risk_profile = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawPortfolio(Base):
    __tablename__ = "raw_portfolios"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    portfolio_id = Column(String)
    user_id = Column(String)
    total_value = Column(Integer)
    risk_profile = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)