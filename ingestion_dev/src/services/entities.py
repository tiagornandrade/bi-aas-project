import logging
from utils.db import SessionLocal
from models.entities import Entity
from commons.entities import EntityEvents

logger = logging.getLogger(__name__)


class EntityService:
    @staticmethod
    def insert_entities(count: int):
        """Insere entidades no banco de dados."""
        db = SessionLocal()
        try:
            entities_dicts = EntityEvents.generate_entities(count)
            entities = [Entity(**entity_dict) for entity_dict in entities_dicts]

            db.bulk_save_objects(entities)
            db.commit()

            logging.info(f"{count} entidades inseridas com sucesso.")
            return db.query(Entity).order_by(Entity.id.desc()).limit(count).all()
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao inserir entidades: {e}")
            return []
        finally:
            db.close()
