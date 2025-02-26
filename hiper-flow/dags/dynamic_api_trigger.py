import yaml
import os
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta

CONFIG_PATH = "/opt/airflow/dags/dags_config.yaml"


def load_config(path: str) -> dict:
    """Carrega o arquivo de configuração YAML."""
    with open(path) as file:
        return yaml.safe_load(file)


def check_api_response(response):
    """Verifica se a resposta da API tem status 200."""
    return response.status_code == 200


def create_dag(layer: str, table: str, layer_params: dict, default_args: dict) -> DAG:
    """Cria uma DAG para executar a API de carga de dados para uma tabela específica."""

    dag_id = f"load_{layer}_{table}"
    schedule_interval = layer_params.get("schedule_interval", "@daily")
    catchup = layer_params.get("catchup", False)

    with DAG(
        dag_id=dag_id,
        default_args=default_args,
        schedule_interval=schedule_interval,
        catchup=catchup,
        tags=[layer, table],
    ) as dag:

        SimpleHttpOperator(
            task_id=f"{layer}_{table}_trigger",
            http_conn_id="api-etl",
            endpoint=f"http://0.0.0.0:8000/{layer}/{table}/execute",
            method="POST",
            headers={"Content-Type": "application/json"},
            data="{}",
            response_check=check_api_response,
            log_response=True,
        )

    return dag


config = load_config(CONFIG_PATH)
default_args = config.get("default_args", {})

for layer, layer_params in config["dags"].items():
    for table in layer_params.get("tables", []):
        dag = create_dag(layer, table, layer_params, default_args)
        globals()[dag.dag_id] = dag
