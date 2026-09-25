
from fastapi import APIRouter, Depends, HTTPException

from database import (
    create_note as db_create_note,
    delete_note as db_delete_note,
    get_all_users_except,
    get_note as db_get_note,
    get_notes as db_get_notes,
    get_tags,
    update_note as db_update_note,
)
from models import Note
from auth import get_current_user
from notification_client import notify_note_created

router = APIRouter()


def validate_pagination(page: int, limit: int):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be 1 or greater",
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100",
        )


def validate_sort(sort: str):
    if sort not in {"popular", "newest", "oldest"}:
        raise HTTPException(
            status_code=400,
            detail="Sort must be popular, newest, or oldest",
        )


@router.get("/notes")
def get_notes_endpoint(
    search: str | None = None,
    tag: str | None = None,
    sort: str = "newest",
    page: int = 1,
    limit: int = 10,
):
    validate_pagination(page, limit)
    validate_sort(sort)

    try:
        notes, total_notes = db_get_notes(
            search=search,
            tag=tag,
            sort=sort,
            page=page,
            limit=limit,
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid database ID",
        )

    total_pages = (total_notes + limit - 1) // limit

    return {
        "notes": notes,
        "page": page,
        "limit": limit,
        "total_notes": total_notes,
        "total_pages": total_pages,
    }


@router.get("/notes/mine")
def get_my_notes(
    search: str | None = None,
    tag: str | None = None,
    sort: str = "newest",
    page: int = 1,
    limit: int = 8,
    current_user: dict = Depends(get_current_user),
):
    validate_pagination(page, limit)
    validate_sort(sort)

    user_id = str(current_user["_id"])

    try:
        notes, total_notes = db_get_notes(
            search=search,
            tag=tag,
            sort=sort,
            page=page,
            limit=limit,
            user_id=user_id,
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID",
        )

    # Preserve the original NoteFlow behavior.
    for note in notes:
        note["username"] = current_user["username"]

    total_pages = (total_notes + limit - 1) // limit

    return {
        "notes": notes,
        "page": page,
        "limit": limit,
        "total_notes": total_notes,
        "total_pages": total_pages,
    }


@router.get("/tags")
def get_tags_endpoint():
    return {
        "tags": get_tags()
    }


@router.get("/notes/{note_id}")
def get_note(note_id: str):
    try:
        note = db_get_note(note_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID",
        )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return note


@router.post("/notes")
def create_note(
    note: Note,
    current_user: dict = Depends(get_current_user),
):
    note_id = db_create_note(
        title=note.title,
        content=note.content,
        tags=note.tags,
        user_id=str(current_user["_id"]),
    )

    # Notify every registered user except the creator.
    for user in get_all_users_except(str(current_user["_id"])):
        email = user.get("email")

        if not email:
            continue

        notify_note_created(
            recipient=email,
            creator_username=current_user["username"],
            note_title=note.title,
        )

    return {
        "message": "Note created successfully",
        "note_id": note_id,
    }


@router.put("/notes/{note_id}")
def update_note(
    note_id: str,
    note: Note,
    current_user: dict = Depends(get_current_user),
):
    try:
        existing_note = db_get_note(note_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID",
        )

    if existing_note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    if (
        current_user["role"] != "admin"
        and existing_note.get("user_id") != str(current_user["_id"])
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only update your own notes",
        )

    db_update_note(
        note_id=note_id,
        title=note.title,
        content=note.content,
        tags=note.tags,
    )

    return {
        "message": "Note updated successfully"
    }


@router.delete("/notes/{note_id}")
def delete_note(
    note_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        existing_note = db_get_note(note_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID",
        )

    if existing_note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    if (
        current_user["role"] != "admin"
        and existing_note.get("user_id") != str(current_user["_id"])
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own notes",
        )

    db_delete_note(note_id)

    return {
        "message": "Note deleted successfully"
    }
