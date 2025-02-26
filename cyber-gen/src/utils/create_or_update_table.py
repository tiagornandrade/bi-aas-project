import os
import re
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL", "postgresql://user:password@localhost:5432/dbname")


def parse_db_url(db_url):
    """Converte a string de conexão do banco para um dicionário de parâmetros do psycopg2."""
    result = urlparse(db_url)
    return {
        "dbname": result.path.lstrip("/"),
        "user": result.username,
        "password": result.password,
        "host": result.hostname,
        "port": result.port,
    }


DB_CONFIG = parse_db_url(DATABASE_URL)
SQL_FILE_PATH = "src/queries/bronze/accounts_deleted.sql"


def read_sql_query(file_path):
    """Lê a query de um arquivo SQL e retorna apenas a parte do SELECT."""
    with open(file_path, encoding="utf-8") as file:
        sql_query = file.read().strip()

    if "SELECT" not in sql_query.upper():
        raise ValueError("A query SQL não contém um comando SELECT válido.")

    select_part = sql_query.split("SELECT", 1)[1]
    select_query = f"SELECT {select_part}".strip()

    if select_query.endswith(";"):
        select_query = select_query[:-1]

    return select_query


def extract_column_types(query):
    """Extrai os nomes das colunas e seus tipos a partir da query SQL."""
    type_mapping = {
        "NUMERIC": "NUMERIC",
        "UUID": "UUID",
        "TEXT": "TEXT",
        "VARCHAR": "TEXT",
        "INTEGER": "INTEGER",
        "BIGINT": "BIGINT",
        "REAL": "REAL",
        "DOUBLE PRECISION": "DOUBLE PRECISION",
        "BOOLEAN": "BOOLEAN",
        "JSONB": "JSONB",
        "DATE": "DATE",
        "TIMESTAMP": "TIMESTAMP",
        "TIMESTAMPTZ": "TIMESTAMPTZ",
    }

    columns = {}

    matches = re.findall(r"\((.*?)\)::(\w+)", query)

    for match in matches:
        col_name, col_type = match
        col_name = col_name.strip().replace("payload ->> '", "").replace("'", "")
        sql_type = type_mapping.get(col_type.upper(), "TEXT")
        columns[col_name] = sql_type

    return columns


def get_existing_columns(schema: str, table: str):
    """Obtém as colunas existentes no banco de dados para a tabela informada."""
    query = f"""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = '{schema}' AND table_name = '{table}';
    """

    try:
        return _extracted_from_get_existing_columns_10(query)
    except Exception as e:
        print(f"⚠️ Erro ao buscar colunas existentes: {e}")
        return {}


def _extracted_from_get_existing_columns_10(query):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(query)
    existing_columns = {row[0]: row[1] for row in cur.fetchall()}
    cur.close()
    conn.close()
    return existing_columns


def generate_create_table(schema: str, table: str, columns: dict):
    """Gera um comando CREATE TABLE baseado nos tipos de dados detectados."""

    cols_definitions = [
        f"{col_name} {col_type}" for col_name, col_type in columns.items()
    ]

    return f"""
    CREATE TABLE IF NOT EXISTS {schema}.{table} (
        id SERIAL PRIMARY KEY,
        {", ".join(cols_definitions)}
    );
    """


def generate_alter_table(
    schema: str, table: str, new_columns: dict, existing_columns: dict
):
    """Gera comandos ALTER TABLE para adicionar colunas novas, se necessário."""
    alter_statements = []
    alter_statements.extend(
        f"ADD COLUMN {col_name} {col_type}"
        for col_name, col_type in new_columns.items()
        if col_name not in existing_columns
    )
    if alter_statements:
        return f"ALTER TABLE {schema}.{table} {', '.join(alter_statements)};"
    return None


def execute_ddl(ddl_statements):
    """Executa comandos DDL no banco de dados."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for ddl in ddl_statements:
            if ddl:
                cur.execute(ddl)
        conn.commit()
        print("✅ Estrutura da tabela atualizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao atualizar a estrutura da tabela: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    query = read_sql_query(SQL_FILE_PATH)
    new_columns = extract_column_types(query)
    if existing_columns := get_existing_columns("bronze", "accounts_deleted"):
        print("🔄 Comparando estrutura da tabela...")
        if alter_sql := generate_alter_table(
            "bronze", "accounts_deleted", new_columns, existing_columns
        ):
            print(f"📜 Executando ALTER TABLE:\n{alter_sql}")
            execute_ddl([alter_sql])
        else:
            print("✅ Nenhuma alteração necessária, a tabela já está atualizada.")
    else:
        print("📜 Criando nova tabela...")
        create_sql = generate_create_table("bronze", "accounts_deleted", new_columns)
        execute_ddl([create_sql])
