import psycopg2
from psycopg2 import pool
import logging
from src.config.settings import DB_CONFIG

logger = logging.getLogger(__name__)

try:
    if connection_pool := pool.SimpleConnectionPool(minconn=1, maxconn=5, **DB_CONFIG):
        logging.info("✅ Pool de conexões criado com sucesso.")
except psycopg2.DatabaseError as e:
    logging.error(f"❌ Erro ao criar pool de conexões: {e}")
    raise


def get_db_connection():
    """Obtém uma conexão do pool."""
    try:
        conn = connection_pool.getconn()
        logging.info("🔄 Conexão obtida do pool.")
        return conn
    except psycopg2.DatabaseError as e:
        logging.error(f"🚨 Erro ao obter conexão do pool: {e}")
        raise


def release_db_connection(conn):
    """Libera uma conexão de volta ao pool."""
    try:
        connection_pool.putconn(conn)
        logging.info("✅ Conexão devolvida ao pool.")
    except psycopg2.DatabaseError as e:
        logging.error(f"⚠️ Erro ao devolver conexão ao pool: {e}")
