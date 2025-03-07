import os
from dotenv import load_dotenv
import yaml

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DBNAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "meu-projeto")
TOPIC_NAME = os.getenv("PUBSUB_TOPIC", "wal-changes")
SUBSCRIPTION_NAME = os.getenv("PUBSUB_SUBSCRIPTION", "wal-changes-sub")

DLQ_TOPIC = os.getenv("PUBSUB_DLQ_TOPIC", "wal-changes-dlq")
DLQ_SUBSCRIPTION_NAME = os.getenv("PUBSUB_DLQ_SUBSCRIPTION", "wal-changes-dlq-sub")

RAW_TABLES_FILE = os.path.join(os.path.dirname(__file__), "tables.yaml")

BQ_DATASET = "cdc_postgres"
BQ_TABLE = "events"

TOPIC_PREFIX = "wal_changes"
DLQ_TOPIC = f"{TOPIC_PREFIX}_dlq"

with open(RAW_TABLES_FILE) as file:
    RAW_TABLES = set(yaml.safe_load(file)["raw_tables"])
    print(f"📚 Tabelas RAW carregadas: {RAW_TABLES}")
