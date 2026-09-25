
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from database import get_user_by_id

load_dotenv()

password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "my-super-secret-key-change-this-later",
)
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

        try:
            user = get_user_by_id(str(user_id))
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Invalid user ID",
            )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        return user

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )
