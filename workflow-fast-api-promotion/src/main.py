from datetime import timezone
from fastapi import FastAPI, HTTPException, Query
from src.utils.query_manager import execute_query
from src.utils.couchdb import create_status_record, update_status, db
from datetime import datetime, timedelta

app = FastAPI()


@app.post("/{table}/load_incremental")
def load_incremental(table: str, start_time: str = None, end_time: str = None):
    """Executa uma carga incremental e registra seu status no CouchDB."""
    try:
        if not start_time:
            start_time = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        if not end_time:
            end_time = datetime.now(timezone.utc).isoformat()

        doc_id = create_status_record(table, "incremental", start_time, end_time)

        update_status(doc_id, "running")

        params = {"start_time": start_time, "end_time": end_time}
        execute_query(table, "insert_incremental", params)

        update_status(doc_id, "success")
        return {"status": "Carga incremental concluída", "job_id": doc_id}

    except FileNotFoundError as e:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=404, detail="Query não encontrada") from e

    except Exception as e:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/{table}/load_full")
def load_full(
    table: str,
    start_time: str = Query(
        None, description="Data de início (ISO 8601, ex: 2024-01-01T00:00:00)"
    ),
    end_time: str = Query(
        None, description="Data de fim (ISO 8601, ex: 2024-01-31T23:59:59)"
    ),
):
    """Executa uma carga full (UPSERT) e registra seu status no CouchDB."""
    try:
        if not start_time:
            start_time = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        if not end_time:
            end_time = datetime.now(timezone.utc).isoformat()

        doc_id = create_status_record(table, "full", start_time, end_time)

        update_status(doc_id, "running")

        params = {"start_time": start_time, "end_time": end_time}
        execute_query(table, "upsert_full_load", params)

        update_status(doc_id, "success")
        return {
            "status": "Carga full concluída",
            "start_time": start_time,
            "end_time": end_time,
            "job_id": doc_id,
        }

    except FileNotFoundError as e:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=404, detail="Query não encontrada") from e

    except Exception as e:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/status/{job_id}")
def get_status(job_id: str):
    """Retorna o status de um job pelo ID."""
    try:
        if job_id in db:
            return db[job_id]
        else:
            raise HTTPException(status_code=404, detail="Job não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
