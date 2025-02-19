from utils.db import SessionLocal
from models.compliance import Regulation, UserVerification
from commons.compliance import CompliancesEvents

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ComplianceService:
    @staticmethod
    def insert_regulations(count: int):
        """Insere regulamentações no banco de dados."""
        db = SessionLocal()
        try:
            regulations_dicts = CompliancesEvents.generate_regulations(count)
            regulations = [Regulation(**reg_dict) for reg_dict in regulations_dicts]

            db.bulk_save_objects(regulations)
            db.commit()

            logging.info(f"{count} regulamentações inseridas com sucesso.")
            return (
                db.query(Regulation).order_by(Regulation.id.desc()).limit(count).all()
            )
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir regulamentações: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_user_verification(count: int):
        """Insere verificações de usuário no banco de dados."""
        db = SessionLocal()
        try:
            verifications_dicts = CompliancesEvents.generate_user_verifications(count)
            verifications = [
                UserVerification(**ver_dict) for ver_dict in verifications_dicts
            ]

            db.bulk_save_objects(verifications)
            db.commit()

            logging.info(f"{count} verificações de usuário inseridas com sucesso.")
            return (
                db.query(UserVerification)
                .order_by(UserVerification.id.desc())
                .limit(count)
                .all()
            )
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir verificações de usuário: {e}")
            return []
        finally:
            db.close()
