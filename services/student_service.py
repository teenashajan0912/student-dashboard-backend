from query.student_query import (fetch_students)

async def get_students_service(db):
    students = fetch_students(db)
    return students