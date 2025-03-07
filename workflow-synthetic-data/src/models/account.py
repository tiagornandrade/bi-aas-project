from sqlalchemy import Column, String, Integer, DateTime
from src.utils.db import Base
from datetime import datetime


class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "public"}
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String)
    account_type = Column(String)
    balance = Column(Integer)
    currency = Column(String)
    status = Column(String)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Subaccount(Base):
    __tablename__ = "subaccounts"
    __table_args__ = {"schema": "public"}
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    subaccount_id = Column(String)
    parent_account_id = Column(String, nullable=False)
    purpose = Column(String)
    balance = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
