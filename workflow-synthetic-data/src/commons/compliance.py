import random
from uuid import uuid4
from faker import Faker
from typing import List

fake = Faker("pt_BR")


class CompliancesEvents:
    """Gera dados sintéticos para regulamentações, auditorias e verificações de usuários."""

    @staticmethod
    def generate_regulations(count: int) -> List[dict]:
        """Gera regulamentações como dicionários."""
        return [
            {
                "regulation_id": str(uuid4()),
                "name": fake.sentence(),
                "description": fake.paragraph(),
                "jurisdiction": fake.country(),
                "date": fake.date_time_this_year(),
                "created_at": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_user_verifications(count: int) -> List[dict]:
        """Gera verificações de usuários como dicionários."""
        return [
            {
                "verification_id": str(uuid4()),
                "user_id": str(uuid4()),
                "type": random.choice(["email", "phone", "identity"]),
                "status": random.choice(["approved", "pending", "rejected"]),
                "date": fake.date_time_this_year(),
                "created_at": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]
