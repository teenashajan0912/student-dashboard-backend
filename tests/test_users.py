import pytest
from fastapi import HTTPException
from services.user_service import (
    update_role_service,
    delete_user_service
)


class User:
    id = 1
    role = "student"
    is_system = False


@pytest.mark.asyncio
async def test_update_role(mocker):

    mocker.patch(
        "services.user_service.get_user_by_id",
        return_value=User()
    )

    db = mocker.Mock()

    result = await update_role_service(
        db,
        1,
        "professor",
        {"role": "admin"}
    )

    assert result["message"] == "Role updated successfully"


@pytest.mark.asyncio
async def test_update_role_user_not_found(mocker):

    mocker.patch(
        "services.user_service.get_user_by_id",
        return_value=None
    )

    db = mocker.Mock()

    with pytest.raises(HTTPException):
        await update_role_service(
            db,
            999,
            "student",
            {"role": "admin"}
        )


@pytest.mark.asyncio
async def test_update_role_invalid_role(mocker):

    mocker.patch(
        "services.user_service.get_user_by_id",
        return_value=User()
    )

    db = mocker.Mock()

    with pytest.raises(HTTPException):
        await update_role_service(
            db,
            1,
            "manager",
            {"role": "admin"}
        )


@pytest.mark.asyncio
async def test_update_role_professor_cannot_make_admin(mocker):

    mocker.patch(
        "services.user_service.get_user_by_id",
        return_value=User()
    )

    db = mocker.Mock()

    with pytest.raises(HTTPException):
        await update_role_service(
            db,
            1,
            "admin",
            {"role": "professor"}
        )


@pytest.mark.asyncio
async def test_update_role_system_admin(mocker):

    class SystemUser:
        id = 1
        role = "admin"
        is_system = True

    mocker.patch(
        "services.user_service.get_user_by_id",
        return_value=SystemUser()
    )

    db = mocker.Mock()

    with pytest.raises(HTTPException):
        await update_role_service(
            db,
            1,
            "student",
            {"role": "admin"}
        )


@pytest.mark.asyncio
async def test_delete_user_not_found(mocker):

    mocker.patch(
        "services.user_service.get_user_by_id",
        return_value=None
    )

    db = mocker.Mock()

    with pytest.raises(HTTPException):
        await delete_user_service(
            db,
            1
        )


@pytest.mark.asyncio
async def test_delete_system_user(mocker):

    class SystemUser:
        id = 1
        role = "admin"
        is_system = True

    mocker.patch(
        "services.user_service.get_user_by_id",
        return_value=SystemUser()
    )

    db = mocker.Mock()

    with pytest.raises(HTTPException):
        await delete_user_service(
            db,
            1
        )


@pytest.mark.asyncio
async def test_delete_user_success(mocker):

    mocker.patch(
        "services.user_service.get_user_by_id",
        return_value=User()
    )

    mock_delete = mocker.patch(
        "services.user_service.delete_user_db"
    )

    db = mocker.Mock()

    result = await delete_user_service(
        db,
        1
    )

    assert result["message"] == "User deleted"

    mock_delete.assert_called_once()