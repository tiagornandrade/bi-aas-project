import random
from uuid import uuid4
from faker import Faker
from typing import List, Dict
from datetime import datetime

fake = Faker("pt_BR")


class CompliancesEvents:
    """Gera dados sintéticos para regulamentações, auditorias e verificações de usuários."""

    @staticmethod
    def generate_regulations(count: int) -> List[Dict]:
        """Gera regulamentações como dicionários."""
        return [
            {
                "table_name": "regulations",
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
    def generate_user_verifications(count: int) -> List[Dict]:
        """Gera verificações de usuários como dicionários."""
        return [
            {
                "table_name": "user_verifications",
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
