import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List


fake = Faker("pt_BR")


class InvestimentsEvents:
    @staticmethod
    def generate_portfolio(count: object) -> List[dict]:
        """Gera carteiras como dicionários.

        Cria um dicionário de carteiras, com informações como ID, ID do usuário, valor total e perfil de risco.
        """
        return [
            {
                "portfolio_id": str(uuid4()),
                "user_id": str(uuid4()),
                "total_value": np.random.randint(1, 1000),
                "risk_profile": np.random.choice(["low", "medium", "high"]),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_transaction(count: object) -> List[dict]:
        """Gera transações como dicionários.

        Cria um dicionário de transações, com informações como ID, ID da carteira, ID do ativo, quantidade, preço e timestamp.
        """
        return [
            {
                "transaction_id": str(uuid4()),
                "portfolio_id": str(uuid4()),
                "asset_id": str(uuid4()),
                "amount": np.random.randint(1, 1000),
                "price": np.random.randint(1, 1000),
                "timestamp": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_portfolio(count: object) -> List[dict]:
        """Gera carteiras como dicionários.

        Cria um dicionário de carteiras, com informações como ID, ID do usuário, valor total e perfil de risco.
        """
        return [
            {
                "portfolio_id": str(uuid4()),
                "user_id": str(uuid4()),
                "total_value": np.random.randint(1, 1000),
                "risk_profile": np.random.choice(["low", "medium", "high"]),
            }
            for _ in range(count)
        ]
