import pulumi_gcp


class Networking:
    def __init__(self, config):
        self.config = config

    def create_vpc_connector(self):
        return pulumi_gcp.vpcaccess.Connector(
            "serverless-vpc-connector",
            name="cyber-gen-vpc-connector",
            region=self.config.region,
            network=self.config.network_name,
            machine_type="e2-micro",
            max_instances=3,
            min_instances=2,
            ip_cidr_range="10.8.0.0/28",
        )

    def enable_vpc_api(self):
        return pulumi_gcp.projects.Service(
            "enable-vpcaccess-api",
            service="vpcaccess.googleapis.com",
            disable_on_destroy=False,
        )
