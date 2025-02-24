import pytest
from unittest.mock import patch, Mock
from src.services.account import AccountService
from src.commons.accounts import AccountEvents
from src.models.account import Account, Subaccount, User
from src.utils.db import SessionLocal, Base, engine


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    yield db
    db.rollback()
    Base.metadata.drop_all(engine)
    db.close()


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
    inserted_users = AccountService.insert_users(count)

    assert len(inserted_users) == count
    # sourcery skip: no-loop-in-tests
    for user in inserted_users:
        assert isinstance(user, User)


def test_insert_users_rollback(test_db, mocker):
    mock_db = mocker.patch(
        "src.services.account.SessionLocal", autospec=True
    ).return_value
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
    AccountService.insert_users(5)

    inserted_accounts = AccountService.insert_accounts(count)

    assert len(inserted_accounts) == count
    # sourcery skip: no-loop-in-tests
    for account in inserted_accounts:
        assert isinstance(account, Account)


def test_insert_accounts_rollback(test_db, mocker):
    mock_db = mocker.patch(
        "src.services.account.SessionLocal", autospec=True
    ).return_value
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
    AccountService.insert_users(5)
    AccountService.insert_accounts(5)

    inserted_subaccounts = AccountService.insert_subaccounts(count)

    assert len(inserted_subaccounts) == count
    # sourcery skip: no-loop-in-tests
    for subaccount in inserted_subaccounts:
        assert isinstance(subaccount, Subaccount)


def test_insert_subaccounts_rollback(test_db, mocker):
    mock_db = mocker.patch(
        "src.services.account.SessionLocal", autospec=True
    ).return_value
    mock_db.commit.side_effect = Exception("Mock DB error")
    AccountService.insert_users(5)
    AccountService.insert_accounts(5)

    inserted_subaccounts = AccountService.insert_subaccounts(5)

    assert inserted_subaccounts == []
