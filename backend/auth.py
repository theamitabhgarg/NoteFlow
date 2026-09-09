from datetime import datetime, timezone

import jwt
from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from database import users_collection


password_hash = PasswordHash.recommended()

SECRET_KEY = "my-super-secret-key-change-this-later"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=401,
                detail="Invalid user ID"
            )

        user = users_collection.find_one({
            "_id": ObjectId(user_id)
        })

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
