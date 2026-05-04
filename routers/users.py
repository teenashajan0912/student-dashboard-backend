from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from deps import get_db
from security import require_role, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


# ADMIN + PROFESSOR VIEW USERS  
@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    user=Depends(require_role("professor"))
):
    return db.query(User).all()


# UPDATE ROLE (PROFESSOR + ADMIN)
@router.put("/{user_id}/role")
def update_role(
    user_id: int,
    new_role: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("professor"))
):

    target = db.query(User).filter(User.id == user_id).first()

    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    # SYSTEM ADMIN PROTECTION
    if target.is_system:
        raise HTTPException(
            status_code=403,
            detail="System admin cannot be modified"
        )

    # VALID ROLE CHECK
    if new_role not in ["student", "professor", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    # PROFESSOR CANNOT CREATE ADMIN
    if user["role"] == "professor" and new_role == "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    target.role = new_role
    db.commit()

    return {"message": "Role updated successfully"}


# DELETE USER (ADMIN ONLY)
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    target = db.query(User).filter(User.id == user_id).first()

    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    # SYSTEM ADMIN PROTECTION
    if target.is_system:
        raise HTTPException(
            status_code=403,
            detail="System admin cannot be deleted"
        )

    db.delete(target)
    db.commit()

    return {"message": "User deleted"}