import multiprocessing
from src.services.producer import capture_wal_changes
from src.services.consumer import consume_kafka_events


def start_producer():
    """Inicia o producer para capturar mudanças do WAL e enviar para Kafka"""
    print("🚀 Iniciando o Producer (WAL -> Kafka)...")
    while True:
        capture_wal_changes()


def start_consumer():
    """Inicia o consumer para consumir eventos do Kafka e escrever na RAW"""
    print("📥 Iniciando o Consumer (Kafka -> RAW)...")
    consume_kafka_events()


if __name__ == "__main__":
    producer_process = multiprocessing.Process(target=start_producer)
    consumer_process = multiprocessing.Process(target=start_consumer)

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()
