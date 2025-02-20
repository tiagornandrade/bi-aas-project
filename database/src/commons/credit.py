import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List

fake = Faker("pt_BR")


class CreditsEvents:
    @staticmethod
    def generate_credit_score(count: object) -> List[dict]:
        """Gera pontuações de crédito como dicionários.

        Cria um dicionário de pontuações de crédito, com informações como ID, ID do usuário, pontuação e data da última atualização.
        """
        return [
            {
                "score_id": str(uuid4()),
                "user_id": str(uuid4()),
                "score": np.random.randint(1, 1000),
                "last_updated": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_risk_assessment(count: object) -> List[dict]:
        """Gera avaliações de risco como dicionários.

        Cria um dicionário de avaliações de risco, com informações como ID, ID do usuário, nível de risco, detalhes e data.
        """
        return [
            {
                "assessment_id": str(uuid4()),
                "user_id": str(uuid4()),
                "risk_level": np.random.choice(["low", "medium", "high"]),
                "details": fake.sentence(),
                "date": fake.date_this_year(),
            }
            for _ in range(count)
        ]
