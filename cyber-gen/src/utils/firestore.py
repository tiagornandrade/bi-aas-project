from google.cloud import datastore
from datetime import datetime, timezone

KIND = "etl_jobs"


class DatastoreClient:
    """Gerencia a conexão com o Google Datastore."""

    def __init__(self):
        self.client = datastore.Client()

    def create_status_record(
        self, table: str, job_type: str, start_time: str, end_time: str
    ):
        """Cria um registro de status no Google Datastore com status 'queued'."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        doc_id = f"{table}_{job_type}_{timestamp}"

        task_key = self.client.key(KIND, doc_id)
        entity = datastore.Entity(key=task_key)

        entity.update(
            {
                "table": table,
                "type": job_type,
                "start_time": start_time,
                "end_time": end_time,
                "status": "queued",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        self.client.put(entity)
        return doc_id

    def update_status(self, doc_id: str, status: str):
        """Atualiza o status de um job no Google Datastore."""
        if entity := self.client.get(self.client.key(KIND, doc_id)):
            entity["status"] = status
            entity["updated_at"] = datetime.now(timezone.utc).isoformat()
            self.client.put(entity)
            return
        raise ValueError(f"Registro com ID {doc_id} não encontrado.")


def get_datastore_client():
    """Fornece uma instância do DatastoreClient."""
    return DatastoreClient()
