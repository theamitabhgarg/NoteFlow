from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from bson import ObjectId

from database import (
    comments_collection,
    notes_collection,
    users_collection
)

from models import Comment

from auth import get_current_user

from notification_client import notify_comment_added


router = APIRouter()


@router.get("/notes/{note_id}/comments")
def get_comments(note_id: str):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID"
        )

    note = notes_collection.find_one({
        "_id": ObjectId(note_id)
    })

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    comments = list(
        comments_collection.find({
            "note_id": note_id
        }).sort(
            "created_at",
            1
        )
    )

    result = []

    for comment in comments:

        username = None

        if comment.get("user_id"):

            user = users_collection.find_one({
                "_id": ObjectId(comment["user_id"])
            })

            if user:
                username = user["username"]

        result.append({
            "id": str(comment["_id"]),
            "note_id": comment["note_id"],
            "user_id": comment["user_id"],
            "username": username,
            "content": comment["content"],
            "created_at": comment.get("created_at"),
            "updated_at": comment.get("updated_at")
        })

    return result


@router.post("/notes/{note_id}/comments")
def create_comment(
    note_id: str,
    comment: Comment,
    current_user: dict = Depends(get_current_user)
):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID"
        )

    note = notes_collection.find_one({
        "_id": ObjectId(note_id)
    })

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    now = datetime.now(timezone.utc)

    new_comment = {
        "note_id": note_id,
        "user_id": str(current_user["_id"]),
        "content": comment.content,
        "created_at": now,
        "updated_at": now
    }

    result = comments_collection.insert_one(
        new_comment
    )

    notes_collection.update_one(
        {
            "_id": ObjectId(note_id)
        },
        {
            "$inc": {
                "comment_count": 1
            }
        }
    )

    # --------------------------------------------------
    # NOTIFICATION
    #
    # Notify the owner of the note.
    # --------------------------------------------------

    note_owner_id = note.get("user_id")

    if note_owner_id:

        try:
            note_owner = users_collection.find_one({
                "_id": ObjectId(note_owner_id)
            })

            if note_owner:

                owner_email = note_owner.get("email")

                if owner_email:

                    notify_comment_added(
                        recipient=owner_email,
                        commenter_username=current_user["username"],
                        note_title=note["title"]
                    )

        except Exception as error:

            print(
                f"Comment notification error: {error}"
            )

    return {
        "message": "Comment added successfully",
        "comment_id": str(result.inserted_id)
    }


@router.put("/comments/{comment_id}")
def update_comment(
    comment_id: str,
    comment: Comment,
    current_user: dict = Depends(get_current_user)
):

    if not ObjectId.is_valid(comment_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid comment ID"
        )

    existing_comment = comments_collection.find_one({
        "_id": ObjectId(comment_id)
    })

    if existing_comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    if (
        current_user["role"] != "admin"
        and existing_comment["user_id"]
        != str(current_user["_id"])
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own comments"
        )

    comments_collection.update_one(
        {
            "_id": ObjectId(comment_id)
        },
        {
            "$set": {
                "content": comment.content,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return {
        "message": "Comment updated successfully"
    }


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: str,
    current_user: dict = Depends(get_current_user)
):

    if not ObjectId.is_valid(comment_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid comment ID"
        )

    existing_comment = comments_collection.find_one({
        "_id": ObjectId(comment_id)
    })

    if existing_comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    if (
        current_user["role"] != "admin"
        and existing_comment["user_id"]
        != str(current_user["_id"])
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own comments"
        )

    comments_collection.delete_one({
        "_id": ObjectId(comment_id)
    })

    notes_collection.update_one(
        {
            "_id": ObjectId(existing_comment["note_id"])
        },
        {
            "$inc": {
                "comment_count": -1
            }
        }
    )

    return {
        "message": "Comment deleted successfully"
    }