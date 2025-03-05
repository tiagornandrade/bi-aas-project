import pulumi
from config import Config
from networking import Networking
from database import Database
from datastream import Datastream
from compute import Compute
from cloud_run import CloudRun
from iam import IAMBinding

config = Config()

networking = Networking(config)
vpc_connector = networking.create_vpc_connector()
enable_vpc_api = networking.enable_vpc_api()

database = Database(config)
db_instance = database.create_instance()
db = database.create_database(db_instance)
db_user = database.create_user(db_instance)

datastream = Datastream(config)
datastream_vpc = datastream.create_datastream_vpc()
datastream_subnet = datastream.create_datastream_subnet(datastream_vpc)
private_connection = datastream.create_private_connection(
    datastream_subnet, datastream_vpc
)

bigquery_dataset = datastream.create_bigquery_dataset()

datastream_source = datastream.create_datastream_source(private_connection)
datastream_destination = datastream.create_datastream_destination()
datastream_stream = datastream.create_datastream_stream(
    datastream_source, datastream_destination, bigquery_dataset
)

compute = Compute(config)
nat = compute.create_nat_gateway()
vm = compute.create_vm(public_ip=False)
bastion = compute.create_bastion_host()

cloud_run = CloudRun(config)
cloud_run_service = cloud_run.create_service(db_instance, vpc_connector)
iam_policy = cloud_run.create_iam_policy(cloud_run_service)

roles = []
iam_binding = IAMBinding(config.project, config.service_account_email, roles)
bindings = iam_binding.create_policy_binding()

pulumi.export("iam_binding_id", bindings[0].id if bindings else None)
pulumi.export(
    "service_url", cloud_run_service.statuses[0]["url"] if cloud_run_service else None
)
pulumi.export(
    "db_connection_name", db_instance.connection_name if db_instance else None
)
pulumi.export("vm_private_ip", vm.network_interfaces[0]["network_ip"] if vm else None)
pulumi.export(
    "bastion_ip",
    bastion.network_interfaces[0]["access_configs"][0]["nat_ip"] if bastion else None,
)
pulumi.export("datastream_source", datastream_source.id if datastream_source else None)
pulumi.export(
    "datastream_destination",
    datastream_destination.id if datastream_destination else None,
)
pulumi.export("datastream_stream", datastream_stream.id if datastream_stream else None)
