from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import SignupRequest,LoginRequest,TokenResponse
from deps import get_db
from services.auth_service import (signup_service,login_service)
from utils.logger import logger

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/signup")
async def signup(
    payload: SignupRequest,
    db: Session = Depends(get_db)
):

    try:
        logger.info("Signup API called")
        result = await signup_service(payload, db)
        return {
            "status": 200,
            "data": result
        }

    except HTTPException as e:

        logger.error(e.detail)
        raise e

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):

    try:
        logger.info("Login API called")
        result = await login_service(payload, db)
        return result

    except HTTPException as e:
        logger.error(e.detail)
        raise e

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )