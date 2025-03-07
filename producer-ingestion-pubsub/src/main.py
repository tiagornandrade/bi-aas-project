import logging
import multiprocessing
import os
from fastapi import FastAPI

from src.services.producer import capture_wal_changes
from src.services.consumer import consume_pubsub_events

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()


@app.get("/")
def health_check():
    """Health Check para Cloud Run"""
    return {"status": "OK"}


def start_producer():
    """Inicia o producer para capturar mudanças do WAL e enviar para Pub/Sub"""
    logging.info("🚀 Iniciando o Producer (WAL -> Pub/Sub)...")
    capture_wal_changes()


def start_consumer():
    """Inicia o consumer para consumir eventos do Pub/Sub e escrever no BigQuery"""
    logging.info("📥 Iniciando o Consumer (Pub/Sub -> BigQuery)...")
    consume_pubsub_events()


if __name__ == "__main__":
    producer_process = multiprocessing.Process(target=start_producer, daemon=True)
    consumer_process = multiprocessing.Process(target=start_consumer, daemon=True)

    producer_process.start()
    consumer_process.start()

    port = int(os.getenv("PORT", 8080))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
