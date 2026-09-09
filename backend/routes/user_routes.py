from fastapi import APIRouter, Depends, HTTPException

from bson import ObjectId

from database import users_collection, notes_collection, votes_collection, comments_collection

from models import UserRegister

from auth import get_current_user, password_hash


router = APIRouter()


@router.post("/admin/users")
def admin_create_user(
    user: UserRegister,
    current_user: dict = Depends(get_current_user)
):
    # Only administrators can create users from the admin settings.
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can create users"
        )

    existing_user = users_collection.find_one({
        "username": user.username
    })

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = password_hash.hash(user.password)

    result = users_collection.insert_one({
        "username": user.username,
        "password": hashed_password,
        "role": "user"
    })

    return {
        "message": "User created successfully",
        "user_id": str(result.inserted_id),
        "username": user.username,
        "role": "user"
    }


@router.get("/users/{username}")
def get_user_profile(username: str):

    user = users_collection.find_one({
        "username": username
    })

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user_id = str(user["_id"])

    # Count notes created by this user
    notes_count = notes_collection.count_documents({
        "user_id": user_id
    })

    # Find all notes created by this user
    user_notes = notes_collection.find({
        "user_id": user_id
    })

    # Calculate total upvotes received
    upvotes_received = 0

    for note in user_notes:
        upvotes_received += note.get("upvote_count", 0)

    return {
        "username": user["username"],
        "role": user["role"],
        "notes_count": notes_count,
        "upvotes_received": upvotes_received
    }


@router.get("/stats/me")
def get_my_statistics(
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])

    # Notes created by the logged-in user
    user_notes = list(
        notes_collection.find({
            "user_id": user_id
        })
    )

    notes_count = len(user_notes)

    # Count unique tags and how many of the user's notes use each tag
    tag_counts = {}

    for note in user_notes:
        for tag in note.get("tags", []):
            if tag:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

    # Upvotes given by the logged-in user
    upvotes_given = votes_collection.count_documents({
        "user_id": user_id
    })

    # Comments written by the logged-in user
    comments_written = comments_collection.count_documents({
        "user_id": user_id
    })

    return {
        "username": current_user["username"],
        "notes_count": notes_count,
        "unique_tags": len(tag_counts),
        "upvotes_given": upvotes_given,
        "comments_written": comments_written,
        "tag_counts": dict(sorted(tag_counts.items()))
    }
