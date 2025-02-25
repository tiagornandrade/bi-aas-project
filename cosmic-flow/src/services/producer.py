from confluent_kafka import Producer, KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
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
admin_client = AdminClient(KAFKA_CONFIG)

WAL_PATTERN = re.compile(r"table public\.(\w+): (\w+): (.*)")


def create_topics(topics):
    """Cria os tópicos no Kafka se ainda não existirem."""
    existing_topics = admin_client.list_topics(timeout=5).topics.keys()
    new_topics = [
        NewTopic(topic, num_partitions=3, replication_factor=1)
        for topic in topics
        if topic not in existing_topics
    ]

    if new_topics:
        print(f"📌 Criando tópicos: {', '.join(t.name for t in new_topics)}")
        future_map = admin_client.create_topics(new_topics)

        for topic, future in future_map.items():
            try:
                future.result()
                print(f"✅ Tópico '{topic}' criado com sucesso!")
            except KafkaException as e:
                if e.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                    print(f"⚠️ Tópico '{topic}' já existe.")
                else:
                    print(f"❌ Erro ao criar tópico '{topic}': {e}")


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

                    topic_name = f"wal_changes_{table_name}"

                    message = json.dumps(
                        {"table": table_name, "type": change_type, "data": record}
                    )

                    try:
                        producer.produce(
                            topic_name,
                            value=message.encode("utf-8"),
                            callback=delivery_report,
                        )
                        producer.flush()

                        print(f"🚀 Evento enviado para Kafka ({topic_name}): {message}")
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


if __name__ == "__main__":
    create_topics([TOPIC_NAME, DLQ_TOPIC])
    capture_wal_changes()
