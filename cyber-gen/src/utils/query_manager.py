import os
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from src.utils.db import SessionLocal


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUERY_DIR = os.path.join(BASE_DIR, "..", "queries")


def load_query(layer: str, table: str) -> str:
    """Carrega um arquivo SQL baseado na camada (bronze, silver, gold) e na tabela."""
    file_path = os.path.join(QUERY_DIR, layer, f"{table}.sql")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Query para '{table}' na camada '{layer}' não encontrada: {file_path}"
        )

    with open(file_path, encoding="utf-8") as file:
        return file.read()


def execute_query(layer: str, table: str, params: dict):
    """Executa uma query genérica para qualquer camada e tabela."""
    query_str = load_query(layer, table)
    query = text(query_str)

    with SessionLocal() as db:
        try:
            db.execute(query, params)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
