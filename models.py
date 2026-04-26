from sqlalchemy import Column, Integer, String, Float,Boolean
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    Gender = Column(String)
    Exam_Score = Column(Integer)
    Attendance = Column(Float)
    Hours_Studied = Column(Float)
    Physical_Activity = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String, default="student") 
    is_system = Column(Boolean, default=False)