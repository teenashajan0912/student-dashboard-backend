import pytest
from services.student_service import get_students_service


@pytest.mark.asyncio
async def test_get_students(mocker):

    students = [
        {"id": 1},
        {"id": 2}
    ]

    mocker.patch(
        "services.student_service.fetch_students",
        return_value=students
    )

    result = await get_students_service(None)

    assert len(result) == 2