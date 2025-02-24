from sqlalchemy import Column, String, Integer, DateTime
from src.utils.db import Base
from datetime import datetime


class RawAccount(Base):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String)
    account_type = Column(String)
    balance = Column(Integer)
    currency = Column(String)
    status = Column(String)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawSubaccount(Base):
    __tablename__ = "subaccounts"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    subaccount_id = Column(String)
    parent_account_id = Column(String)
    purpose = Column(String)
    balance = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawUser(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
