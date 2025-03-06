import pulumi  # type: ignore
import pulumi_gcp  # type: ignore
from config import Config
from networking import Networking
from database import Database
from datastream import Datastream
from compute import Compute
from cloud_run import CloudRun
from iam import IAMBinding

config = Config()

# Networking
networking = Networking(config)
vpc_connector = networking.create_vpc_connector()
enable_vpc_api = networking.enable_vpc_api()

# Database
database = Database(config)
db_instance = database.create_instance()
db = database.create_database(db_instance)
db_user = database.create_user(db_instance)

# Datastream
datastream = Datastream(config)
datastream_vpc, datastream_subnet = datastream.create_datastream_network()

datastream_source = datastream.create_datastream_source()
datastream_destination = datastream.create_datastream_destination()

bigquery_dataset = datastream.create_bigquery_dataset()

datastream_stream = datastream.create_datastream_stream(
    datastream_source, datastream_destination, bigquery_dataset
)

# Compute
compute = Compute(config)
nat = compute.create_nat_gateway()
vm = compute.create_vm(public_ip=False)
bastion = compute.create_bastion_host()

# Cloud Run
cloud_run = CloudRun(config)
cloud_run_service = cloud_run.create_service(db_instance, vpc_connector)
iam_policy = cloud_run.create_iam_policy(cloud_run_service)

# IAM
roles = ["roles/cloudsql.admin", "roles/storage.admin", "roles/bigquery.admin"]
iam_binding = IAMBinding(config.project, config.service_account_email, roles)
bindings = iam_binding.create_policy_binding()

# Exports
pulumi.export(
    "database_info",
    {
        "db_connection_name": db_instance.connection_name if db_instance else None,
        "db_name": db.name if db else None,
    },
)

pulumi.export(
    "compute_info",
    {
        "vm_private_ip": vm.network_interfaces[0]["network_ip"] if vm else None,
        "bastion_ip": (
            bastion.network_interfaces[0]["access_configs"][0]["nat_ip"]
            if bastion
            else None
        ),
    },
)

pulumi.export(
    "datastream_info",
    {
        "datastream_source": datastream_source.id if datastream_source else None,
        "datastream_destination": (
            datastream_destination.id if datastream_destination else None
        ),
        "datastream_stream": datastream_stream.id if datastream_stream else None,
    },
)

pulumi.export(
    "cloud_run_info",
    {
        "service_url": (
            cloud_run_service.statuses[0]["url"]
            if (cloud_run_service and cloud_run_service.statuses)
            else None
        ),
    },
)

pulumi.export(
    "iam_binding_info",
    {
        "iam_binding_id": bindings[0].id if bindings else None,
    },
)
