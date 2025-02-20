import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List
from models.payment import Transaction, PaymentMethod, Merchant

fake = Faker("pt_BR")


class PaymentsEvents:
    @staticmethod
    def generate_transactions(count: int) -> List[dict]:
        """Gera transações.

        Cria uma lista de transações, com informações como ID, valor, moeda, status, timestamp, ID do remetente e ID do destinatário.
        """
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

    @staticmethod
    def generate_payment_methods(count: int) -> List[dict]:
        """Gera métodos de pagamento.

        Cria uma lista de métodos de pagamento, com informações como ID, tipo, detalhes e ID do usuário.
        """
        return [
            PaymentMethod(
                method_id=str(uuid4()),
                type=np.random.choice(["credit card", "PIX"]),
                details=fake.credit_card_number(),
                user_id=str(uuid4()),
            )
            for _ in range(count)
        ]

    @staticmethod
    def generate_merchants(count: int) -> List[dict]:
        """Gera comerciantes.

        Cria uma lista de comerciantes, com informações como ID, nome, categoria e informações de contato.
        """
        return [
            Merchant(
                merchant_id=str(uuid4()),
                name=fake.company(),
                category=np.random.choice(["restaurant", "market", "pharmacy"]),
                contact_info=fake.phone_number(),
            )
            for _ in range(count)
        ]
