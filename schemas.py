from pydantic import BaseModel

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str = "student" 


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class StudentResponse(BaseModel):
    id: int
    Hours_Studied: int
    Attendance: int
    Gender: str
    Exam_Score: int
    Physical_Activity: int

    class Config:
        orm_mode = True