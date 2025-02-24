import logging
from src.utils.db import SessionLocal
from src.models.account import Account, Subaccount, User
from src.commons.accounts import AccountEvents

logger = logging.getLogger(__name__)


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
    def insert_accounts(count: int):
        """Insere contas no banco de dados."""
        db = SessionLocal()
        try:
            accounts_dicts = AccountEvents.generate_accounts(count)
            accounts = [Account(**acc_dict) for acc_dict in accounts_dicts]

            db.bulk_save_objects(accounts)
            db.commit()

            logger.info(f"{count} contas inseridas com sucesso.")
            return db.query(Account).order_by(Account.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao inserir contas: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_subaccounts(count: int):
        """Insere subcontas no banco de dados."""
        db = SessionLocal()
        try:
            subaccounts_dicts = AccountEvents.generate_subaccounts(count)
            subaccounts = [Subaccount(**sub_dict) for sub_dict in subaccounts_dicts]

            db.bulk_save_objects(subaccounts)
            db.commit()

            logger.info(f"{count} subcontas inseridas com sucesso.")
            return db.query(Subaccount).order_by(Subaccount.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao inserir subcontas: {e}")
            return []
        finally:
            db.close()

