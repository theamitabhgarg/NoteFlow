from datetime import datetime, timedelta, timezone

import jwt

from fastapi import APIRouter, Form, HTTPException

from database import users_collection

from models import UserRegister

from auth import password_hash, SECRET_KEY, ALGORITHM


router = APIRouter()


@router.post("/register")
def register(user: UserRegister):

    existing_user = users_collection.find_one({
        "username": user.username
    })

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = password_hash.hash(user.password)

    users_collection.insert_one({
        "username": user.username,
        "password": hashed_password,
        "role": "user"
    })

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):

    user = users_collection.find_one({
        "username": username
    })

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not password_hash.verify(password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    payload = {
        "user_id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
