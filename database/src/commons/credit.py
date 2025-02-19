import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List, Any

fake = Faker("pt_BR")


class CreditsEvents:
    @staticmethod
    def generate_credit_score(x: object) -> List[dict[Any, Any]]:
        """Gera pontuações de crédito como dicionários.

        Cria um dicionário de pontuações de crédito, com informações como ID, ID do usuário, pontuação e data da última atualização.
        """
        return {
            data: {
                "score_id": str(uuid4()),
                "user_id": str(uuid4()),
                "score": np.random.randint(1, 1000),
                "last_updated": fake.date_time_this_year(),
            }
            for data in range(x)
        }

    @staticmethod
    def generate_risk_assessment(x: object) -> List[dict]:
        """Gera avaliações de risco como dicionários.

        Cria um dicionário de avaliações de risco, com informações como ID, ID do usuário, nível de risco, detalhes e data.
        """
        return {
            data: {
                "assessment_id": str(uuid4()),
                "user_id": str(uuid4()),
                "risk_level": np.random.choice(["low", "medium", "high"]),
                "details": fake.sentence(),
                "date": fake.date_this_year(),
            }
            for data in range(x)
        }
