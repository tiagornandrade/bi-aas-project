import numpy as np
from uuid import uuid4
from faker import Faker
from typing import List

fake = Faker("pt_BR")


class EntityEvents:
    """Gera dados sintéticos para a tabela entities."""

    @staticmethod
    def generate_entities(count: int) -> List[dict]:
        """Gera entidades como dicionários.

        Cria uma lista de dicionários, onde cada dicionário representa
        uma entidade com detalhes como ID e nome.
        """
        return [
            {
                "entity_id": str(uuid4()),
                "name": fake.company(),
            }
            for _ in range(count)
        ]
