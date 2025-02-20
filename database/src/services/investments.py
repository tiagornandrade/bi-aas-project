import logging
from utils.db import SessionLocal
from models.investments import Portfolio
from commons.investments import InvestmentsEvents

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class PortfolioService:
    @staticmethod
    def insert_portfolios(count: int):
        """Insere portfólios no banco de dados."""
        db = SessionLocal()
        try:
            portfolios_dicts = InvestmentsEvents.generate_portfolios(count)
            portfolios = [
                Portfolio(**portfolio_dict) for portfolio_dict in portfolios_dicts
            ]

            db.bulk_save_objects(portfolios)
            db.commit()

            logging.info(f"{count} portfólios inseridos com sucesso.")
            return db.query(Portfolio).order_by(Portfolio.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir portfólios: {e}")
            return []
        finally:
            db.close()
