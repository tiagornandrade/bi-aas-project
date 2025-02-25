import yaml
import os
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta

CONFIG_PATH = "/opt/airflow/dags/dags_config.yaml"

with open(CONFIG_PATH) as file:
    config = yaml.safe_load(file)

default_args = config.get("default_args", {})

for layer, layer_params in config["dags"].items():
    schedule_interval = layer_params.get("schedule_interval", "@daily")
    catchup = layer_params.get("catchup", False)
    tables = layer_params.get("tables", [])

    for table in tables:
        dag_id = f"load_{layer}_{table}"

        with DAG(
            dag_id=dag_id,
            default_args=default_args,
            schedule_interval=schedule_interval,
            catchup=catchup,
            tags=[layer, table],
        ) as dag:

            api_task = SimpleHttpOperator(
                task_id=f"{layer}_{table}_task",
                http_conn_id="api_service",
                endpoint=f"/{layer}/{table}/{'incremental' if layer == 'bronze' else 'upsert'}",
                method="POST",
                headers={"Content-Type": "application/json"},
                data="{}",
                response_check=lambda response: response.status_code == 200,
                log_response=True,
            )

        globals()[dag_id] = dag
