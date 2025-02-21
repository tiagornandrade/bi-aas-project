from sqlalchemy import Column, String, Integer, TIMESTAMP, BigInteger
from src.utils.db import Base
from datetime import datetime


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    transaction_id = Column(String)
    amount = Column(Integer)
    currency = Column(String)
    status = Column(String)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    sender_id = Column(String)
    receiver_id = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    method_id = Column(String)
    type = Column(String)
    details = Column(String)
    user_id = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    merchant_id = Column(String)
    name = Column(String)
    category = Column(String)
    contact_info = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawTransaction(Base):
    __tablename__ = "raw_transactions"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    transaction_id = Column(String)
    amount = Column(Integer)
    currency = Column(String)
    status = Column(String)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    sender_id = Column(String)
    receiver_id = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawPaymentMethod(Base):
    __tablename__ = "raw_payment_methods"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    method_id = Column(String)
    type = Column(String)
    details = Column(String)
    user_id = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawMerchant(Base):
    __tablename__ = "raw_merchants"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    merchant_id = Column(String)
    name = Column(String)
    category = Column(String)
    contact_info = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
