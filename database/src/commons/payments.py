import numpy as np
from uuid import uuid4
from faker import Faker
from datetime import datetime
from typing import List
from models.payment import Transaction, PaymentMethod, Merchant

fake = Faker("pt_BR")


def generate_transactions(count: int) -> List[Transaction]:
    return [
        Transaction(
            transaction_id=str(uuid4()),
            amount=np.random.randint(1, 1000),
            currency="BRL",
            status=np.random.choice(["approved", "declined"]),
            timestamp=fake.date_time_this_year(),
            sender_id=str(uuid4()),
            receiver_id=str(uuid4()),
        )
        for _ in range(count)
    ]


def generate_payment_methods(count: int) -> List[PaymentMethod]:
    return [
        PaymentMethod(
            method_id=str(uuid4()),
            type=np.random.choice(["credit card", "PIX"]),
            details=fake.credit_card_number(),
            user_id=str(uuid4()),
        )
        for _ in range(count)
    ]


def generate_merchants(count: int) -> List[Merchant]:
    return [
        Merchant(
            merchant_id=str(uuid4()),
            name=fake.company(),
            category=np.random.choice(["restaurant", "market", "pharmacy"]),
            contact_info=fake.phone_number(),
        )
        for _ in range(count)
    ]