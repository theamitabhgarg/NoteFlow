from fastapi import APIRouter, Depends, HTTPException

from bson import ObjectId

from pymongo.errors import DuplicateKeyError

from database import (
    votes_collection,
    notes_collection,
    users_collection
)

from auth import get_current_user

from notification_client import notify_upvote_added


router = APIRouter()


@router.post("/notes/{note_id}/upvote")
def upvote_note(
    note_id: str,
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

    user_id = str(current_user["_id"])

    new_vote = {
        "note_id": note_id,
        "user_id": user_id,
        "vote": 1
    }

    try:

        votes_collection.insert_one(
            new_vote
        )

    except DuplicateKeyError:

        raise HTTPException(
            status_code=400,
            detail="You have already upvoted this note"
        )

    notes_collection.update_one(
        {
            "_id": ObjectId(note_id)
        },
        {
            "$inc": {
                "upvote_count": 1
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

                    notify_upvote_added(
                        recipient=owner_email,
                        voter_username=current_user["username"],
                        note_title=note["title"]
                    )

        except Exception as error:

            print(
                f"Upvote notification error: {error}"
            )

    return {
        "message": "Note upvoted successfully"
    }


@router.delete("/notes/{note_id}/upvote")
def remove_upvote(
    note_id: str,
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

    user_id = str(current_user["_id"])

    existing_vote = votes_collection.find_one({
        "note_id": note_id,
        "user_id": user_id
    })

    if existing_vote is None:
        raise HTTPException(
            status_code=400,
            detail="You have not upvoted this note"
        )

    votes_collection.delete_one({
        "_id": existing_vote["_id"]
    })

    notes_collection.update_one(
        {
            "_id": ObjectId(note_id)
        },
        {
            "$inc": {
                "upvote_count": -1
            }
        }
    )

    return {
        "message": "Upvote removed successfully"
    }