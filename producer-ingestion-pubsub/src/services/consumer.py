import logging
import json
import uuid
import time
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

from google.cloud import pubsub_v1, bigquery
from config.settings import PROJECT_ID, RAW_TABLES, BQ_DATASET, TOPIC_PREFIX, DLQ_TOPIC

logger = logging.getLogger(__name__)

subscriber = pubsub_v1.SubscriberClient()
bq_client = bigquery.Client(project=PROJECT_ID)


def get_subscription_path(table_name):
    """Retorna o caminho da assinatura do Pub/Sub para cada tabela"""
    return subscriber.subscription_path(PROJECT_ID, f"{TOPIC_PREFIX}_{table_name}")


def get_table_id(table_name):
    """Retorna o ID da tabela no BigQuery"""
    return f"{PROJECT_ID}.{BQ_DATASET}.{table_name}"


def process_event(event):
    """Processa um evento do Pub/Sub e insere no BigQuery."""
    try:
        table_name = event.get("table")
        event_type = event.get("type")
        record = event.get("data")

        if not table_name or not record:
            logger.warning(f"⚠️ Evento inválido recebido: {event}")
            return False

        if table_name not in RAW_TABLES:
            logger.warning(f"⚠️ Tabela {table_name} não está na RAW. Ignorando evento.")
            return False

        event_uuid = str(uuid.uuid4())
        event_timestamp = datetime.now(timezone.utc).isoformat()

        table_id = get_table_id(table_name)

        rows_to_insert = [
            {
                "event_uuid": event_uuid,
                "event_type": event_type,
                "event_timestamp": event_timestamp,
                "payload": json.dumps(record),
                "ingested_at": event_timestamp,
            }
        ]

        if errors := bq_client.insert_rows_json(table_id, rows_to_insert):
            logger.error(f"❌ Erros ao inserir no BigQuery ({table_id}): {errors}")
            return False

        logger.info(f"✅ Evento inserido no BigQuery ({table_id}): {event}")
        return True

    except Exception as e:
        logger.error(f"❌ Erro ao processar evento no BigQuery: {e}")
        return False


def callback(message):
    """Callback para processar mensagens do Pub/Sub"""
    try:
        event = json.loads(message.data.decode("utf-8"))

        if not process_event(event):
            logger.warning("⚠️ Falha no processamento, enviando para DLQ...")
            send_to_dlq(event)
        message.ack()
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao processar mensagem: {e}")
        message.ack()


def send_to_dlq(event):
    """Envia eventos com erro para a Dead Letter Queue (DLQ)"""
    try:
        publisher = pubsub_v1.PublisherClient()
        dlq_topic_path = publisher.topic_path(PROJECT_ID, DLQ_TOPIC)

        event["error"] = "Falha ao processar evento"
        message = json.dumps(event).encode("utf-8")

        future = publisher.publish(dlq_topic_path, message)
        future.result()
        logger.info(f"📤 Evento enviado para DLQ: {event}")

    except Exception as e:
        logger.error(f"🚨 Falha ao enviar para DLQ: {e}")


def consume_pubsub_events():
    """Inicia o consumo de mensagens do Pub/Sub de múltiplas tabelas"""
    logger.info("📥 Iniciando consumo de mensagens do Pub/Sub...")

    with ThreadPoolExecutor(max_workers=len(RAW_TABLES)) as executor:
        for table_name in RAW_TABLES:
            subscription_path = get_subscription_path(table_name)
            executor.submit(subscriber.subscribe, subscription_path, callback)

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("🛑 Interrompendo consumo de mensagens do Pub/Sub...")
