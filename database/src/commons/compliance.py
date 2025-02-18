
import os
import numpy as np
from uuid import uuid4
from faker import Faker


fake = Faker("pt_BR")


class CompliancesEvents:
    @staticmethod
    def generate_regulation(x: object) -> object:
        return {
            data: {
                "regulation_id": str(uuid4()),
                "name": fake.word(),
                "description": fake.sentence(),
                "jurisdiction": fake.word(),
            }
            for data in range(x)
        }

    @staticmethod
    def generate_audit(x: object) -> object:
        return {
            data: {
                "audit_id": str(uuid4()),
                "entity_id": str(uuid4()),
                "status": np.random.choice(["pending", "completed"]),
                "findings": fake.sentence(),
                "date": fake.date_this_year(),
            }
            for data in range(x)
        }

    @staticmethod
    def generate_user_verification(x: object) -> object:
        return {
            data: {
                "verification_id": str(uuid4()),
                "user_id": str(uuid4()),
                "type": np.random.choice(["KYC", "AML"]),
                "status": np.random.choice(["pending", "approved", "rejected"]),
                "date": fake.date_this_year(),
            }
            for data in range(x)
        }
