from query.student_query import (fetch_students)

def get_students_service(db):
    students = fetch_students(db)
    return students