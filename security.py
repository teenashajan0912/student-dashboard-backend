from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "secret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

ROLE_LEVEL = {
    "student": 1,
    "professor": 2,
    "admin": 3
}

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()

    to_encode.update({
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
        
def require_role(min_role: str):
    def wrapper(user=Depends(get_current_user)):
        if user.get("role") is None:
            raise HTTPException(status_code=403, detail="No role in token")

        if ROLE_LEVEL[user["role"]] < ROLE_LEVEL[min_role]:
            raise HTTPException(status_code=403, detail="Forbidden")

        return user
    return wrapper

