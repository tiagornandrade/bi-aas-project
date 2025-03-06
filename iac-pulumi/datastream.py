import pulumi
import pulumi_gcp


class Datastream:
    def __init__(self, config):
        self.config = config

    def create_datastream_network(
        self, vpc_name="datastream-vpc", subnet_name="datastream-subnet"
    ):
        """Cria uma VPC personalizada e uma sub-rede para o Datastream"""
        vpc = pulumi_gcp.compute.Network(
            vpc_name,
            name=vpc_name,
            auto_create_subnetworks=False,
        )

        subnet = pulumi_gcp.compute.Subnetwork(
            subnet_name,
            name=subnet_name,
            region=self.config.region,
            network=vpc.id,
            ip_cidr_range="10.240.0.0/24",
            private_ip_google_access=True,
        )

        return vpc, subnet

    def create_private_connection(self, datastream_subnet, datastream_vpc):
        """Cria uma conexão privada para o Datastream"""
        return pulumi_gcp.datastream.PrivateConnection(
            "cyber-gen-private-connect",
            private_connection_id="cyber-gen-private-connect",
            location=self.config.region,
            display_name="Cyber Gen Private Connection",
            vpc_peering_config={
                "vpc": datastream_vpc.name.apply(
                    lambda name: f"projects/{self.config.project}/global/networks/{name}"
                ),
                "subnet": datastream_subnet.id,
            },
        )

    def create_datastream_source(self, private_connection):
        """Cria um ConnectionProfile para o PostgreSQL no Cloud SQL via IP privado"""
        return pulumi_gcp.datastream.ConnectionProfile(
            "cyber-gen-source-connection",
            connection_profile_id="cyber-gen-source-connection",
            location=self.config.region,
            display_name="Cyber Gen PostgreSQL Source",
            postgresql_profile={
                "hostname": "10.97.17.2",
                "port": 5432,
                "database": self.config.db_name,
                "username": self.config.db_user,
                "password": pulumi.Output.secret(self.config.db_password),
            },
            private_connectivity={
                "private_connection": private_connection.id,
            },
        )

    def create_datastream_destination(self):
        """Cria o ConnectionProfile para o BigQuery"""
        return pulumi_gcp.datastream.ConnectionProfile(
            "cyber-gen-destination-connection",
            connection_profile_id="cyber-gen-destination-connection",
            location=self.config.region,
            display_name="Cyber Gen BigQuery Destination",
            bigquery_profile={},
        )

    def create_datastream_stream(
        self, source_connection, destination_connection, bigquery_dataset
    ):
        """Cria um Stream para transferir dados do PostgreSQL para o BigQuery"""
        return pulumi_gcp.datastream.Stream(
            "cyber-gen-stream",
            display_name="Cyber Gen Replication Stream",
            location=self.config.region,
            stream_id="postgres-to-bigquery-stream",
            source_config={
                "source_connection_profile": source_connection.id,
                "postgresql_source_config": {
                    "include_objects": {
                        "postgresql_schemas": [
                            {
                                "schema": "public",
                                "postgresql_tables": [
                                    {"table": "orders"},
                                    {"table": "customers"},
                                ],
                            }
                        ]
                    }
                },
            },
            destination_config={
                "destination_connection_profile": destination_connection.id,
                "bigquery_destination_config": {
                    "data_freshness": "900s",
                    "single_target_dataset": {
                        "dataset_id": bigquery_dataset.dataset_id,
                    },
                },
            },
            backfill_all={},
        )

    def create_bigquery_dataset(self):
        """Cria um dataset no BigQuery"""
        return pulumi_gcp.bigquery.Dataset(
            "cyber-gen-dataset",
            dataset_id=self.config.bigquery_dataset,
            friendly_name="Cyber Gen Dataset",
            description="Dataset para armazenar os dados do PostgreSQL via Datastream",
            location=self.config.region,
        )
