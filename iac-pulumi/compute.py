import pulumi_gcp


class Compute:
    def __init__(self, config):
        self.config = config

    def create_nat_gateway(self):
        """Cria um NAT Gateway para permitir que VMs privadas acessem a internet."""
        router = pulumi_gcp.compute.Router(
            "my-nat-router",
            name="my-nat-router",
            network=self.config.network_name,
            region=self.config.region,
        )

        return pulumi_gcp.compute.RouterNat(
            "my-nat-config",
            name="my-nat-config",
            router=router.name,
            region=self.config.region,
            nat_ip_allocate_option="AUTO_ONLY",
            source_subnetwork_ip_ranges_to_nat="ALL_SUBNETWORKS_ALL_IP_RANGES",
        )

    def create_vm(self, public_ip=False):
        """Cria a VM principal, permitindo definir se terá IP público ou não."""
        access_config = [{}] if public_ip else []

        return pulumi_gcp.compute.Instance(
            "cyber-gen-vm",
            name="cyber-gen-vm",
            machine_type="e2-micro",
            zone=self.config.zone,
            boot_disk={"initializeParams": {"image": "debian-cloud/debian-11"}},
            network_interfaces=[
                {
                    "network": self.config.network_name,
                    "subnetwork_project": self.config.project,
                    "access_configs": access_config,
                }
            ],
            metadata_startup_script="""#!/bin/bash
                apt update && apt install -y postgresql-client
                echo "PostgreSQL Client instalado com sucesso!"
            """,
        )

    def create_bastion_host(self):
        """Cria uma VM Bastion para acesso seguro à VM privada."""
        return pulumi_gcp.compute.Instance(
            "bastion-vm",
            name="bastion-vm",
            machine_type="e2-micro",
            zone=self.config.zone,
            boot_disk={"initializeParams": {"image": "debian-cloud/debian-11"}},
            network_interfaces=[
                {
                    "network": self.config.network_name,
                    "subnetwork_project": self.config.project,
                    "access_configs": [{}],
                }
            ],
            metadata_startup_script="""#!/bin/bash
                echo "Bastion host configurado com sucesso!"
            """,
        )
