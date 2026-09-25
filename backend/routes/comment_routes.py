
from fastapi import APIRouter, Depends, HTTPException

from database import (
    create_comment as db_create_comment,
    delete_comment as db_delete_comment,
    get_comment as db_get_comment,
    get_comments as db_get_comments,
    get_user_by_id,
    update_comment as db_update_comment,
)
from models import Comment
from auth import get_current_user
from notification_client import notify_comment_added

router = APIRouter()


@router.get("/notes/{note_id}/comments")
def get_comments(note_id: str):
    try:
        comments = db_get_comments(note_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID",
        )

    if comments is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return comments


@router.post("/notes/{note_id}/comments")
def create_comment(
    note_id: str,
    comment: Comment,
    current_user: dict = Depends(get_current_user),
):
    try:
        result = db_create_comment(
            note_id=note_id,
            user_id=str(current_user["_id"]),
            content=comment.content,
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID or user ID",
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    note = result["note"]
    note_owner_id = note.get("user_id")

    if note_owner_id:
        try:
            note_owner = get_user_by_id(str(note_owner_id))

            if note_owner:
                owner_email = note_owner.get("email")

                if owner_email:
                    notify_comment_added(
                        recipient=owner_email,
                        commenter_username=current_user["username"],
                        note_title=note["title"],
                    )
        except Exception as error:
            print(f"Comment notification error: {error}")

    return {
        "message": "Comment added successfully",
        "comment_id": result["id"],
    }


@router.put("/comments/{comment_id}")
def update_comment(
    comment_id: str,
    comment: Comment,
    current_user: dict = Depends(get_current_user),
):
    try:
        existing_comment = db_get_comment(comment_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid comment ID",
        )

    if existing_comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    if (
        current_user["role"] != "admin"
        and existing_comment["user_id"] != str(current_user["_id"])
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own comments",
        )

    db_update_comment(
        comment_id=comment_id,
        content=comment.content,
    )

    return {
        "message": "Comment updated successfully"
    }


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        existing_comment = db_get_comment(comment_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid comment ID",
        )

    if existing_comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    if (
        current_user["role"] != "admin"
        and existing_comment["user_id"] != str(current_user["_id"])
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own comments",
        )

    db_delete_comment(comment_id)

    return {
        "message": "Comment deleted successfully"
    }
