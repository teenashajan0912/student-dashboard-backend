from fastapi import HTTPException
from query.user_query import (get_all_users,get_user_by_id,delete_user_db)

def get_users_service(db):
    return get_all_users(db)


def update_role_service(db,user_id,new_role,current_user):

    target = get_user_by_id(db,user_id)

    if not target:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if target.is_system:
        raise HTTPException(
            status_code=403,
            detail="System admin cannot be modified"
        )

    if new_role not in [
        "student",
        "professor",
        "admin"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    if (
        current_user["role"] == "professor"
        and new_role == "admin"
    ):

        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    target.role = new_role

    db.commit()

    return {
        "message": "Role updated successfully"
    }


def delete_user_service(
    db,
    user_id
):

    target = get_user_by_id(
        db,
        user_id
    )

    if not target:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if target.is_system:

        raise HTTPException(
            status_code=403,
            detail="System admin cannot be deleted"
        )

    delete_user_db(
        db,
        target
    )

    return {
        "message": "User deleted"
    }