import pulumi
import pulumi_gcp


class Database:
    def __init__(self, config):
        self.config = config

    def create_instance(self):
        """Cria uma instância do Cloud SQL (PostgreSQL)"""
        cloudsql_vpc = pulumi_gcp.compute.Network(
            self.config.cloudsql_vpc_name,
            name=self.config.cloudsql_vpc_name,
            auto_create_subnetworks=False,
        )

        return pulumi_gcp.sql.DatabaseInstance(
            "cyber_gen_postgres",
            name="cyber-gen-db",
            database_version="POSTGRES_14",
            region=self.config.region,
            deletion_protection=False,
            settings={
                "tier": "db-f1-micro",
                "availability_type": "REGIONAL",
                "ip_configuration": {
                    "private_network": self.config.network_name,
                    "ipv4_enabled": True,
                    "authorized_networks": [{"value": "0.0.0.0/0"}],
                },
                "backup_configuration": {"enabled": False},
            },
        )

    def create_database(self, instance):
        """Cria o banco de dados na instância"""
        return pulumi_gcp.sql.Database(
            "cybergen-db", name=self.config.db_name, instance=instance.name
        )

    def create_user(self, instance):
        """Cria um usuário no banco de dados"""
        return pulumi_gcp.sql.User(
            "db-user",
            name=self.config.db_user,
            instance=instance.name,
            password=pulumi.Output.secret(self.config.db_password),
        )

    def create_private_service_connection(self, network):
        """Cria uma conexão de serviço privada para o Cloud SQL"""
        return pulumi_gcp.compute.GlobalAddress(
            "cloudsql-private-ip",
            name="cloudsql-private-ip",
            region=self.config.region,
            address_type="INTERNAL",
            network=network.id,
            purpose="VPC_PEERING",
            prefix_length=16,
        )
