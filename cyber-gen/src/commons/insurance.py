import random
from uuid import uuid4
from faker import Faker
from typing import List, Dict
from datetime import datetime

fake = Faker("pt_BR")


class InsuranceEvents:
    """Gera dados sintéticos para apólices de seguro, reivindicações e entidades seguradas."""

    @staticmethod
    def generate_policies(count: int) -> List[Dict]:
        """Gera apólices de seguro como dicionários."""
        return [
            {
                "table_name": "policies",
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
    def generate_claims(count: int) -> List[Dict]:
        """Gera reivindicações de seguro como dicionários."""
        return [
            {
                "table_name": "claims",
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
    def generate_insured_entities(count: int) -> List[Dict]:
        """Gera entidades seguradas como dicionários."""
        return [
            {
                "table_name": "insured_entities",
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
