import psycopg2
from config.settings import DB_CONFIG


def get_db_connection():
    """Retorna uma conexão ativa com o banco de dados."""
    return psycopg2.connect(**DB_CONFIG)
