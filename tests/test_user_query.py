import pytest
from query.user_query import (
    get_user_by_username,
    get_all_users,
    get_user_by_id,
    create_user,
    delete_user_db
)


def test_get_user_by_username(mocker):
    db = mocker.Mock()

    query_mock = db.query.return_value
    filter_mock = query_mock.filter.return_value

    filter_mock.first.return_value = "user"

    result = get_user_by_username(
        db,
        "john"
    )

    assert result == "user"


def test_get_all_users(mocker):
    db = mocker.Mock()

    db.query.return_value.all.return_value = [
        {"id": 1}
    ]

    result = get_all_users(db)

    assert len(result) == 1


def test_get_user_by_id(mocker):
    db = mocker.Mock()

    query_mock = db.query.return_value
    filter_mock = query_mock.filter.return_value

    filter_mock.first.return_value = {
        "id": 1
    }

    result = get_user_by_id(
        db,
        1
    )

    assert result["id"] == 1


def test_create_user(mocker):
    db = mocker.Mock()

    user_data = {
        "username": "john",
        "email": "john@test.com",
        "hashed_password": "abc123",
        "role": "student"
    }

    result = create_user(
        db,
        user_data
    )

    db.add.assert_called_once()
    db.commit.assert_called_once()

    assert result.username == "john"


def test_delete_user_db(mocker):
    db = mocker.Mock()

    user = mocker.Mock()

    delete_user_db(
        db,
        user
    )

    db.delete.assert_called_once_with(user)
    db.commit.assert_called_once()