import itertools
import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List

fake = Faker("pt_BR")

counter = itertools.count(start=1)


class InsuranceEvents:
    """Gera dados sintéticos para apólices de seguro, reivindicações e entidades seguradas."""

    @staticmethod
    def generate_policies(count: int) -> List[dict]:
        """Gera apólices de seguro como dicionários."""
        return [
            {
                "id": next(counter),
                "policy_id": str(uuid4()),
                "type": np.random.choice(["auto", "health", "home"]),
                "coverage_amount": np.random.randint(5000, 50000),
                "premium": np.random.randint(100, 1000),
                "start_date": fake.date_this_year(),
                "end_date": fake.date_this_year(),
                "user_id": str(uuid4()),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_claims(count: int) -> List[dict]:
        """Gera reivindicações de seguro como dicionários."""
        return [
            {
                "id": next(counter),
                "claim_id": str(uuid4()),
                "policy_id": str(uuid4()),
                "amount_claimed": np.random.randint(1000, 20000),
                "status": np.random.choice(["approved", "pending", "denied"]),
                "filed_date": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_insured_entities(count: int) -> List[dict]:
        """Gera entidades seguradas como dicionários."""
        return [
            {
                "id": next(counter),
                "entity_id": str(uuid4()),
                "type": np.random.choice(["vehicle", "property", "life"]),
                "description": fake.sentence(),
                "value": np.random.randint(10000, 100000),
            }
            for _ in range(count)
        ]
