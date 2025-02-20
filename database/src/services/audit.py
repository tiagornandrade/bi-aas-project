import logging
from utils.db import SessionLocal
from models.audit import Audit
from commons.audits import AuditsEvents

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class AuditService:
    @staticmethod
    def insert_audits(count: int):
        """Insere auditorias no banco de dados e retorna os objetos inseridos"""
        db = SessionLocal()
        try:
            audit_dicts = AuditsEvents.generate_audits(count)
            audits = [Audit(**audit_dict) for audit_dict in audit_dicts]

            db.bulk_save_objects(audits)
            db.commit()

            inserted_audits = (
                db.query(Audit).order_by(Audit.audit_id.desc()).limit(count).all()
            )
            logging.info(f"{count} auditorias inseridas com sucesso.")
            return inserted_audits
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir auditorias: {e}")
            return []
        finally:
            db.close()
