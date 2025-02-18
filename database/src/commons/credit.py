
import os
import numpy as np
from uuid import uuid4
from faker import Faker


fake = Faker("pt_BR")


class CreditsEvents:
    @staticmethod
    def generate_credit_score(x: object) -> object:
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
    def generate_risk_assessment(x: object) -> object:
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

    @staticmethod
    def generate_user(x: object) -> object:
        return {
            data: {
                "user_id": str(uuid4()),
                "name": fake.name(),
                "income": np.random.randint(1, 1000),
                "debt": np.random.randint(1, 1000),
            }
            for data in range(x)
        }
