
from fastapi import APIRouter, Depends, HTTPException

from database import (
    add_vote,
    get_user_by_id,
    remove_vote,
)
from auth import get_current_user
from notification_client import notify_upvote_added

router = APIRouter()


@router.post("/notes/{note_id}/upvote")
def upvote_note(
    note_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        note = add_vote(
            note_id=note_id,
            user_id=str(current_user["_id"]),
        )
    except ValueError as error:
        message = str(error)

        if message == "You have already upvoted this note":
            raise HTTPException(
                status_code=400,
                detail=message,
            )

        raise HTTPException(
            status_code=400,
            detail="Invalid note ID or user ID",
        )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    note_owner_id = note.get("user_id")

    if note_owner_id:
        try:
            note_owner = get_user_by_id(str(note_owner_id))

            if note_owner:
                owner_email = note_owner.get("email")

                if owner_email:
                    notify_upvote_added(
                        recipient=owner_email,
                        voter_username=current_user["username"],
                        note_title=note["title"],
                    )
        except Exception as error:
            print(f"Upvote notification error: {error}")

    return {
        "message": "Note upvoted successfully"
    }


@router.delete("/notes/{note_id}/upvote")
def remove_upvote(
    note_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        note = remove_vote(
            note_id=note_id,
            user_id=str(current_user["_id"]),
        )
    except ValueError as error:
        message = str(error)

        if message == "You have not upvoted this note":
            raise HTTPException(
                status_code=400,
                detail=message,
            )

        raise HTTPException(
            status_code=400,
            detail="Invalid note ID or user ID",
        )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return {
        "message": "Upvote removed successfully"
    }
