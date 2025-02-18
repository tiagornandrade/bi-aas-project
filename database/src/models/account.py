from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from utils.db import Base
from datetime import datetime


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(String, primary_key=True, index=True)
    account_type = Column(String)
    balance = Column(Integer)
    currency = Column(String)
    status = Column(String)
    user_id = Column(String, ForeignKey("users.user_id"))


class Subaccount(Base):
    __tablename__ = "subaccounts"

    subaccount_id = Column(String, primary_key=True, index=True)
    parent_account_id = Column(String, ForeignKey("accounts.account_id"))
    purpose = Column(String)
    balance = Column(Integer)


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
