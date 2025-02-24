from confluent_kafka import Producer
import json
import psycopg2
import re
import time

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:9092",
}

TOPIC_NAME = "wal_changes"
DLQ_TOPIC = "wal_changes_dlq"

producer = Producer(KAFKA_CONFIG)

WAL_PATTERN = re.compile(r"table public\.(\w+): (\w+): (.*)")


def delivery_report(err, msg):
    """Callback para confirmar entrega ao Kafka e enviar para DLQ em caso de erro."""
    if err:
        print(f"❌ Erro ao enviar mensagem para {msg.topic()}: {err}")
        dlq_message = json.loads(msg.value().decode("utf-8"))
        dlq_message["error"] = str(err)

        try:
            producer.produce(
                DLQ_TOPIC,
                value=json.dumps(dlq_message).encode("utf-8"),
                callback=lambda e, m: print(
                    f"📌 Evento enviado para DLQ: {m.value()}"
                    if not e
                    else f"⚠️ Erro ao enviar para DLQ: {e}"
                ),
            )
            producer.flush()
        except Exception as dlq_err:
            print(f"🚨 Falha ao enviar para DLQ: {dlq_err}")
    else:
        print(f"✅ Mensagem entregue para {msg.topic()} [{msg.partition()}]")


def capture_wal_changes():
    """Captura mudanças do WAL e envia para o Kafka"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM pg_logical_slot_get_changes('my_slot', NULL, NULL);"
            )
            changes = cur.fetchall()

            for change in changes:
                event = change[2]
                if match := WAL_PATTERN.search(event):
                    table_name, change_type, raw_values = match.groups()
                    columns = re.findall(r"(\w+)\[.*?\]:'?([^']+)'?", raw_values)
                    record = dict(columns)

                    message = json.dumps(
                        {"table": table_name, "type": change_type, "data": record}
                    )

                    try:
                        producer.produce(
                            TOPIC_NAME,
                            value=message.encode("utf-8"),
                            callback=delivery_report,
                        )
                        producer.flush()

                        print(f"🚀 Evento enviado para Kafka: {message}")
                    except Exception as e:
                        print(f"❌ Erro ao produzir evento: {e}")
                        dlq_message = {
                            "table": table_name,
                            "type": change_type,
                            "data": record,
                            "error": str(e),
                        }
                        try:
                            producer.produce(
                                DLQ_TOPIC,
                                value=json.dumps(dlq_message).encode("utf-8"),
                                callback=lambda err, msg: print(
                                    f"📌 Evento enviado para DLQ: {msg.value()}"
                                    if not err
                                    else f"⚠️ Erro ao enviar para DLQ: {err}"
                                ),
                            )
                            producer.flush()
                        except Exception as dlq_err:
                            print(f"🚨 Falha ao enviar para DLQ: {dlq_err}")

    time.sleep(1)
