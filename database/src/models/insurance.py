from sqlalchemy import Column, String, Integer, TIMESTAMP, BigInteger
from src.utils.db import Base
from datetime import datetime


class Policy(Base):
    __tablename__ = "policies"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    policy_id = Column(String)
    type = Column(String)
    coverage_amount = Column(Integer)
    premium = Column(Integer)
    start_date = Column(TIMESTAMP, default=datetime.utcnow)
    end_date = Column(TIMESTAMP, default=datetime.utcnow)
    user_id = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Claim(Base):
    __tablename__ = "claims"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    claim_id = Column(String)
    policy_id = Column(String)
    amount_claimed = Column(Integer)
    status = Column(String)
    filed_date = Column(TIMESTAMP, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class InsuredEntity(Base):
    __tablename__ = "insured_entities"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    entity_id = Column(String)
    type = Column(String)
    description = Column(String)
    value = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawPolicy(Base):
    __tablename__ = "raw_policies"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    policy_id = Column(String)
    type = Column(String)
    coverage_amount = Column(Integer)
    premium = Column(Integer)
    start_date = Column(TIMESTAMP, default=datetime.utcnow)
    end_date = Column(TIMESTAMP, default=datetime.utcnow)
    user_id = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawClaim(Base):
    __tablename__ = "raw_claims"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    claim_id = Column(String)
    policy_id = Column(String)
    amount_claimed = Column(Integer)
    status = Column(String)
    filed_date = Column(TIMESTAMP, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawInsuredEntity(Base):
    __tablename__ = "raw_insured_entities"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    entity_id = Column(String)
    type = Column(String)
    description = Column(String)
    value = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
