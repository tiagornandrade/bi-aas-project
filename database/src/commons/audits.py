import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List

fake = Faker("pt_BR")


class AuditsEvents:
    @staticmethod
    def generate_audits(count: int) -> List[dict]:
        """Gera auditorias como dicionários."""
        return [
            {
                "audit_id": str(uuid4()),
                "entity_id": str(uuid4()),
                "status": np.random.choice(["success", "failure"]),
                "findings": np.random.choice(["no findings", "findings"]),
                "date": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]
