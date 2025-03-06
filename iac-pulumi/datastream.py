import pulumi
import pulumi_gcp
import time


unique_suffix = str(int(time.time()))


def get_resource_name(base: str) -> str:
    """Generates a unique resource name.

    This helper function creates a unique resource name by appending
    a timestamp-based suffix to the provided base name.

    Args:
        base: The base name for the resource.

    Returns:
        The unique resource name.
    """
    return f"{base}-{unique_suffix}"


def build_source_config(source_connection) -> dict:
    """Builds the source configuration for the Datastream stream.

    This function constructs the source configuration dictionary required
    by the Datastream stream, specifying the connection profile and
    PostgreSQL objects to include.

    Args:
        source_connection: The Datastream source connection profile.

    Returns:
        The source configuration dictionary.
    """
    return {
        "source_connection_profile": source_connection.id,
        "postgresql_source_config": {
            "include_objects": {
                "postgresql_schemas": [
                    {
                        "schema": "public",
                        "postgresql_tables": [
                            {"table": "accounts"},
                            {"table": "audits"},
                            {"table": "claims"},
                            {"table": "credit_scores"},
                            {"table": "entities"},
                            {"table": "insured_entities"},
                            {"table": "loans"},
                            {"table": "merchants"},
                            {"table": "payment_methods"},
                            {"table": "payments"},
                            {"table": "policies"},
                            {"table": "portfolios"},
                            {"table": "regulations"},
                            {"table": "risk_assessments"},
                            {"table": "subaccounts"},
                            {"table": "transactions"},
                            {"table": "user_verifications"},
                            {"table": "users"},
                        ],
                    }
                ]
            },
            "publication": "postgres_publication",
            "replication_slot": "postgres_replication",
        },
    }


def build_destination_config(destination_connection, bigquery_dataset) -> dict:
    """Builds the destination configuration for the Datastream stream.

    This function constructs the destination configuration dictionary for
    the Datastream stream, specifying the BigQuery connection profile,
    target dataset, and append-only mode.

    Args:
        destination_connection: The Datastream destination connection profile.
        bigquery_dataset: The BigQuery dataset object.

    Returns:
        The destination configuration dictionary.
    """
    return {
        "destination_connection_profile": destination_connection.id,
        "bigquery_destination_config": {
            # "data_freshness": "900s",
            "single_target_dataset": {"dataset_id": bigquery_dataset.id},
            "append_only": {},
        },
    }


class Datastream:
    """Creates and manages Datastream resources."""

    def __init__(self, config):
        self.config = config

    def create_datastream_network(self):
        """Creates a custom VPC network and subnet for Datastream."""
        vpc_name = get_resource_name("datastream-vpc")
        vpc = pulumi_gcp.compute.Network(
            vpc_name,
            name=vpc_name,
            auto_create_subnetworks=False,
        )

        subnet_name = get_resource_name("datastream-subnet")
        subnet = pulumi_gcp.compute.Subnetwork(
            subnet_name,
            name=subnet_name,
            region=self.config.region,
            network=vpc.id,
            ip_cidr_range="10.250.0.0/24",
            private_ip_google_access=True,
        )

        return vpc, subnet

    def create_datastream_source(self):
        """Creates a Datastream connection profile for a PostgreSQL source."""
        return pulumi_gcp.datastream.ConnectionProfile(
            get_resource_name("cyber-gen-source-connection"),
            connection_profile_id=get_resource_name("source-profile"),
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
        """Creates a Datastream connection profile for a BigQuery destination."""
        return pulumi_gcp.datastream.ConnectionProfile(
            get_resource_name("cyber-gen-destination-connection"),
            connection_profile_id=get_resource_name("destination-profile"),
            location=self.config.region,
            display_name="Cyber Gen BigQuery Destination",
            bigquery_profile={},
        )

    def create_datastream_stream(self, source_connection, destination_connection, bigquery_dataset):
        """Creates a Datastream stream to replicate data from PostgreSQL to BigQuery."""
        stream = pulumi_gcp.datastream.Stream(
            get_resource_name("cyber-gen-stream"),
            display_name="Cyber Gen Replication Stream",
            location=self.config.region,
            stream_id=get_resource_name("postgres-to-bigquery-stream"),
            source_config=build_source_config(source_connection),
            destination_config=build_destination_config(destination_connection, bigquery_dataset),
            backfill_all={},
        )

    def create_bigquery_dataset(self, prefix="cdc_postgres_"):
        """Creates a BigQuery dataset."""
        dataset_name = f"{prefix}{self.config.bigquery_dataset}"

        return pulumi_gcp.bigquery.Dataset(
            get_resource_name("cyber-gen-dataset"),
            dataset_id=dataset_name,
            friendly_name="Cyber Gen Dataset",
            description="Dataset for PostgreSQL data via Datastream",
            location="US",
            opts=pulumi.ResourceOptions(delete_before_replace=True),
        )
