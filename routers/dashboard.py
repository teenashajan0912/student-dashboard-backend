from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps import get_db
from services.dashboard_service import (get_dashboard_service,physical_activity_service)
from utils.logger import logger

router = APIRouter()
@router.get("/dashboard")
async def dashboard(
    db: Session = Depends(get_db)
):

    try:
        logger.info("Dashboard API called")
        result = await get_dashboard_service(db)
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


@router.get("/physical-activity")
async def physical_activity(
    db: Session = Depends(get_db)
):
    try:
        logger.info("Physical activity API called")
        result = await physical_activity_service(db)
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