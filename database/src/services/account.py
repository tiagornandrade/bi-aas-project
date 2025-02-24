import logging
import numpy as np
from sqlalchemy.exc import SQLAlchemyError
from src.utils.db import SessionLocal
from src.models.account import Account, Subaccount, User
from src.commons.accounts import AccountEvents

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class AccountService:
    @staticmethod
    def insert_users(count: int, batch_size: int = 100):
        """Insere usuários no banco de dados em lotes menores"""
        db = SessionLocal()
        try:
            user_dicts = AccountEvents.generate_users(count)
            users = [User(**txn_dict) for txn_dict in user_dicts]

            db.bulk_save_objects(users)
            db.commit()

            logging.info(f"{count} usuários inseridos com sucesso.")
            return db.query(User).order_by(User.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir usuários: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_accounts(count: int, batch_size: int = 100):
        """Insere contas garantindo que os usuários existam"""
        db = SessionLocal()
        try:
            account_dicts = AccountEvents.accounts(count)
            accounts = [Account(**txn_dict) for txn_dict in account_dicts]

            db.bulk_save_objects(accounts)
            db.commit()

            logging.info(f"{count} contas inseridas com sucesso.")
            return db.query(Account).order_by(Account.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir contas: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_subaccounts(count: int, batch_size: int = 100):
        """Insere subcontas garantindo que as contas existam"""
        db = SessionLocal()
        try:
            subaccount_dicts = AccountEvents.subaccounts(count)
            subaccounts = [Subaccount(**txn_dict) for txn_dict in subaccount_dicts]

            db.bulk_save_objects(subaccounts)
            db.commit()

            logging.info(f"{count} subcontas inseridas com sucesso.")
            return (
                db.query(Subaccount).order_by(Subaccount.id.desc()).limit(count).all()
            )
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir subcontas: {e}")
            return []
        finally:
            db.close()
