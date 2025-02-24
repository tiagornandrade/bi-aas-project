from sqlalchemy import Column, String, Integer, DateTime
from src.utils.db import Base
from datetime import datetime


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "public", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String)
    amount = Column(Integer)
    currency = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender_id = Column(String)
    receiver_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    __table_args__ = {"schema": "public", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    method_id = Column(String)
    type = Column(String)
    details = Column(String)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Merchant(Base):
    __tablename__ = "merchants"
    __table_args__ = {"schema": "public", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    merchant_id = Column(String)
    name = Column(String)
    category = Column(String)
    contact_info = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawTransaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String)
    amount = Column(Integer)
    currency = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender_id = Column(String)
    receiver_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawPaymentMethod(Base):
    __tablename__ = "payment_methods"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    method_id = Column(String)
    type = Column(String)
    details = Column(String)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawMerchant(Base):
    __tablename__ = "merchants"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    merchant_id = Column(String)
    name = Column(String)
    category = Column(String)
    contact_info = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
