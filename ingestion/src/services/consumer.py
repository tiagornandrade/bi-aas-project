from confluent_kafka import Consumer, KafkaException, Producer
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
DLQ_TOPIC = "wal_changes_dlq"

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


def process_event(conn, event):
    """Processa um evento do Kafka e insere no banco de dados."""
    try:
        table_name = event.get("table")
        event_type = event.get("type")
        record = event.get("data")

        if not table_name or not record:
            logging.warning(f"⚠️ Evento inválido recebido: {event}")
            return False

        if table_name not in RAW_TABLES:
            logging.warning(f"⚠️ Tabela {table_name} não está na RAW. Ignorando evento.")
            return False

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
            return True

    except json.JSONDecodeError as e:
        logging.error(f"🚨 Erro ao decodificar JSON: {e}")
    except psycopg2.Error as e:
        logging.error(f"❌ Erro no PostgreSQL: {e}")
        conn.rollback()
    return False


def consume_kafka_events():
    """Consome eventos do Kafka e grava na tabela correspondente da camada RAW"""

    conn = connect_to_postgres()
    producer = Producer(KAFKA_CONFIG)
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([TOPIC_NAME])

    logging.info("📥 Iniciando consumo de eventos do Kafka...")

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                logging.error(f"❌ Erro no Kafka: {msg.error()}")
                continue

            event = json.loads(msg.value().decode("utf-8"))

            if not process_event(conn, event):
                logging.warning(f"⚠️ Falha no processamento, enviando para DLQ...")
                event["error"] = "Erro ao processar evento"

                try:
                    producer.produce(
                        DLQ_TOPIC,
                        value=json.dumps(event).encode("utf-8"),
                        callback=lambda err, m: logging.info(
                            f"📌 Evento enviado para DLQ: {m.value()}"
                            if not err
                            else f"⚠️ Erro ao enviar para DLQ: {err}"
                        ),
                    )
                    producer.flush()
                except Exception as dlq_err:
                    logging.error(f"🚨 Falha ao enviar para DLQ: {dlq_err}")

    except KeyboardInterrupt:
        logging.info("🛑 Interrompendo consumo do Kafka...")

    finally:
        consumer.close()
        conn.close()
        logging.info("✅ Kafka e PostgreSQL fechados com sucesso.")


def consume_dlq_events():
    """Consome eventos da DLQ e tenta reprocessá-los."""
    conn = connect_to_postgres()
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([DLQ_TOPIC])

    logging.info("📥 Iniciando consumo da DLQ para reprocessamento...")

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                logging.error(f"❌ Erro no Kafka: {msg.error()}")
                continue

            event = json.loads(msg.value().decode("utf-8"))
            logging.info(f"🔄 Tentando reprocessar evento da DLQ: {event}")

            if process_event(conn, event):
                logging.info(f"✅ Evento reprocessado com sucesso: {event}")

    except KeyboardInterrupt:
        logging.info("🛑 Interrompendo consumo da DLQ...")

    finally:
        consumer.close()
        conn.close()
        logging.info("✅ DLQ Kafka e PostgreSQL fechados com sucesso.")


if __name__ == "__main__":
    import threading

    kafka_thread = threading.Thread(target=consume_kafka_events)
    dlq_thread = threading.Thread(target=consume_dlq_events)

    kafka_thread.start()
    dlq_thread.start()

    kafka_thread.join()
    dlq_thread.join()
