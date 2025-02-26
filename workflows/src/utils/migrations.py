from models.account import Base
from models.audit import Base
from models.compliance import Base
from models.credit import Base
from models.entities import Base
from models.insurance import Base
from models.investments import Base
from models.lending import Base
from models.payment import Base
from utils.db import engine, Base
from sqlalchemy import MetaData, text
from sqlalchemy.exc import SQLAlchemyError


SQLALCHEMY_TO_POSTGRESQL = {
    "INTEGER": "INTEGER",
    "BIGINT": "BIGINT",
    "VARCHAR": "VARCHAR",
    "TEXT": "TEXT",
    "BOOLEAN": "BOOLEAN",
    "DECIMAL": "DECIMAL",
    "FLOAT": "DOUBLE PRECISION",
    "NUMERIC": "NUMERIC",
    "DATETIME": "TIMESTAMP",
    "DATE": "DATE",
    "TIME": "TIME",
}


def sync_models_with_db():
    """
    Sincroniza os modelos SQLAlchemy com o banco de dados, adicionando colunas ausentes quando necessário.
    """
    Base.metadata.create_all(engine)
    metadata = MetaData()

    try:
        metadata.reflect(bind=engine)

        with engine.connect() as conn:
            with conn.begin():
                for table_name, model_table in Base.metadata.tables.items():
                    if table_name in metadata.tables:
                        db_table = metadata.tables[table_name]

                        for column in model_table.columns:
                            column_name = column.name

                            if column_name not in db_table.c:
                                column_type = str(column.type).upper()
                                column_type_pg = SQLALCHEMY_TO_POSTGRESQL.get(
                                    column_type, column_type
                                )

                                alter_stmt = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_pg}"
                                if column_type_pg == "TIMESTAMP":
                                    alter_stmt += " DEFAULT NOW()"

                                try:
                                    conn.execute(text(alter_stmt))
                                    print(
                                        f"✅ Coluna '{column_name}' adicionada na tabela '{table_name}' como '{column_type_pg}'."
                                    )
                                except SQLAlchemyError as e:
                                    print(
                                        f"❌ Erro ao adicionar a coluna '{column_name}' na tabela '{table_name}': {e}"
                                    )
                print(
                    f"⚠️ Tabela '{table_name}' não existe no banco. Criando com SQLAlchemy..."
                )

    except SQLAlchemyError as e:
        print(f"❌ Erro ao sincronizar modelos com o banco: {e}")


if __name__ == "__main__":
    print("🔄 Criando tabelas no banco de dados...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")

        print("\n🔄 Sincronizando colunas do modelo com o banco de dados...")
        sync_models_with_db()

        print("✅ Atualização das tabelas concluída!")
    except SQLAlchemyError as e:
        print(f"❌ Erro ao criar tabelas: {e}")
