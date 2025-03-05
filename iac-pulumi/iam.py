import pulumi_gcp


class IAMBinding:
    def __init__(self, project_id, service_account_email, roles):
        self.project_id = project_id
        self.service_account_email = service_account_email
        self.roles = roles

    def create_policy_binding(self):
        """Cria a ligação da política IAM para a conta de serviço"""
        iam_bindings = []

        for role in self.roles:
            binding = pulumi_gcp.projects.IAMBinding(
                f"{role}-binding",
                project=self.project_id,
                members=[f"serviceAccount:{self.service_account_email}"],
                role=role,
            )
            iam_bindings.append(binding)

        return iam_bindings
