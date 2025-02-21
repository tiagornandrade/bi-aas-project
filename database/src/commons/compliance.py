import itertools
import random
from uuid import uuid4
from faker import Faker
from typing import List

fake = Faker("pt_BR")

counter = itertools.count(start=1)


class CompliancesEvents:
    """Gera dados sintéticos para regulamentações, auditorias e verificações de usuários."""

    @staticmethod
    def generate_regulations(count: int) -> List[dict]:
        """Gera regulamentações como dicionários."""
        return [
            {
                "id": next(counter),
                "regulation_id": str(uuid4()),
                "name": fake.sentence(),
                "description": fake.paragraph(),
                "jurisdiction": fake.country(),
                "created_at": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_user_verifications(count: int) -> List[dict]:
        """Gera verificações de usuários como dicionários."""
        return [
            {
                "id": next(counter),
                "verification_id": str(uuid4()),
                "user_id": str(uuid4()),
                "type": random.choice(["email", "phone", "identity"]),
                "status": random.choice(["approved", "pending", "rejected"]),
                "date": fake.date_time_this_year(),
                "created_at": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]
