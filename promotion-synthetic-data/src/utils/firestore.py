from google.cloud import datastore
from datetime import datetime, timezone

KIND = "etl_jobs"


class DatastoreClient:
    """Gerencia a conexão com o Google Datastore."""

    def __init__(self):
        self.client = datastore.Client()

    def _current_timestamp(self) -> tuple[str, str]:
        """Gera timestamps padronizados para evitar duplicação de código."""
        now = datetime.now(timezone.utc)
        return now.strftime("%Y%m%dT%H%M%S"), now.isoformat()

    def create_status_record(
        self, table: str, job_type: str, start_time: str, end_time: str
    ) -> str:
        """Cria um registro de status no Google Datastore com status 'queued'."""
        timestamp, now_iso = self._current_timestamp()
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
                "created_at": now_iso,
                "updated_at": now_iso,
            }
        )

        self.client.put(entity)
        return doc_id

    def update_status(self, doc_id: str, status: str):
        """Atualiza o status de um job no Google Datastore."""
        key = self.client.key(KIND, doc_id)
        if entity := self.client.get(key):
            _, now_iso = self._current_timestamp()
            entity.update({"status": status, "updated_at": now_iso})
            self.client.put(entity)
            return
        raise ValueError(f"Registro com ID {doc_id} não encontrado.")


def get_datastore_client() -> DatastoreClient:
    """Fornece uma instância do DatastoreClient."""
    return DatastoreClient()
