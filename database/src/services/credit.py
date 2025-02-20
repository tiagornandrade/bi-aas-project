import logging
from utils.db import SessionLocal
from models.credit import CreditScore, RiskAssessment
from commons.credit import CreditsEvents

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CreditService:
    @staticmethod
    def insert_credit_scores(count: int):
        """Insere pontuações de crédito no banco de dados."""
        db = SessionLocal()
        try:
            scores_dicts = CreditsEvents.generate_credit_scores(count)
            scores = [CreditScore(**score_dict) for score_dict in scores_dicts]

            db.bulk_save_objects(scores)
            db.commit()

            logging.info(f"{count} pontuações de crédito inseridas com sucesso.")
            return (
                db.query(CreditScore).order_by(CreditScore.id.desc()).limit(count).all()
            )
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir pontuações de crédito: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def insert_risk_assessments(count: int):
        """Insere avaliações de risco no banco de dados."""
        db = SessionLocal()
        try:
            assessments_dicts = CreditsEvents.generate_risk_assessments(count)
            assessments = [
                RiskAssessment(**assessment_dict)
                for assessment_dict in assessments_dicts
            ]

            db.bulk_save_objects(assessments)
            db.commit()

            logging.info(f"{count} avaliações de risco inseridas com sucesso.")
            return (
                db.query(RiskAssessment)
                .order_by(RiskAssessment.id.desc())
                .limit(count)
                .all()
            )
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir avaliações de risco: {e}")
            return []
        finally:
            db.close()
