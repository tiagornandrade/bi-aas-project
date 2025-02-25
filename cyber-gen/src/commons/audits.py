import random
from uuid import uuid4
from faker import Faker
from typing import List, Dict
from datetime import datetime

fake = Faker("pt_BR")


class AuditsEvents:
    @staticmethod
    def generate_audits(count: int) -> List[Dict]:
        """Gera auditorias como dicionários."""
        return [
            {
                "table_name": "audits",
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
