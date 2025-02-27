from google.cloud import datastore
from datetime import datetime

db = datastore.Client()

KIND = "etl_jobs"


def create_status_record(table: str, job_type: str, start_time: str, end_time: str):
    """Cria um registro de status no Google Datastore com status 'queued'."""
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    doc_id = f"{table}_{job_type}_{timestamp}"

    task_key = db.key(KIND, doc_id)

    entity = datastore.Entity(key=task_key)
    entity.update(
        {
            "table": table,
            "type": job_type,
            "start_time": start_time,
            "end_time": end_time,
            "status": "queued",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
    )

    db.put(entity)
    return doc_id


def update_status(doc_id: str, status: str):
    """Atualiza o status de um job no Google Datastore."""
    task_key = db.key(KIND, doc_id)
    entity = db.get(task_key)

    if entity:
        entity["status"] = status
        entity["updated_at"] = datetime.utcnow().isoformat()
        db.put(entity)
    else:
        raise ValueError(f"Registro com ID {doc_id} não encontrado.")
