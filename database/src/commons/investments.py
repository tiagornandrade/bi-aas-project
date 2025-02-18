
import os
import numpy as np
from uuid import uuid4
from faker import Faker


fake = Faker("pt_BR")


class InvestimentsEvents:
    @staticmethod
    def generate_portfolio(x: object) -> object:
        return {
            data: {
                "portfolio_id": str(uuid4()),
                "user_id": str(uuid4()),
                "total_value": np.random.randint(1, 1000),
                "risk_profile": np.random.choice(["low", "medium", "high"]),
            }
            for data in range(x)
        }

    @staticmethod
    def generate_transaction(x: object) -> object:
        return {
            data: {
                "transaction_id": str(uuid4()),
                "portfolio_id": str(uuid4()),
                "asset_id": str(uuid4()),
                "amount": np.random.randint(1, 1000),
                "price": np.random.randint(1, 1000),
                "timestamp": fake.date_time_this_year(),
            }
            for data in range(x)
        }

    @staticmethod
    def generate_portfolio(x: object) -> object:
        return {
            data: {
                "portfolio_id": str(uuid4()),
                "user_id": str(uuid4()),
                "total_value": np.random.randint(1, 1000),
                "risk_profile": np.random.choice(["low", "medium", "high"]),
            }
            for data in range(x)
        }
