from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import router as auth_router
from routers.students import router as students_router
from routers.dashboard import router as dashboard_router
from routers.users import router as users_router
from database import Base, engine, SessionLocal
from models import User, Student
from sqlalchemy.orm import Session
from security import hash_password
import pandas as pd
from models import Student

Base.metadata.create_all(bind=engine)

def create_default_user():
    db: Session = SessionLocal()

    existing = db.query(User).filter(User.username == "admin").first()

    if not existing:
        user = User(
            username="admin",
            email="admin@test.com",
            hashed_password=hash_password("password123"),
            role="admin",
            is_system=True
        )

        db.add(user)
        db.commit()
        print("✅ Default admin created with role:", user.role)
    else:
        print("⚠️ Admin already exists with role:", existing.role)

    db.close()

create_default_user()

def load_csv_data():
    db = SessionLocal()

    if db.query(Student).count() > 0:
        print("Data already exists")
        db.close()
        return

    try:
        df = pd.read_csv("StudentPerformanceFactors.csv")

        for _, row in df.iterrows():
            student = Student(
                Gender=row["Gender"],
                Exam_Score=row["Exam_Score"],
                Attendance=row["Attendance"],
                Hours_Studied=row["Hours_Studied"],
                Physical_Activity=row["Physical_Activity"] 
)
            db.add(student)

        db.commit()
        print("CSV data loaded successfully")

    except Exception as e:
        print("Error loading CSV:", e)

    db.close()

load_csv_data()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(students_router)
app.include_router(dashboard_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "API Running.. "}