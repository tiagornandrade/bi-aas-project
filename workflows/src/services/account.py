import logging
from utils.db import SessionLocal
from models.account import Account, Subaccount, User
from commons.accounts import AccountEvents

logger = logging.getLogger(__name__)


class AccountService:
    @staticmethod
    def insert_users(count, db=None):
        db = db or SessionLocal()
        try:
            users_dicts = AccountEvents.generate_users(count)
            users = [User(**users_dict) for users_dict in users_dicts]
            db.add_all(users)
            db.commit()
            return users
        except Exception as e:
            db.rollback()
            print(f"Erro ao inserir usuários: {e}")
            return []

    @staticmethod
    def insert_accounts(count, db=None):
        """Insere contas no banco de dados."""
        db = db or SessionLocal()
        try:
            account_dicts = AccountEvents.generate_accounts(count)
            accounts = [Account(**account_dict) for account_dict in account_dicts]
            db.add_all(accounts)
            db.commit()
            return accounts
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao inserir contas: {e}")
            return []

    @staticmethod
    def insert_subaccounts(count, db=None):
        """Insere subcontas no banco de dados."""
        db = db or SessionLocal()
        try:
            subaccount_dicts = AccountEvents.generate_subaccounts(count)
            subaccounts = [
                Subaccount(**subaccount_dict) for subaccount_dict in subaccount_dicts
            ]
            db.add_all(subaccounts)
            db.commit()
            return subaccounts
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao inserir subcontas: {e}")
            return []
