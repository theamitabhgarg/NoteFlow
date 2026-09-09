from fastapi import APIRouter, Depends, HTTPException

from bson import ObjectId

from database import notes_collection, users_collection, comments_collection, votes_collection

from models import Note

from auth import get_current_user

from datetime import datetime, timezone

router = APIRouter()


@router.get("/notes")
def get_notes(
    search: str | None = None,
    tag: str | None = None,
    sort: str = "newest",
    page: int = 1,
    limit: int = 10
):

    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be 1 or greater"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )

    query = {}

    # -----------------------------
    # SEARCH
    # -----------------------------

    if search:

        query["$or"] = [
            {
                "title": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "content": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "tags": {
                    "$regex": search,
                    "$options": "i"
                }
            }
        ]

    # -----------------------------
    # TAG FILTER
    # -----------------------------

    if tag:

        query["tags"] = {
            "$in": [tag]
        }

    # -----------------------------
    # COUNT
    # -----------------------------

    total_notes = notes_collection.count_documents(query)

    # -----------------------------
    # PAGINATION
    # -----------------------------

    skip = (page - 1) * limit

    # -----------------------------
    # SORT
    # -----------------------------

    if sort == "popular":

        notes_cursor = notes_collection.find(query).sort(
            "upvote_count",
            -1
        )

    elif sort == "oldest":

        notes_cursor = notes_collection.find(query).sort(
            "created_at",
            1
        )

    elif sort == "newest":

        notes_cursor = notes_collection.find(query).sort(
            "created_at",
            -1
        )

    else:

        raise HTTPException(
            status_code=400,
            detail="Sort must be popular, newest, or oldest"
        )

    # -----------------------------
    # PAGINATION
    # -----------------------------

    notes_cursor = notes_cursor.skip(skip).limit(limit)

    result = []

    for note in notes_cursor:

        username = None

        if note.get("user_id"):
            user = users_collection.find_one({
                "_id": ObjectId(note["user_id"])
            })

            if user:
                username = user["username"]

        result.append({
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"],
            "user_id": note.get("user_id"),
            "username": username,
            "tags": note.get("tags", []),
            "created_at": note.get("created_at"),
            "updated_at": note.get("updated_at"),
            "comment_count": note.get("comment_count", 0),
            "upvote_count": note.get("upvote_count", 0)
        })

    total_pages = (total_notes + limit - 1) // limit

    return {
        "notes": result,
        "page": page,
        "limit": limit,
        "total_notes": total_notes,
        "total_pages": total_pages
    }


@router.get("/notes/mine")
def get_my_notes(
    search: str | None = None,
    tag: str | None = None,
    sort: str = "newest",
    page: int = 1,
    limit: int = 8,
    current_user: dict = Depends(get_current_user)
):

    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be 1 or greater"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )

    user_id = str(current_user["_id"])

    query = {"user_id": user_id}

    if search:
        query["$or"] = [
            {
                "title": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "content": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "tags": {
                    "$regex": search,
                    "$options": "i"
                }
            }
        ]

    if tag:
        query["tags"] = {"$in": [tag]}

    total_notes = notes_collection.count_documents(query)
    skip = (page - 1) * limit

    if sort == "popular":
        notes_cursor = notes_collection.find(query).sort("upvote_count", -1)
    elif sort == "oldest":
        notes_cursor = notes_collection.find(query).sort("created_at", 1)
    elif sort == "newest":
        notes_cursor = notes_collection.find(query).sort("created_at", -1)
    else:
        raise HTTPException(
            status_code=400,
            detail="Sort must be popular, newest, or oldest"
        )

    notes_cursor = notes_cursor.skip(skip).limit(limit)

    result = []

    for note in notes_cursor:
        result.append({
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"],
            "user_id": note.get("user_id"),
            "username": current_user["username"],
            "tags": note.get("tags", []),
            "created_at": note.get("created_at"),
            "updated_at": note.get("updated_at"),
            "comment_count": note.get("comment_count", 0),
            "upvote_count": note.get("upvote_count", 0)
        })

    total_pages = (total_notes + limit - 1) // limit

    return {
        "notes": result,
        "page": page,
        "limit": limit,
        "total_notes": total_notes,
        "total_pages": total_pages
    }


@router.get("/tags")
def get_tags():
    tags = notes_collection.distinct("tags")
    tags = sorted(tag for tag in tags if tag)
    return {"tags": tags}


@router.get("/notes/{note_id}")
def get_note(note_id: str):

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

    username = None

    if note.get("user_id"):

        user = users_collection.find_one({
            "_id": ObjectId(note["user_id"])
        })

        if user:
            username = user["username"]

    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "content": note["content"],
        "user_id": note.get("user_id"),
        "username": username,
        "tags": note.get("tags", []),
        "created_at": note.get("created_at"),
        "updated_at": note.get("updated_at"),
        "comment_count": note.get("comment_count", 0),
        "upvote_count": note.get("upvote_count", 0)
    }


@router.post("/notes")
def create_note(
    note: Note,
    current_user: dict = Depends(get_current_user)
):

    now = datetime.now(timezone.utc)

    new_note = {
        "title": note.title,
        "content": note.content,
        "tags": note.tags,
        "user_id": str(current_user["_id"]),
        "created_at": now,
        "updated_at": now,
        "comment_count": 0,
        "upvote_count": 0
    }

    result = notes_collection.insert_one(new_note)

    return {
        "message": "Note created successfully",
        "note_id": str(result.inserted_id)
    }


@router.put("/notes/{note_id}")
def update_note(
    note_id: str,
    note: Note,
    current_user: dict = Depends(get_current_user)
):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID"
        )

    existing_note = notes_collection.find_one({
        "_id": ObjectId(note_id)
    })

    if existing_note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    if (
        current_user["role"] != "admin"
        and existing_note.get("user_id") != str(current_user["_id"])
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only update your own notes"
        )

    notes_collection.update_one(
        {"_id": ObjectId(note_id)},
        {
            "$set": {
                "title": note.title,
                "content": note.content,
                "tags": note.tags,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return {
        "message": "Note updated successfully"
    }


@router.delete("/notes/{note_id}")
def delete_note(
    note_id: str,
    current_user: dict = Depends(get_current_user)
):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID"
        )

    existing_note = notes_collection.find_one({
        "_id": ObjectId(note_id)
    })

    if existing_note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    if (
        current_user["role"] != "admin"
        and existing_note.get("user_id") != str(current_user["_id"])
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own notes"
        )

    notes_collection.delete_one({
        "_id": ObjectId(note_id)
    })

    comments_collection.delete_many({
        "note_id": note_id
    })

    votes_collection.delete_many({
        "note_id": note_id
    })

    return {
        "message": "Note deleted successfully"
    }
