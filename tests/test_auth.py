import pytest
from services.auth_service import signup_service, login_service


class Payload:
    username = "testuser"
    email = "test@test.com"
    password = "password123"
    role = "student"


@pytest.mark.asyncio
async def test_signup_success(mocker):

    mocker.patch(
        "services.auth_service.get_user_by_username",
        return_value=None
    )

    mocker.patch(
        "services.auth_service.create_user"
    )

    result = await signup_service(
        Payload(),
        None
    )

    assert result["message"] == "User created"


@pytest.mark.asyncio
async def test_login_success(mocker):

    user = mocker.Mock()
    user.username = "testuser"
    user.role = "student"
    user.hashed_password = "hashed"

    mocker.patch(
        "services.auth_service.get_user_by_username",
        return_value=user
    )

    mocker.patch(
        "services.auth_service.verify_password",
        return_value=True
    )

    mocker.patch(
        "services.auth_service.create_access_token",
        return_value="token123"
    )

    result = await login_service(
        Payload(),
        None
    )

    assert result["access_token"] == "token123"