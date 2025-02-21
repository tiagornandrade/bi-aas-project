import itertools
import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List


fake = Faker("pt_BR")

counter = itertools.count(start=1)


class LendingEvents:
    @staticmethod
    def generate_loans(count: int) -> List[dict]:
        """Gera empréstimos como dicionários."""
        return [
            {
                "id": next(counter),
                "loan_id": str(uuid4()),
                "user_id": str(uuid4()),
                "amount": np.random.randint(1000, 50000),
                "interest_rate": np.random.uniform(2.5, 15.0),
                "term": np.random.randint(12, 60),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_payments(count: int) -> List[dict]:
        """Gera pagamentos de empréstimos como dicionários."""
        return [
            {
                "id": next(counter),
                "payment_id": str(uuid4()),
                "loan_id": str(uuid4()),
                "amount": np.random.randint(100, 2000),
                "date": fake.date_time_this_year(),
                "status": np.random.choice(["completed", "pending", "failed"]),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_credit_score(count: object) -> List[dict]:
        """Gera pontuações de crédito como dicionários.

        Cria um dicionário de pontuações de crédito, com informações como ID, ID do usuário, pontuação e data da última atualização.
        """
        return [
            {
                "id": next(counter),
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
                "id": next(counter),
                "assessment_id": str(uuid4()),
                "user_id": str(uuid4()),
                "risk_level": np.random.choice(["low", "medium", "high"]),
                "details": fake.sentence(),
                "date": fake.date_this_year(),
            }
            for _ in range(count)
        ]
