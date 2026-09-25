
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Form, HTTPException

from database import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from models import UserRegister
from auth import password_hash, SECRET_KEY, ALGORITHM

router = APIRouter()


@router.post("/register")
def register(user: UserRegister):
    if get_user_by_username(user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    if get_user_by_email(user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    hashed_password = password_hash.hash(user.password)

    try:
        create_user(
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
        "message": "User registered successfully"
    }


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
):
    user = get_user_by_username(username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    if not password_hash.verify(password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    payload = {
        "user_id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
