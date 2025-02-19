import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List

fake = Faker("pt_BR")


class AccountEvents:
    @staticmethod
    def generate_accounts(count: int) -> List[dict]:
        """Gera contas como dicionários.

        Cria uma lista de dicionários, onde cada dicionário representa
        uma conta com detalhes como ID, tipo, saldo, moeda, status e ID do usuário.
        """
        return [
            {
                "account_id": str(uuid4()),
                "account_type": np.random.choice(["personal", "business"]),
                "balance": np.random.randint(1, 1000),
                "currency": np.random.choice(["BRL", "USD"]),
                "status": np.random.choice(["active", "inactive"]),
                "user_id": str(uuid4()),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_subaccounts(count: int) -> List[dict]:
        """Gera subcontas como dicionários.

        Cria uma lista de dicionários, onde cada dicionário representa
        uma subconta com detalhes como ID, ID da conta pai, propósito e saldo.
        """
        return [
            {
                "subaccount_id": str(uuid4()),
                "parent_account_id": str(uuid4()),
                "purpose": np.random.choice(["savings", "investment"]),
                "balance": np.random.randint(1, 1000),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_users(count: int) -> List[dict]:
        """Gera usuários como dicionários.

        Cria uma lista de dicionários, onde cada dicionário representa
        um usuário com detalhes como ID, nome, e-mail, telefone e data de criação.
        """
        return [
            {
                "user_id": str(uuid4()),
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "created_at": fake.date_time_this_year(),
            }
            for _ in range(count)
        ]
