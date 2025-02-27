import os
from fastapi import FastAPI, HTTPException
from datetime import datetime
import uvicorn
from src.utils.query_manager import execute_query
from src.utils.firestore import create_status_record, update_status, db

app = FastAPI()


def process_job(layer: str, table: str):
    """
    Processa a execução da query da camada específica e atualiza o status no Datastore.
    """
    doc_id = None

    try:
        start_time = datetime.utcnow().isoformat()
        end_time = start_time

        doc_id = create_status_record(table, "execute", start_time, end_time)
        update_status(doc_id, "running")

        execute_query(layer, table, params={})

        update_status(doc_id, "success")
        return {"status": "Execução concluída", "job_id": doc_id}

    except FileNotFoundError:
        if doc_id:
            update_status(doc_id, "failed")
        raise HTTPException(status_code=404, detail="Query não encontrada")

    except Exception as e:
        if doc_id:
            update_status(doc_id, "failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Cyber-gen is running"}


@app.post("/{layer}/{table}/execute")
def execute_table(layer: str, table: str):
    """Executa a query correspondente à camada e registra o status."""
    if layer not in ["bronze", "silver", "gold"]:
        raise HTTPException(status_code=400, detail="Camada inválida")

    return process_job(layer, table)


@app.get("/status/{job_id}")
def get_status(job_id: str):
    """Retorna o status de um job pelo ID."""
    try:
        task_key = db.key("etl_jobs", job_id)
        entity = db.get(task_key)

        if entity:
            return entity
        raise HTTPException(status_code=404, detail="Job não encontrado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
