from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps import get_db
from security import get_current_user
from services.student_service import (get_students_service)
from utils.logger import logger

router = APIRouter()

@router.get("/students")
async def get_students(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    try:
        logger.info("Students API called")
        result = await get_students_service(db)
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