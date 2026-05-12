from models import Student
def fetch_students(db):
    return db.query(Student).all()