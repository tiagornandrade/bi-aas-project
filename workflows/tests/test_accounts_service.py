import pytest
from unittest.mock import patch, Mock
from services.account import AccountService
from commons.accounts import AccountEvents
from models.account import Account, Subaccount, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.db import SessionLocal, Base, engine

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


@pytest.fixture(scope="function")
def test_db():
    """Garante que os testes rodem no SQLite e não no PostgreSQL."""

    test_engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )

    Base.metadata.create_all(test_engine)
    db = TestingSessionLocal()

    global SessionLocal
    original_session = SessionLocal
    SessionLocal = TestingSessionLocal

    yield db

    db.rollback()
    Base.metadata.drop_all(test_engine)
    db.close()

    SessionLocal = original_session


@pytest.mark.parametrize(
    "count",
    [
        (0),
        (1),
        (5),
    ],
    ids=["zero_users", "one_user", "multiple_users"],
)
def test_insert_users_happy_path(test_db, count):
    inserted_users = AccountService.insert_users(count, db=test_db)
    assert len(inserted_users) == count
    # sourcery skip: no-loop-in-tests
    for user in inserted_users:
        assert isinstance(user, User)


def test_insert_users_rollback(test_db, mocker):
    mock_db = mocker.patch("services.account.SessionLocal", autospec=True).return_value
    mock_db.commit.side_effect = Exception("Mock DB error")

    inserted_users = AccountService.insert_users(5)

    assert inserted_users == []


@pytest.mark.parametrize(
    "count",
    [
        (0),
        (1),
        (5),
    ],
    ids=["zero_accounts", "one_account", "multiple_accounts"],
)
def test_insert_accounts_happy_path(test_db, count):
    inserted_accounts = AccountService.insert_accounts(count, db=test_db)
    assert len(inserted_accounts) == count
    # sourcery skip: no-loop-in-tests
    for account in inserted_accounts:
        assert isinstance(account, Account)


def test_insert_accounts_rollback(test_db, mocker):
    mock_db = mocker.patch("services.account.SessionLocal", autospec=True).return_value
    mock_db.commit.side_effect = Exception("Mock DB error")
    AccountService.insert_users(5)

    inserted_accounts = AccountService.insert_accounts(5)

    assert inserted_accounts == []


@pytest.mark.parametrize(
    "count",
    [
        (0),
        (1),
        (5),
    ],
    ids=["zero_subaccounts", "one_subaccount", "multiple_subaccounts"],
)
def test_insert_subaccounts_happy_path(test_db, count):
    inserted_subaccounts = AccountService.insert_subaccounts(count, db=test_db)
    assert len(inserted_subaccounts) == count
    # sourcery skip: no-loop-in-tests
    for subaccount in inserted_subaccounts:
        assert isinstance(subaccount, Subaccount)


def test_insert_subaccounts_rollback(test_db, mocker):
    mock_db = mocker.patch("services.account.SessionLocal", autospec=True).return_value
    mock_db.commit.side_effect = Exception("Mock DB error")
    AccountService.insert_users(5)
    AccountService.insert_accounts(5)

    inserted_subaccounts = AccountService.insert_subaccounts(5)

    assert inserted_subaccounts == []
