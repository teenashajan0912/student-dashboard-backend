import pytest
from services.dashboard_service import get_dashboard_service

class Student:

    def __init__(self,score,gender,attendance,hours):
        self.Exam_Score = score
        self.Gender = gender
        self.Attendance = attendance
        self.Hours_Studied = hours


@pytest.mark.asyncio
async def test_dashboard_summary(mocker):

    students = [
        Student(40, "Male", 80, 5),
        Student(90, "Female", 95, 8)
    ]

    mocker.patch(
        "services.dashboard_service.fetch_students",
        return_value=students
    )

    result = await get_dashboard_service(None)

    assert len(result) == 3