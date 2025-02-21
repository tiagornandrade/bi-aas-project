from confluent_kafka import Consumer, KafkaException
from datetime import datetime
import uuid
import json
import psycopg2
import psycopg2.extras
import logging
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "wal_group",
    "auto.offset.reset": "earliest",
}
TOPIC_NAME = "wal_changes"

RAW_TABLES = {
    "accounts",
    "audits",
    "claims",
    "credit_scores",
    "entities",
    "insured_entities",
    "loans",
    "merchants",
    "payment_methods",
    "payments",
    "policies",
    "portfolios",
    "regulations",
    "risk_assessments",
    "subaccounts",
    "transactions",
    "user_verifications",
    "users",
}


def connect_to_postgres():
    """Tenta conectar ao PostgreSQL e retorna a conexão"""
    for attempt in range(5):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.autocommit = True
            logging.info("✅ Conectado ao PostgreSQL.")
            return conn
        except psycopg2.Error as e:
            logging.error(
                f"🚨 Erro ao conectar ao PostgreSQL (tentativa {attempt + 1}/5): {e}"
            )
            time.sleep(1)
    raise Exception("❌ Falha ao conectar ao PostgreSQL após múltiplas tentativas.")


def consume_kafka_events():
    """Consome eventos do Kafka e grava na tabela correspondente da camada RAW"""

    conn = connect_to_postgres()

    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([TOPIC_NAME])

    logging.info("📥 Iniciando consumo de eventos do Kafka...")

    try:
        while True:
            try:
                msg = consumer.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    logging.error(f"❌ Erro no Kafka: {msg.error()}")
                    continue

                event = json.loads(msg.value().decode("utf-8"))
                table_name = event.get("table")
                event_type = event.get("type")
                record = event.get("data")

                if not table_name or not record:
                    logging.warning(f"⚠️ Evento inválido recebido: {event}")
                    continue

                if table_name not in RAW_TABLES:
                    logging.warning(
                        f"⚠️ Tabela {table_name} não está na RAW. Ignorando evento."
                    )
                    continue

                event_uuid = str(uuid.uuid4())
                event_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

                with conn.cursor() as cur:
                    sql = f"""
                        INSERT INTO raw.{table_name} (table_name, event_uuid, event_type, event_timestamp, payload, ingested_at)
                        VALUES (%s, %s, %s, %s, %s::jsonb, CURRENT_TIMESTAMP);
                    """
                    cur.execute(
                        sql,
                        (
                            table_name,
                            event_uuid,
                            event_type,
                            event_timestamp,
                            json.dumps(record),
                        ),
                    )
                    logging.info(f"✅ Evento inserido em raw.{table_name}: {event}")

            except json.JSONDecodeError as e:
                logging.error(f"🚨 Erro ao decodificar JSON: {e}")
            except psycopg2.Error as e:
                logging.error(f"❌ Erro no PostgreSQL: {e}")
                conn.rollback()
            except KafkaException as e:
                logging.error(f"🚨 Erro no Kafka: {e}")

    except KeyboardInterrupt:
        logging.info("🛑 Interrompendo consumo do Kafka...")

    finally:
        consumer.close()
        conn.close()
        logging.info("✅ Kafka e PostgreSQL fechados com sucesso.")


if __name__ == "__main__":
    consume_kafka_events()
