import os
from sqlalchemy.orm import Session
from src.utils.db import SessionLocal

QUERY_DIR = "queries"

def load_query(table: str, action: str) -> str:
    """Carrega um arquivo SQL baseado na tabela e ação (insert_incremental, upsert_full_load)."""
    file_path = os.path.join(QUERY_DIR, table, f"{action}.sql")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Query {action} para a tabela {table} não encontrada.")
    
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def execute_query(table: str, action: str, params: dict):
    """Executa uma query genérica para qualquer tabela."""
    db: Session = SessionLocal()
    try:
        query = load_query(table, action)
        db.execute(query, params)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()