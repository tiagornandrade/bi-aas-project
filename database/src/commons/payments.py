import itertools
import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List

fake = Faker("pt_BR")

counter = itertools.count(start=1)


class PaymentsEvents:
    """Gera dados sintéticos para transações financeiras."""

    @staticmethod
    def generate_transactions(count: int) -> List[dict]:
        """Gera transações como dicionários."""
        return [
            {
                "id": next(counter),
                "transaction_id": str(uuid4()),
                "amount": np.random.randint(10, 5000),
                "currency": np.random.choice(["BRL", "USD", "EUR"]),
                "status": np.random.choice(["completed", "pending", "failed"]),
                "timestamp": fake.date_time_this_year(),
                "sender_id": str(uuid4()),
                "receiver_id": str(uuid4()),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_payment_methods(count: int) -> List[dict]:
        """Gera métodos de pagamento como dicionários."""
        return [
            {
                "id": next(counter),
                "method_id": str(uuid4()),
                "type": np.random.choice(
                    ["credit_card", "debit_card", "pix", "paypal"]
                ),
                "details": fake.credit_card_number(),
                "user_id": str(uuid4()),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_merchants(count: int) -> List[dict]:
        """Gera comerciantes como dicionários."""
        return [
            {
                "id": next(counter),
                "merchant_id": str(uuid4()),
                "name": fake.company(),
                "category": np.random.choice(["retail", "services", "ecommerce"]),
                "contact_info": fake.email(),
            }
            for _ in range(count)
        ]
