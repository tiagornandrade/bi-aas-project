import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List


fake = Faker("pt_BR")


class LendingEvents:
    @staticmethod
    def generate_loan(x: object) -> List[dict]:
        """Gera empréstimos como dicionários.

        Cria um dicionário de empréstimos, com informações como ID, ID do usuário, valor, taxa de juros, prazo e data de criação.
        """
        return {
            data: {
                "loan_id": str(uuid4()),
                "user_id": str(uuid4()),
                "amount": np.random.randint(1, 1000),
                "interest_rate": np.random.uniform(0, 0.5),
                "term": np.random.randint(1, 36),
                "created_at": fake.date_time_this_year(),
            }
            for data in range(x)
        }

    @staticmethod
    def generate_payment(x: object) -> List[dict]:
        """Gera pagamentos como dicionários.

        Cria um dicionário de pagamentos, com informações como ID, ID do empréstimo, valor, data e status.
        """
        return {
            data: {
                "payment_id": str(uuid4()),
                "loan_id": str(uuid4()),
                "amount": np.random.randint(1, 1000),
                "date": fake.date_this_year(),
                "status": np.random.choice(["pending", "completed"]),
            }
            for data in range(x)
        }

    @staticmethod
    def generate_credit_score(x: object) -> List[dict]:
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
