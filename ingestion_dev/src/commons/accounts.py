import random
from uuid import uuid4
from faker import Faker
from typing import List, Dict
from datetime import datetime

fake = Faker("pt_BR")


class AccountEvents:

    @staticmethod
    def generate_accounts(count: int) -> List[Dict]:
        """Gera eventos de contas no formato compatível com a tabela 'accounts'."""
        return [
            {
                "table_name": "accounts",
                "event_uuid": str(uuid4()),
                "event_type": random.choice(["insert", "update", "delete"]),
                "event_timestamp": datetime.utcnow(),
                "payload": {
                    "account_id": str(uuid4()),
                    "user_id": str(uuid4()),
                    "balance": round(random.uniform(100, 10000), 2),
                    "currency": random.choice(["USD", "BRL", "EUR"]),
                    "created_at": fake.date_time_this_year().isoformat(),
                    "account_type": random.choice(["personal", "business"]),
                },
                "ingested_at": datetime.utcnow(),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_subaccounts(count: int) -> List[Dict]:
        """Gera eventos de subcontas no formato compatível com a tabela 'subaccounts'."""
        return [
            {
                "table_name": "subaccounts",
                "event_uuid": str(uuid4()),
                "event_type": random.choice(["insert", "update", "delete"]),
                "event_timestamp": datetime.utcnow(),
                "payload": {
                    "subaccount_id": str(uuid4()),
                    "parent_account_id": str(uuid4()),
                    "balance": round(random.uniform(50, 5000), 2),
                    "created_at": fake.date_time_this_year().isoformat(),
                },
                "ingested_at": datetime.utcnow(),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_users(count: int) -> List[Dict]:
        """Gera eventos de usuários no formato compatível com a tabela 'users'."""
        return [
            {
                "table_name": "users",
                "event_uuid": str(uuid4()),
                "event_type": random.choice(["insert", "update", "delete"]),
                "event_timestamp": datetime.utcnow(),
                "payload": {
                    "user_id": str(uuid4()),
                    "name": fake.name(),
                    "email": fake.email(),
                    "phone": fake.phone_number(),
                    "created_at": fake.date_time_this_year().isoformat(),
                },
                "ingested_at": datetime.utcnow(),
            }
            for _ in range(count)
        ]