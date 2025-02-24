from sqlalchemy import Column, String, Integer, DateTime
from src.utils.db import Base
from datetime import datetime


class Policy(Base):
    __tablename__ = "policies"
    __table_args__ = {"schema": "public", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    policy_id = Column(String)
    type = Column(String)
    coverage_amount = Column(Integer)
    premium = Column(Integer)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Claim(Base):
    __tablename__ = "claims"
    __table_args__ = {"schema": "public", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_id = Column(String)
    policy_id = Column(String)
    amount_claimed = Column(Integer)
    status = Column(String)
    filed_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class InsuredEntity(Base):
    __tablename__ = "insured_entities"
    __table_args__ = {"schema": "public", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String)
    type = Column(String)
    description = Column(String)
    value = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawPolicy(Base):
    __tablename__ = "policies"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    policy_id = Column(String)
    type = Column(String)
    coverage_amount = Column(Integer)
    premium = Column(Integer)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawClaim(Base):
    __tablename__ = "claims"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_id = Column(String)
    policy_id = Column(String)
    amount_claimed = Column(Integer)
    status = Column(String)
    filed_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawInsuredEntity(Base):
    __tablename__ = "insured_entities"
    __table_args__ = {"schema": "raw", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(String)
    type = Column(String)
    description = Column(String)
    value = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
