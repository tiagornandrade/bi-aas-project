import pulumi
import pulumi_gcp
from dotenv import load_dotenv
import os

load_dotenv()

project = os.getenv("PROJECT_ID")
region = os.getenv("REGION")
zone = "us-central1-a"
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

network_name = f"projects/{project}/global/networks/default"

db_instance_name = "cyber-gen-db"

vpc_connector = pulumi_gcp.vpcaccess.Connector(
    "serverless-vpc-connector",
    name="cyber-gen-vpc-connector",
    region=region,
    network=network_name,
    machine_type="e2-micro",
    max_instances=3,
    min_instances=2,
    ip_cidr_range="10.8.0.0/28",
)

db_instance = pulumi_gcp.sql.DatabaseInstance(
    "cyber_gen_postgres",
    name=db_instance_name,
    database_version="POSTGRES_14",
    region=region,
    deletion_protection=False,
    settings={
        "tier": "db-f1-micro",
        "availability_type": "REGIONAL",
        "ip_configuration": {
            "private_network": network_name,
        },
        "backup_configuration": {"enabled": False},
    },
)

database = pulumi_gcp.sql.Database(
    "cybergen-db", name=db_name, instance=db_instance.name
)

db_user_instance = pulumi_gcp.sql.User(
    "db-user", name=db_user, instance=db_instance.name, password=db_password
)

vm = pulumi_gcp.compute.Instance(
    "cyber-gen-vm",
    name="cyber-gen-vm",
    machine_type="e2-micro",
    zone=zone,
    boot_disk={"initializeParams": {"image": "debian-cloud/debian-11"}},
    network_interfaces=[
        {
            "network": network_name,
            "subnetwork_project": project,
            "access_configs": [],
        }
    ],
    metadata_startup_script="""#!/bin/bash
    apt update && apt install -y postgresql-client
    echo "PostgreSQL Client instalado com sucesso!"
    """,
)

enable_vpc_api = pulumi_gcp.projects.Service(
    "enable-vpcaccess-api", service="vpcaccess.googleapis.com", disable_on_destroy=False
)

cloud_run_service = pulumi_gcp.cloudrun.Service(
    "default",
    name="cyber-gen-service-1",
    location=region,
    template={
        "spec": {
            "containers": [
                {
                    "image": "gcr.io/yams-lab-nonprod/cyber-gen:latest",
                    "envs": [
                        {"name": "DB_NAME", "value": db_name},
                        {"name": "DB_USER", "value": db_user},
                        {"name": "DB_PASSWORD", "value": db_password},
                        {"name": "DB_INSTANCE", "value": db_instance.connection_name},
                    ],
                }
            ],
            "serviceAccountName": "biaas-dev@yams-lab-nonprod.iam.gserviceaccount.com",
            "vpcAccess": {"connector": vpc_connector.id, "egress": "ALL_TRAFFIC"},
        },
    },
    traffics=[
        {
            "percent": 100,
            "latestRevision": True,
        }
    ],
)

iam_policy = pulumi_gcp.cloudrun.IamPolicy(
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

pulumi.export("service_url", cloud_run_service.statuses[0]["url"])
pulumi.export("db_connection_name", db_instance.connection_name)
pulumi.export("vm_private_ip", vm.network_interfaces[0]["network_ip"])
