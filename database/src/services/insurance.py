import logging
from utils.db import SessionLocal
from models.insurance import Policy, Claim, InsuredEntity
from commons.insurance import InsuranceEvents

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class InsuranceService:
    @staticmethod
    def insert_policies(count: int):
        """Insere apólices de seguro no banco de dados."""
        db = SessionLocal()
        try:
            policies_dicts = InsuranceEvents.generate_policies(count)
            policies = [Policy(**policy_dict) for policy_dict in policies_dicts]

            db.bulk_save_objects(policies)
            db.commit()

            logging.info(f"{count} apólices inseridas com sucesso.")
            return db.query(Policy).order_by(Policy.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir apólices: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_claims(count: int):
        """Insere reivindicações de seguro no banco de dados."""
        db = SessionLocal()
        try:
            claims_dicts = InsuranceEvents.generate_claims(count)
            claims = [Claim(**claim_dict) for claim_dict in claims_dicts]

            db.bulk_save_objects(claims)
            db.commit()

            logging.info(f"{count} reivindicações inseridas com sucesso.")
            return db.query(Claim).order_by(Claim.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir reivindicações: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_insured_entities(count: int):
        """Insere entidades seguradas no banco de dados."""
        db = SessionLocal()
        try:
            entities_dicts = InsuranceEvents.generate_insured_entities(count)
            entities = [InsuredEntity(**entity_dict) for entity_dict in entities_dicts]

            db.bulk_save_objects(entities)
            db.commit()

            logging.info(f"{count} entidades seguradas inseridas com sucesso.")
            return (
                db.query(InsuredEntity)
                .order_by(InsuredEntity.id.desc())
                .limit(count)
                .all()
            )
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir entidades seguradas: {e}")
            return []
        finally:
            db.close()
