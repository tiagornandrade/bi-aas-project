import logging
from src.utils.db import SessionLocal
from src.models.lending import Loan, Payment
from src.commons.lending import LendingEvents

logger = logging.getLogger(__name__)


class LoanService:
    @staticmethod
    def insert_loans(count: int):
        """Insere empréstimos no banco de dados."""
        db = SessionLocal()
        try:
            loans_dicts = LendingEvents.generate_loans(count)
            loans = [Loan(**loan_dict) for loan_dict in loans_dicts]

            db.bulk_save_objects(loans)
            db.commit()

            logging.info(f"{count} empréstimos inseridos com sucesso.")
            return db.query(Loan).order_by(Loan.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir empréstimos: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_payments(count: int):
        """Insere pagamentos no banco de dados."""
        db = SessionLocal()
        try:
            payments_dicts = LendingEvents.generate_payments(count)
            payments = [Payment(**payment_dict) for payment_dict in payments_dicts]

            db.bulk_save_objects(payments)
            db.commit()

            logging.info(f"{count} pagamentos inseridos com sucesso.")
            return db.query(Payment).order_by(Payment.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir pagamentos: {e}")
            return []
        finally:
            db.close()
