import numpy as np
from uuid import uuid4
from faker import Faker
from datetime import datetime
from typing import List

fake = Faker("pt_BR")


class AccountEventsService:
    @staticmethod
    def generate_accounts(count: int) -> List[dict]:
        """Gera contas como dicionários"""
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
        """Gera subcontas como dicionários"""
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
        """Gera usuários como dicionários"""
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
