from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Student
from deps import get_db
from schemas import StudentResponse
from typing import List
from security import get_current_user

router = APIRouter()

@router.get("/students", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db),user=Depends(get_current_user)):
    students = db.query(Student).all()
    return students