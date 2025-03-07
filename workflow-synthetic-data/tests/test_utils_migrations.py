import pytest
from pytest_mock import MockerFixture
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from utils.migrations import sync_models_with_db
from utils.db import Base
from sqlalchemy.orm import Session
from sqlalchemy.sql import text


@pytest.fixture
def table_name():
    return "test_table"


@pytest.fixture
def model_columns():
    return lambda: [Column("id", Integer, primary_key=True), Column("name", String)]


def test_sync_models_with_db_error_handling(mocker: MockerFixture, test_engine):
    """
    Testa se erros durante a sincronização dos modelos com o banco de dados são manipulados corretamente.
    """
    error_message = "Erro simulada na criação de tabelas"

    mocker.patch(
        "utils.migrations.Base.metadata.create_all",
        side_effect=Exception(error_message),
    )

    with pytest.raises(Exception, match=error_message):
        sync_models_with_db()


def drop_existing_indexes(engine):
    """
    Remove todos os índices existentes no banco SQLite.
    """
    with Session(engine) as session:
        tables = session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")
        )
        for table in tables:
            indexes = session.execute(
                text(f"PRAGMA index_list('{table[0]}')")
            ).fetchall()
            for index in indexes:
                index_name = index[1]
                session.execute(text(f"DROP INDEX IF EXISTS {index_name}"))
        session.commit()


@pytest.fixture(scope="function")
def test_engine():
    """
    Configura um banco de dados SQLite em memória para cada teste.
    """
    test_engine = create_engine("sqlite:///:memory:")

    with test_engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys = OFF;"))
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)

    yield test_engine

    with test_engine.connect() as conn:
        Base.metadata.drop_all(conn)


@pytest.mark.parametrize(
    "table_name, model_columns, existing_columns, expected_alter_statements",
    [
        (
            "test_table",
            lambda: [Column("id", Integer, primary_key=True), Column("name", String)],
            lambda: [],
            [
                "ALTER TABLE test_table ADD COLUMN id INTEGER PRIMARY KEY",
                "ALTER TABLE test_table ADD COLUMN name VARCHAR",
            ],
        ),
        (
            "test_table",
            lambda: [Column("id", Integer, primary_key=True), Column("name", String)],
            lambda: ["id"],
            ["ALTER TABLE test_table ADD COLUMN name VARCHAR"],
        ),
    ],
)
def test_sync_models_with_db_add_columns(
    mocker: MockerFixture,
    test_engine,
    table_name,
    model_columns,
    existing_columns,
    expected_alter_statements,
):
    """
    Testa se colunas ausentes são adicionadas corretamente ao banco de dados.
    """
    metadata = MetaData()
    model_columns = model_columns()
    existing_columns = existing_columns()

    # sourcery skip: no-conditionals-in-tests
    if not existing_columns:
        db_table = Table(table_name, metadata, *model_columns)
        metadata.create_all(test_engine)

    if existing_columns:
        db_table = Table(
            table_name, metadata, *[Column(col, String) for col in existing_columns]
        )
        metadata.create_all(test_engine)

    mocker.patch("utils.migrations.engine", test_engine)

    table_definition = Table(
        table_name,
        MetaData(),
        *[Column(c.name, c.type, primary_key=c.primary_key) for c in model_columns],
    )
    mocker.patch(
        "utils.migrations.Base.metadata.tables", {table_name: table_definition}
    )

    with test_engine.connect() as conn:
        sync_models_with_db()

    with test_engine.connect() as conn:
        result = conn.execute(text(f"PRAGMA table_info('{table_name}')"))
        existing_columns = {row[1] for row in result.fetchall()}

        # sourcery skip: no-loop-in-tests
        for stmt in expected_alter_statements:
            column_name = stmt.split(" ADD COLUMN ")[1].split(" ")[0]
            assert column_name in existing_columns


@pytest.mark.parametrize(
    "table_name",
    [
        ("test_table"),
        ("another_table"),
    ],
    ids=["existing_table", "non_existing_table"],
)
def test_sync_models_with_db_no_missing_columns(
    mocker: MockerFixture, test_engine, table_name
):
    """
    Testa se nenhuma alteração ocorre quando todas as colunas já existem.
    """
    metadata = MetaData()
    model_columns = [Column("id", Integer, primary_key=True), Column("name", String)]

    db_table = Table(
        table_name, metadata, *[Column(col.name, col.type) for col in model_columns]
    )
    metadata.create_all(test_engine)

    mocker.patch("utils.migrations.engine", test_engine)

    table_definition = Table(table_name, MetaData(), *model_columns)
    mocker.patch(
        "utils.migrations.Base.metadata.tables", {table_name: table_definition}
    )

    with test_engine.connect() as conn:
        sync_models_with_db()

    with test_engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"
            ),
            {"table_name": table_name},
        )
        assert result.fetchone() is not None
