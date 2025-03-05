import pulumi
import pulumi_gcp


class CloudRun:
    def __init__(self, config):
        self.config = config

    def create_service(self, db_instance, vpc_connector):
        return pulumi_gcp.cloudrun.Service(
            "default",
            name="cyber-gen-service-1",
            location=self.config.region,
            template={
                "metadata": {
                    "annotations": {
                        "run.googleapis.com/vpc-access-connector": vpc_connector.id,
                        "run.googleapis.com/vpc-access-egress": "all-traffic",
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "image": "gcr.io/yams-lab-nonprod/cyber-gen:latest",
                            "envs": [
                                {"name": "DB_NAME", "value": self.config.db_name},
                                {"name": "DB_USER", "value": self.config.db_user},
                                {
                                    "name": "DB_PASSWORD",
                                    "value": self.config.db_password,
                                },
                                {
                                    "name": "DB_INSTANCE",
                                    "value": db_instance.connection_name,
                                },
                            ],
                        }
                    ],
                    "serviceAccountName": "biaas-dev@yams-lab-nonprod.iam.gserviceaccount.com",
                },
            },
            traffics=[{"percent": 100, "latestRevision": True}],
        )

    def create_iam_policy(self, cloud_run_service):
        return pulumi_gcp.cloudrun.IamPolicy(
            "default-no-auth",
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
