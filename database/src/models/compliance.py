from sqlalchemy import Column, String, TIMESTAMP, BigInteger
from src.utils.db import Base
from datetime import datetime


class Regulation(Base):
    __tablename__ = "regulations"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    regulation_id = Column(String)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    jurisdiction = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class UserVerification(Base):
    __tablename__ = "user_verifications"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    verification_id = Column(String)
    user_id = Column(String)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date = Column(TIMESTAMP, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawRegulation(Base):
    __tablename__ = "raw_regulations"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    regulation_id = Column(String)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    jurisdiction = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class RawUserVerification(Base):
    __tablename__ = "raw_user_verifications"

    id = Column(BigInteger, primary_key=True, server_default="AUTOINCREMENT")
    verification_id = Column(String)
    user_id = Column(String)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date = Column(TIMESTAMP, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)