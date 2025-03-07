import logging
from src.utils.db import SessionLocal
from src.models.audit import Audit
from src.commons.audits import AuditsEvents

logger = logging.getLogger(__name__)


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
                db.query(Audit).order_by(Audit.id.desc()).limit(count).all()
            )
            logging.info(f"{count} auditorias inseridas com sucesso.")
            return inserted_audits
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir auditorias: {e}")
            return []
        finally:
            db.close()
