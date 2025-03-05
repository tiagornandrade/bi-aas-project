import os
from dotenv import load_dotenv
import pulumi

load_dotenv()


class Config:
    def __init__(self):
        self.project = os.getenv("PROJECT_ID")
        self.region = os.getenv("REGION")
        self.zone = os.getenv("ZONE", "us-central1-a")
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = pulumi.Output.secret(os.getenv("DB_PASSWORD"))
        self.bigquery_dataset = os.getenv("BIGQUERY_DATASET")
        self.network_name = f"projects/{self.project}/global/networks/default"
        self.cloudsql_vpc_name = f"cloudsql-vpc-{pulumi.get_stack()}"
        self.service_account_email = os.getenv("SERVICE_ACCOUNT_EMAIL")
