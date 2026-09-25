
from fastapi import APIRouter, Depends, HTTPException

from database import (
    create_user,
    get_profile_statistics,
    get_user_by_username,
    get_user_statistics,
)
from models import UserRegister
from auth import get_current_user, password_hash

router = APIRouter()


@router.post("/admin/users")
def admin_create_user(
    user: UserRegister,
    current_user: dict = Depends(get_current_user),
):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can create users",
        )

    if get_user_by_username(user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    hashed_password = password_hash.hash(user.password)

    try:
        created_user = create_user(
            username=user.username,
            email=user.email,
            password=hashed_password,
            role="user",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    return {
        "message": "User created successfully",
        "user_id": str(created_user["_id"]),
        "username": created_user["username"],
        "role": created_user["role"],
    }


@router.get("/users/{username}")
def get_user_profile(username: str):
    user = get_user_by_username(username)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    stats = get_profile_statistics(str(user["_id"]))

    return {
        "username": user["username"],
        "role": user["role"],
        "notes_count": stats["notes_count"],
        "upvotes_received": stats["upvotes_received"],
    }


@router.get("/stats/me")
def get_my_statistics(
    current_user: dict = Depends(get_current_user),
):
    stats = get_user_statistics(str(current_user["_id"]))

    return {
        "username": current_user["username"],
        **stats,
    }
