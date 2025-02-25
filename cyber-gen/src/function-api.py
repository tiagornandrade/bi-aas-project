from fastapi import FastAPI, HTTPException
from src.utils.query_manager import execute_query
from src.utils.couchdb import create_status_record, update_status, db
from datetime import datetime, timedelta

app = FastAPI()


def process_job(
    layer: str, table: str, job_type: str, start_time: str = None, end_time: str = None
):
    """
    Função auxiliar para processar a lógica de execução de jobs.
    Define horários padrão, cria um registro de status e atualiza seu status.
    Retorna o ID do job para referência posterior.
    """
    try:
        if not start_time:
            delta = (
                timedelta(days=7) if job_type == "incremental" else timedelta(days=30)
            )
            start_time = (datetime.utcnow() - delta).isoformat()
        if not end_time:
            end_time = datetime.utcnow().isoformat()

        doc_id = create_status_record(table, job_type, start_time, end_time)
        update_status(doc_id, "running")

        params = {"start_time": start_time, "end_time": end_time}
        execute_query(layer, table, params)

        update_status(doc_id, "success")
        return doc_id
    except FileNotFoundError as e:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=404, detail="Query não encontrada") from e
    except Exception as e:
        update_status(doc_id, "failed")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/bronze/{table}/incremental")
def load_incremental_bronze(table: str, start_time: str = None, end_time: str = None):
    """Executa uma carga incremental na camada Bronze e registra seu status no CouchDB."""
    job_id = process_job("bronze", table, "incremental", start_time, end_time)
    return {"status": "Carga incremental concluída", "job_id": job_id}


@app.post("/silver/{table}/upsert")
def upsert_silver(table: str, start_time: str = None, end_time: str = None):
    """Executa um UPSERT na camada Silver e registra seu status no CouchDB."""
    job_id = process_job("silver", table, "upsert", start_time, end_time)
    return {
        "status": "UPSERT concluído",
        "start_time": start_time,
        "end_time": end_time,
        "job_id": job_id,
    }


@app.post("/gold/{table}/upsert")
def upsert_gold(table: str, start_time: str = None, end_time: str = None):
    """Executa um UPSERT na camada Gold e registra seu status no CouchDB."""
    job_id = process_job("gold", table, "upsert", start_time, end_time)
    return {
        "status": "UPSERT concluído",
        "start_time": start_time,
        "end_time": end_time,
        "job_id": job_id,
    }


@app.get("/status/{job_id}")
def get_status(job_id: str):
    """Retorna o status de um job pelo ID."""
    try:
        if job_id in db:
            return db[job_id]
        raise HTTPException(status_code=404, detail="Job não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
