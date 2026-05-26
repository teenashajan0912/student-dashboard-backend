from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps import get_db
from security import require_role
from services.user_service import (get_users_service,update_role_service,delete_user_service)
from utils.logger import logger

router = APIRouter(prefix="/users",tags=["Users"])

@router.get("/")
async def get_users(
    db: Session = Depends(get_db),
    user=Depends(require_role("professor"))
):

    try:
        logger.info("Get users API called")
        result = await get_users_service(db)
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


@router.put("/{user_id}/role")
async def update_role(
    user_id: int,
    new_role: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("professor"))
):

    try:

        logger.info("Update role API called")
        result = await update_role_service(db,user_id,new_role,user)

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


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    try:
        logger.info("Delete user API called")
        result = await delete_user_service(db,user_id)

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