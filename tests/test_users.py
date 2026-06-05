import pytest
from services.user_service import update_role_service

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