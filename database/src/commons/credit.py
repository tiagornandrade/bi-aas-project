import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List

fake = Faker("pt_BR")


class CreditsEvents:
    """Gera dados sintéticos para pontuações de crédito e avaliações de risco."""

    @staticmethod
    def generate_credit_scores(count: int) -> List[dict]:
        """Gera pontuações de crédito como dicionários."""
        return [
            {
                "score_id": str(uuid4()),
                "user_id": str(uuid4()),
                "score": np.random.randint(300, 850),
                "last_updated": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_risk_assessments(count: int) -> List[dict]:
        """Gera avaliações de risco como dicionários."""
        return [
            {
                "assessment_id": str(uuid4()),
                "user_id": str(uuid4()),
                "risk_level": np.random.choice(["low", "medium", "high"]),
                "details": fake.sentence(),
                "date": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]
