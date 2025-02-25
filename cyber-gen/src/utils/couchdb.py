import os
import couchdb
from datetime import datetime

COUCHDB_URL = os.getenv("COUCHDB_URL", "http://admin:password@localhost:5984")
COUCHDB_DBNAME = "etl_jobs"

server = couchdb.Server(COUCHDB_URL)
if COUCHDB_DBNAME not in server:
    db = server.create(COUCHDB_DBNAME)
else:
    db = server[COUCHDB_DBNAME]


def create_status_record(table: str, job_type: str, start_time: str, end_time: str):
    """Cria um registro de status como 'queued' no CouchDB, com um ID único baseado na tabela e tipo de carga."""
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    doc_id = f"{table}_{job_type}_{timestamp}"

    doc = {
        "_id": doc_id,
        "table": table,
        "type": job_type,
        "start_time": start_time,
        "end_time": end_time,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    db.save(doc)
    return doc_id


def update_status(doc_id: str, status: str):
    """Atualiza o status de um job no CouchDB."""
    if doc_id in db:
        doc = db[doc_id]
        doc["status"] = status
        doc["updated_at"] = datetime.utcnow().isoformat()
        db.save(doc)
