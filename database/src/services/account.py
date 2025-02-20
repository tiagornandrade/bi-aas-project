import numpy as np
from src.utils.db import SessionLocal, engine
from src.models.account import Account, Subaccount, User
from src.commons.accounts import AccountEvents


class AccountService:
    @staticmethod
    def insert_users(count: int):
        """Insere usuários no banco de dados e retorna os objetos inseridos"""
        db = SessionLocal()
        try:
            user_dicts = AccountEvents.generate_users(count)
            users = [User(**user) for user in user_dicts]

            db.bulk_save_objects(users)
            db.commit()

            return db.query(User).order_by(User.user_id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            print(f"Erro ao inserir usuários: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_accounts(count: int):
        """Insere contas garantindo que os usuários existam"""
        db = SessionLocal()
        try:
            existing_users = db.query(User.user_id).all()
            user_ids = [user[0] for user in existing_users]

            account_dicts = AccountEvents.generate_accounts(count)
            valid_accounts = [
                Account(**{**account, "user_id": np.random.choice(user_ids)})
                for account in account_dicts
            ]

            db.bulk_save_objects(valid_accounts)
            db.commit()

            return (
                db.query(Account).order_by(Account.account_id.desc()).limit(count).all()
            )
        except Exception as e:
            db.rollback()
            print(f"Erro ao inserir contas: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_subaccounts(count: int):
        """Insere subcontas garantindo que as contas existam"""
        db = SessionLocal()
        try:
            existing_accounts = db.query(Account.account_id).all()
            account_ids = [account[0] for account in existing_accounts]

            subaccount_dicts = AccountEvents.generate_subaccounts(count)
            valid_subaccounts = [
                Subaccount(
                    **{**subaccount, "parent_account_id": np.random.choice(account_ids)}
                )
                for subaccount in subaccount_dicts
            ]

            db.bulk_save_objects(valid_subaccounts)
            db.commit()

            return (
                db.query(Subaccount)
                .order_by(Subaccount.subaccount_id.desc())
                .limit(count)
                .all()
            )
        except Exception as e:
            db.rollback()
            print(f"Erro ao inserir subcontas: {e}")
            return []
        finally:
            db.close()
