import pulumi
import pulumi_gcp


class CloudRun:
    def __init__(self, config):
        self.config = config

    def create_api_service(self, db_instance, vpc_connector):
        """Cria o serviço da API FastAPI no Cloud Run"""
        image = "gcr.io/yams-lab-nonprod/cyber-gen:latest"

        envs = [
            {"name": "DB_NAME", "value": self.config.db_name},
            {"name": "DB_USER", "value": self.config.db_user},
            {"name": "DB_PASSWORD", "value": self.config.db_password},
            {"name": "DB_INSTANCE", "value": db_instance.connection_name},
        ]

        return pulumi_gcp.cloudrun.Service(
            "api-service",
            location=self.config.region,
            template={
                "metadata": {
                    "annotations": {
                        "run.googleapis.com/vpc-access-connector": vpc_connector.id,
                        "run.googleapis.com/vpc-access-egress": "all-traffic",
                    }
                },
                "spec": {
                    "containers": [{"image": image, "envs": envs}],
                    "serviceAccountName": self.config.service_account_email,
                },
            },
            traffics=[{"percent": 100, "latestRevision": True}],
        )

    def create_producer_service(self, db_instance, vpc_connector):
        # sourcery skip: class-extract-method
        """Cria o serviço do Producer no Cloud Run"""
        image = "gcr.io/yams-lab-nonprod/producer-ingestion-pubsub:latest"

        envs = [
            {"name": "GCP_PROJECT_ID", "value": self.config.project},
            {"name": "DB_NAME", "value": self.config.db_name},
            {"name": "DB_USER", "value": self.config.db_user},
            {"name": "DB_PASSWORD", "value": self.config.db_password},
            {"name": "DB_INSTANCE", "value": db_instance.connection_name},
        ]

        return pulumi_gcp.cloudrun.Service(
            "producer-service",
            location=self.config.region,
            template={
                "metadata": {
                    "annotations": {
                        "run.googleapis.com/vpc-access-connector": vpc_connector.id,
                        "run.googleapis.com/vpc-access-egress": "all-traffic",
                    }
                },
                "spec": {
                    "containers": [{"image": image, "envs": envs}],
                    "serviceAccountName": self.config.service_account_email,
                },
            },
            traffics=[{"percent": 100, "latestRevision": True}],
        )

    def create_iam_policy(self, cloud_run_service):
        """Cria permissões IAM para permitir acesso ao serviço"""
        return pulumi_gcp.cloudrun.IamPolicy(
            f"{cloud_run_service._name}-no-auth",
            location=cloud_run_service.location,
            project=cloud_run_service.project,
            service=cloud_run_service.name,
            policy_data=pulumi.Output.all(cloud_run_service.id).apply(
                lambda service_id: f"""{{
                    "bindings": [
                        {{
                            "role": "roles/run.invoker",
                            "members": ["allUsers"]
                        }}
                    ]
                }}"""
            ),
        )
