from fastapi import HTTPException
from query.user_query import (get_user_by_username,create_user)
from security import (hash_password,verify_password,create_access_token)

def signup_service(payload, db):
    existing_user = get_user_by_username(db,payload.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username exists"
        )

    user_data = {
        "username": payload.username,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "role": payload.role
    }

    create_user(db, user_data)
    return {"message": "User created"}


def login_service(payload, db):
    user = get_user_by_username(db,payload.username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        payload.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }