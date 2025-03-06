import pulumi
import pulumi_gcp
import time


unique_suffix = str(int(time.time()))


class Datastream:
    """Creates and manages Datastream resources.

    This class handles the creation of Datastream networks, source and
    destination connection profiles, streams, and BigQuery datasets.
    """

    def __init__(self, config):
        self.config = config

    def create_datastream_network(self):
        """Creates a custom VPC network and subnet for Datastream.

        This method sets up the required network infrastructure for Datastream,
        including a VPC network and a subnet with private Google access.
        """
        vpc = pulumi_gcp.compute.Network(
            "datastream-vpc",
            name="datastream-vpc",
            auto_create_subnetworks=False,
        )

        subnet = pulumi_gcp.compute.Subnetwork(
            "datastream-subnet",
            name="datastream-subnet",
            region=self.config.region,
            network=vpc.id,
            ip_cidr_range="10.250.0.0/24",
            private_ip_google_access=True,
        )

        return vpc, subnet

    def create_datastream_source(self):
        """Creates a Datastream connection profile for a PostgreSQL source.

        This method sets up a connection profile to an existing PostgreSQL database
        hosted in Cloud SQL, using authorized IP for connectivity.
        """
        authorized_networks = [
            {"value": "34.71.242.81"},
            {"value": "34.72.28.29"},
            {"value": "34.67.6.157"},
            {"value": "34.67.234.134"},
            {"value": "34.72.239.218"},
        ]

        return pulumi_gcp.datastream.ConnectionProfile(
            f"cyber-gen-source-connection-{unique_suffix}",
            connection_profile_id=f"source-profile-{unique_suffix}",
            location=self.config.region,
            display_name="Cyber Gen PostgreSQL Source",
            postgresql_profile={
                "hostname": self.config.db_host,
                "port": 5432,
                "database": self.config.db_name,
                "username": self.config.db_user,
                "password": pulumi.Output.secret(self.config.db_password),
            },
        )

    def create_datastream_destination(self):
        """Creates a Datastream connection profile for a BigQuery destination.

        This method sets up a connection profile to BigQuery, which serves
        as the destination for the Datastream.
        """
        return pulumi_gcp.datastream.ConnectionProfile(
            f"cyber-gen-destination-connection-{unique_suffix}",
            connection_profile_id=f"destination-profile-{unique_suffix}",
            location=self.config.region,
            display_name="Cyber Gen BigQuery Destination",
            bigquery_profile={},
        )

    def create_datastream_stream(
        self, source_connection, destination_connection, bigquery_dataset
    ):
        """Creates a Datastream stream to replicate data from PostgreSQL to BigQuery.

        This method configures a stream to transfer data from a PostgreSQL source
        to a BigQuery destination, including specific tables and performing a backfill.
        """
        stream = pulumi_gcp.datastream.Stream(
            f"cyber-gen-stream-{unique_suffix}",
            display_name="Cyber Gen Replication Stream",
            location=self.config.region,
            stream_id=f"postgres-to-bigquery-stream-{unique_suffix}",
            source_config={
                "source_connection_profile": source_connection.id,
                "postgresql_source_config": {
                    "include_objects": {
                        "postgresql_schemas": [
                            {"schema": "public", "postgresql_tables": [{"table": "*"}]},
                        ]
                    },
                    "publication": "postgres_publication",
                    "replication_slot": "postgres_replication",
                },
            },
            destination_config={
                "destination_connection_profile": destination_connection.id,
                "bigquery_destination_config": {
                    "data_freshness": "300s",
                    "single_target_dataset": {
                        "dataset_id": bigquery_dataset.id,
                    },
                    "append_only": {},
                },
            },
            backfill_all={},
        )

    def create_bigquery_dataset(self, prefix="cdc_postgres_"):
        """Cria um dataset no BigQuery"""
        dataset_name = f"{prefix}{self.config.bigquery_dataset}"

        return pulumi_gcp.bigquery.Dataset(
            "cyber-gen-dataset",
            dataset_id=dataset_name,
            friendly_name="Cyber Gen Dataset",
            description="Dataset para armazenar os dados do PostgreSQL via Datastream",
            location="US",
            opts=pulumi.ResourceOptions(delete_before_replace=True),
        )
