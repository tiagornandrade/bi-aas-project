import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DB_URL", "duckdb:///./database.duckdb")

engine = create_engine(DATABASE_URL, connect_args={"read_only": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
