import random
from uuid import uuid4
from faker import Faker
from typing import List, Dict
from datetime import datetime

fake = Faker("pt_BR")


class CreditsEvents:
    """Gera dados sintéticos para pontuações de crédito e avaliações de risco."""

    @staticmethod
    def generate_credit_scores(count: int) -> List[Dict]:
        """Gera pontuações de crédito como dicionários."""
        return [
            {
                "table_name": "credit_scores",
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
    def generate_risk_assessments(count: int) -> List[Dict]:
        """Gera avaliações de risco como dicionários."""
        return [
            {
                "table_name": "risk_assessments",
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
