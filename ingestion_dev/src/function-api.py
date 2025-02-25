from fastapi import FastAPI, HTTPException, Query
from src.utils.query_manager import execute_query
from src.utils.couchdb import create_status_record, update_status, db
from datetime import datetime, timedelta

app = FastAPI()


@app.post("/bronze/{table}/incremental")
def load_incremental_bronze(table: str, start_time: str = None, end_time: str = None):
    """Executa uma carga incremental na camada Bronze e registra seu status no CouchDB."""
    try:
        if not start_time:
            start_time = (datetime.utcnow() - timedelta(days=7)).isoformat()
        if not end_time:
            end_time = datetime.utcnow().isoformat()

        doc_id = create_status_record(table, "incremental", start_time, end_time)
        update_status(doc_id, "running")

        params = {"start_time": start_time, "end_time": end_time}
        execute_query("bronze", table, params)

        update_status(doc_id, "success")
        return {"status": "Carga incremental concluída", "job_id": doc_id}

    except FileNotFoundError:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=404, detail="Query não encontrada")

    except Exception as e:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/silver/{table}/upsert")
def upsert_silver(table: str, start_time: str = None, end_time: str = None):
    """Executa um UPSERT na camada Silver e registra seu status no CouchDB."""
    try:
        if not start_time:
            start_time = (datetime.utcnow() - timedelta(days=30)).isoformat()
        if not end_time:
            end_time = datetime.utcnow().isoformat()

        doc_id = create_status_record(table, "upsert", start_time, end_time)
        update_status(doc_id, "running")

        params = {"start_time": start_time, "end_time": end_time}
        execute_query("silver", table, params)

        update_status(doc_id, "success")
        return {
            "status": "UPSERT concluído",
            "start_time": start_time,
            "end_time": end_time,
            "job_id": doc_id,
        }

    except FileNotFoundError:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=404, detail="Query não encontrada")

    except Exception as e:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/gold/{table}/upsert")
def upsert_gold(table: str, start_time: str = None, end_time: str = None):
    """Executa um UPSERT na camada Gold e registra seu status no CouchDB."""
    try:
        if not start_time:
            start_time = (datetime.utcnow() - timedelta(days=30)).isoformat()
        if not end_time:
            end_time = datetime.utcnow().isoformat()

        doc_id = create_status_record(table, "upsert", start_time, end_time)
        update_status(doc_id, "running")

        params = {"start_time": start_time, "end_time": end_time}
        execute_query("gold", table, params)

        update_status(doc_id, "success")
        return {
            "status": "UPSERT concluído",
            "start_time": start_time,
            "end_time": end_time,
            "job_id": doc_id,
        }

    except FileNotFoundError:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=404, detail="Query não encontrada")

    except Exception as e:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status/{job_id}")
def get_status(job_id: str):
    """Retorna o status de um job pelo ID."""
    try:
        if job_id in db:
            return db[job_id]
        else:
            raise HTTPException(status_code=404, detail="Job não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
