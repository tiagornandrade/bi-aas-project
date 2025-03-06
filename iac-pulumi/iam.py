import pulumi_gcp
import logging


class IAMBinding:
    def __init__(self, project_id, service_account_email, roles):
        self.project_id = project_id
        self.service_account_email = service_account_email
        self.roles = roles

    def create_policy_binding(self):
        """Cria a ligação da política IAM para a conta de serviço"""
        if not self.roles:
            logging.warning("Roles list is empty. Nenhuma ligação IAM será criada.")

        iam_bindings = []

        for role in self.roles:
            binding = pulumi_gcp.projects.IAMBinding(
                f"{role}-binding",
                project=self.project_id,
                members=[f"serviceAccount:{self.service_account_email}"],
                role=role,
            )
            iam_bindings.append(binding)

        bigquery_permission = pulumi_gcp.projects.IAMBinding(
            "datastream-bigquery-permissions",
            project=self.project_id,
            members=[
                "serviceAccount:service-517665453940@gcp-sa-datastream.iam.gserviceaccount.com"
            ],
            role="roles/bigquery.dataViewer",
        )
        iam_bindings.append(bigquery_permission)

        return iam_bindings
