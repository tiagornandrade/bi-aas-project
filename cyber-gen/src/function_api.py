import os
from fastapi import Depends, FastAPI, HTTPException
from datetime import datetime
import uvicorn
from datetime import timezone
from src.utils.query_manager import execute_query
from src.utils.firestore import (
    DatastoreClient,
    create_status_record,
    get_datastore_client,
    update_status,
)

app = FastAPI()


def process_job(layer: str, table: str):
    """
    Processa a execução da query da camada específica e atualiza o status no Datastore.
    """
    doc_id = None

    try:
        start_time = datetime.now(timezone.utc).isoformat()
        end_time = start_time

        doc_id = create_status_record(table, "execute", start_time, end_time)
        update_status(doc_id, "running")

        execute_query(layer, table, params={})

        update_status(doc_id, "success")
        return {"status": "Execução concluída", "job_id": doc_id}

    except FileNotFoundError as e:
        if doc_id:
            update_status(doc_id, "failed")
        raise HTTPException(status_code=404, detail="Query não encontrada") from e

    except Exception as e:
        if doc_id:
            update_status(doc_id, "failed")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/")
def read_root():
    return {"message": "Cyber-gen is running"}


@app.post("/{layer}/{table}/execute")
def execute_table(layer: str, table: str):
    """Executa a query correspondente à camada e registra o status."""
    if layer in {"bronze", "silver", "gold"}:
        return process_job(layer, table)
    else:
        raise HTTPException(status_code=400, detail="Camada inválida")


@app.post("/status/")
def create_status(
    table: str,
    job_type: str,
    start_time: str,
    end_time: str,
    datastore_client: DatastoreClient = Depends(get_datastore_client),
):
    """Cria um status no Datastore."""
    try:
        job_id = datastore_client.create_status_record(
            table, job_type, start_time, end_time
        )
        return {"message": "Job criado com sucesso", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.patch("/status/{job_id}")
def update_status(
    job_id: str,
    status: str,
    datastore_client: DatastoreClient = Depends(get_datastore_client),
):
    """Atualiza o status de um job no Datastore."""
    try:
        datastore_client.update_status(job_id, status)
        return {"message": "Status atualizado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
