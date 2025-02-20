import logging
from utils.db import SessionLocal
from models.payment import Transaction, PaymentMethod, Merchant
from commons.payments import PaymentsEvents

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TransactionService:
    @staticmethod
    def insert_transactions(count: int):
        """Insere transações no banco de dados."""
        db = SessionLocal()
        try:
            transactions_dicts = PaymentsEvents.generate_transactions(count)
            transactions = [Transaction(**txn_dict) for txn_dict in transactions_dicts]

            db.bulk_save_objects(transactions)
            db.commit()

            logging.info(f"{count} transações inseridas com sucesso.")
            return (
                db.query(Transaction).order_by(Transaction.id.desc()).limit(count).all()
            )
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir transações: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_payment_methods(count: int):
        """Insere métodos de pagamento no banco de dados."""
        db = SessionLocal()
        try:
            payment_methods_dicts = PaymentsEvents.generate_payment_methods(count)
            payment_methods = [
                PaymentMethod(**pm_dict) for pm_dict in payment_methods_dicts
            ]

            db.bulk_save_objects(payment_methods)
            db.commit()

            logging.info(f"{count} métodos de pagamento inseridos com sucesso.")
            return (
                db.query(PaymentMethod)
                .order_by(PaymentMethod.id.desc())
                .limit(count)
                .all()
            )
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir métodos de pagamento: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_merchants(count: int):
        """Insere comerciantes no banco de dados."""
        db = SessionLocal()
        try:
            merchants_dicts = PaymentsEvents.generate_merchants(count)
            merchants = [Merchant(**merchant_dict) for merchant_dict in merchants_dicts]

            db.bulk_save_objects(merchants)
            db.commit()

            logging.info(f"{count} comerciantes inseridos com sucesso.")
            return db.query(Merchant).order_by(Merchant.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir comerciantes: {e}")
            return []
        finally:
            db.close()
