from sqlalchemy import Column, String, Integer, TIMESTAMP, BigInteger
from utils.db import Base
from datetime import datetime


class Account(Base):
    __tablename__ = "accounts"
<<<<<<< Updated upstream
    __table_args__ = {"extend_existing": True}
=======
>>>>>>> Stashed changes

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    account_id = Column(String)
    account_type = Column(String)
    balance = Column(Integer)
    currency = Column(String)
    status = Column(String)
    user_id = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Subaccount(Base):
    __tablename__ = "subaccounts"
<<<<<<< Updated upstream
    __table_args__ = {"extend_existing": True}
=======
>>>>>>> Stashed changes

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    subaccount_id = Column(String)
    parent_account_id = Column(String)
    purpose = Column(String)
    balance = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"
<<<<<<< Updated upstream
    __table_args__ = {"extend_existing": True}
=======

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    user_id = Column(String)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawAccount(Base):
    __tablename__ = "raw_accounts"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    account_id = Column(String)
    account_type = Column(String)
    balance = Column(Integer)
    currency = Column(String)
    status = Column(String)
    user_id = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawSubaccount(Base):
    __tablename__ = "raw_subaccounts"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    subaccount_id = Column(String)
    parent_account_id = Column(String)
    purpose = Column(String)
    balance = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawUser(Base):
    __tablename__ = "raw_users"
>>>>>>> Stashed changes

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    user_id = Column(String)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
