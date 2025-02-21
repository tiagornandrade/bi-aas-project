import os
from dotenv import load_dotenv

load_dotenv()


DB_SECRETS = {
    "dbname": os.getenv("DBNAME", "postgres"),
    "user": os.getenv("USER", "postgres"),
    "password": os.getenv("PASSWORD", "postgres"),
    "host": os.getenv("HOST", "localhost"),
    "port": os.getenv("PORT", "5432"),
}

KAFKA_CONFIG_PRODUCER = {
    "bootstrap.servers": os.getenv("BOOTSTRAP", "localhost:9092"),
}

KAFKA_CONFIG_CONSUMER = {
    "bootstrap.servers": os.getenv("BOOTSTRAP", "localhost:9092"),
    "group.id": os.getenv("GROUP_ID", "wal_group"),
    "auto.offset.reset": os.getenv("OFFSET_RESET", "earliest"),
}

TOPIC_NAME_CONSUMER = os.getenv("TOPIC_CONSUMER", "wal_topic")

TOPIC_NAME_PRODUCER = os.getenv("TOPIC_PRODUCER", "wal_changes")
