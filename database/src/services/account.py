import numpy as np
from sqlalchemy.exc import SQLAlchemyError
from src.utils.db import SessionLocal
from src.models.account import Account, Subaccount, User
from src.commons.accounts import AccountEvents


class AccountService:
    @staticmethod
    def insert_users(count: int, batch_size: int = 100):
        """Insere usuários no banco de dados em lotes menores"""
        db = SessionLocal()
        try:
            user_dicts = AccountEvents.generate_users(count)
            batches = [
                user_dicts[i : i + batch_size]
                for i in range(0, len(user_dicts), batch_size)
            ]

            for batch in batches:
                users = [User(**user) for user in batch]
                db.bulk_save_objects(users)
                db.commit()

            return db.query(User).order_by(User.id.desc()).limit(count).all()
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao inserir usuários: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_accounts(count: int, batch_size: int = 100):
        """Insere contas garantindo que os usuários existam"""
        db = SessionLocal()
        try:
            existing_users = [
                user[0] for user in db.query(User.user_id).yield_per(100).all()
            ]
            if not existing_users:
                print("⚠️ Nenhum usuário encontrado para associar contas!")
                return []

            account_dicts = AccountEvents.generate_accounts(count)
            valid_accounts = [
                Account(**{**account, "user_id": np.random.choice(existing_users)})
                for account in account_dicts
            ]

            batches = [
                valid_accounts[i : i + batch_size]
                for i in range(0, len(valid_accounts), batch_size)
            ]
            for batch in batches:
                db.bulk_save_objects(batch)
                db.commit()

            return db.query(Account).order_by(Account.id.desc()).limit(count).all()
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao inserir contas: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_subaccounts(count: int, batch_size: int = 100):
        """Insere subcontas garantindo que as contas existam"""
        db = SessionLocal()
        try:
            existing_accounts = [
                account[0]
                for account in db.query(Account.account_id).yield_per(100).all()
            ]
            if not existing_accounts:
                print("⚠️ Nenhuma conta encontrada para associar subcontas!")
                return []

            subaccount_dicts = AccountEvents.generate_subaccounts(count)
            valid_subaccounts = [
                Subaccount(
                    **{
                        **subaccount,
                        "parent_account_id": np.random.choice(existing_accounts),
                    }
                )
                for subaccount in subaccount_dicts
            ]

            batches = [
                valid_subaccounts[i : i + batch_size]
                for i in range(0, len(valid_subaccounts), batch_size)
            ]
            for batch in batches:
                db.bulk_save_objects(batch)
                db.commit()

            return (
                db.query(Subaccount).order_by(Subaccount.id.desc()).limit(count).all()
            )
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao inserir subcontas: {e}")
            return []
        finally:
            db.close()
