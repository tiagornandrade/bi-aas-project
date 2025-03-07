import logging
from google.cloud import pubsub_v1
import json
import psycopg2
import re
import time
from src.db.connection import get_db_connection
from config.settings import PROJECT_ID, DLQ_TOPIC

logger = logging.getLogger(__name__)

publisher = pubsub_v1.PublisherClient()
dlq_topic_path = publisher.topic_path(PROJECT_ID, DLQ_TOPIC)

WAL_PATTERN = re.compile(r"table public\.(\w+): (\w+): (.*)")


def get_topic_path(table_name):
    """Gera o nome do tópico do Pub/Sub baseado na tabela"""
    return publisher.topic_path(PROJECT_ID, f"wal_changes_{table_name}")


def publish_message(topic, data):
    """Publica uma mensagem no Pub/Sub"""
    try:
        message = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic, message)
        future.result()
        logger.info(f"📤 Mensagem enviada para {topic}: {data}")
        return True
    except Exception as e:
        logger.error(f"❌ Falha ao enviar mensagem para {topic}: {e}")
        return False


def capture_wal_changes():
    """Captura mudanças do WAL e envia para o Pub/Sub"""
    logger.info("🔄 Iniciando captura de mudanças do WAL...")

    while True:
        conn = None
        try:
            conn = get_db_connection()
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

                        message_data = {
                            "table": table_name,
                            "type": change_type,
                            "data": record,
                        }

                        topic_path = get_topic_path(table_name)

                        if not publish_message(topic_path, message_data):
                            logger.warning(
                                "⚠️ Falha ao publicar no Pub/Sub, enviando para DLQ..."
                            )
                            message_data["error"] = "Falha ao publicar no Pub/Sub"
                            publish_message(dlq_topic_path, message_data)

                logger.info(
                    "✅ Captura de mudanças do WAL finalizada. Aguardando próximo ciclo..."
                )

        except psycopg2.Error as e:
            logger.error(f"❌ Erro ao conectar ou executar query no PostgreSQL: {e}")

        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")

        finally:
            if conn:
                conn.close()
                logger.info("🔄 Conexão com PostgreSQL fechada.")

        time.sleep(5)
