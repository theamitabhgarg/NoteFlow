
import os
from datetime import datetime, timezone
from typing import Optional

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
    or_,
    cast,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "mongodb").lower()

# ---------------------------------------------------------------------------
# MongoDB
# ---------------------------------------------------------------------------

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "notes_db")

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client[MONGO_DATABASE]

users_collection = mongo_db["users"]
notes_collection = mongo_db["notes"]
comments_collection = mongo_db["comments"]
votes_collection = mongo_db["votes"]

# Prevent duplicate votes in MongoDB.
votes_collection.create_index(
    [("user_id", 1), ("note_id", 1)],
    unique=True
)

# ---------------------------------------------------------------------------
# PostgreSQL
# ---------------------------------------------------------------------------

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "noteflow")

POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    (
        f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    )
)

postgres_engine = create_engine(
    POSTGRES_URL,
    pool_pre_ping=True,
)

PostgresSessionLocal = sessionmaker(
    bind=postgres_engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="user")


class NoteTable(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tags = Column(ARRAY(Text), nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    comment_count = Column(Integer, nullable=False, default=0)
    upvote_count = Column(Integer, nullable=False, default=0)


class CommentTable(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    note_id = Column(
        Integer,
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)


class VoteTable(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    note_id = Column(
        Integer,
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    vote = Column(Integer, nullable=False, default=1)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "note_id",
            name="uq_vote_user_note",
        ),
    )


def initialize_database():
    """Create PostgreSQL tables when PostgreSQL mode is selected."""
    if DATABASE_TYPE == "postgresql":
        Base.metadata.create_all(bind=postgres_engine)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now():
    return datetime.now(timezone.utc)


def _mongo_object_id(value: str):
    if not ObjectId.is_valid(value):
        raise ValueError("Invalid ID")
    return ObjectId(value)


def _postgres_id(value: str):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValueError("Invalid ID")

    if parsed <= 0:
        raise ValueError("Invalid ID")

    return parsed


def is_postgresql():
    return DATABASE_TYPE == "postgresql"


def is_mongodb():
    return DATABASE_TYPE == "mongodb"


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------

def get_user_by_username(username: str):
    if is_mongodb():
        user = users_collection.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])
        return user

    with PostgresSessionLocal() as session:
        user = (
            session.query(UserTable)
            .filter(UserTable.username == username)
            .first()
        )

        if not user:
            return None

        return _user_to_dict(user)


def get_user_by_email(email: str):
    if is_mongodb():
        user = users_collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user

    with PostgresSessionLocal() as session:
        user = (
            session.query(UserTable)
            .filter(UserTable.email == email)
            .first()
        )

        if not user:
            return None

        return _user_to_dict(user)


def get_user_by_id(user_id: str):
    if is_mongodb():
        oid = _mongo_object_id(user_id)
        user = users_collection.find_one({"_id": oid})
        if user:
            user["_id"] = str(user["_id"])
        return user

    parsed_id = _postgres_id(user_id)

    with PostgresSessionLocal() as session:
        user = (
            session.query(UserTable)
            .filter(UserTable.id == parsed_id)
            .first()
        )

        if not user:
            return None

        return _user_to_dict(user)


def create_user(username: str, email: Optional[str], password: str, role="user"):
    if is_mongodb():
        document = {
            "username": username,
            "email": email,
            "password": password,
            "role": role,
        }

        try:
            result = users_collection.insert_one(document)
        except DuplicateKeyError:
            raise ValueError("Username or email already exists")

        document["_id"] = str(result.inserted_id)
        return document

    with PostgresSessionLocal() as session:
        existing_username = (
            session.query(UserTable)
            .filter(UserTable.username == username)
            .first()
        )

        if existing_username:
            raise ValueError("Username already exists")

        if email:
            existing_email = (
                session.query(UserTable)
                .filter(UserTable.email == email)
                .first()
            )

            if existing_email:
                raise ValueError("Email already exists")

        user = UserTable(
            username=username,
            email=email,
            password=password,
            role=role,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return _user_to_dict(user)


def get_all_users_except(user_id: str):
    if is_mongodb():
        oid = _mongo_object_id(user_id)

        users = users_collection.find({
            "_id": {"$ne": oid}
        })

        result = []
        for user in users:
            user["_id"] = str(user["_id"])
            result.append(user)

        return result

    parsed_id = _postgres_id(user_id)

    with PostgresSessionLocal() as session:
        users = (
            session.query(UserTable)
            .filter(UserTable.id != parsed_id)
            .all()
        )

        return [_user_to_dict(user) for user in users]


def _user_to_dict(user):
    return {
        "_id": str(user.id),
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "role": user.role,
    }


# ---------------------------------------------------------------------------
# Note operations
# ---------------------------------------------------------------------------

def get_notes(
    search=None,
    tag=None,
    sort="newest",
    page=1,
    limit=10,
    user_id=None,
):
    if is_mongodb():
        query = {}

        if user_id:
            query["user_id"] = user_id

        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"tags": {"$regex": search, "$options": "i"}},
            ]

        if tag:
            query["tags"] = {"$in": [tag]}

        total = notes_collection.count_documents(query)

        sort_field = {
            "popular": ("upvote_count", -1),
            "newest": ("created_at", -1),
            "oldest": ("created_at", 1),
        }.get(sort)

        if not sort_field:
            raise ValueError("Invalid sort")

        skip = (page - 1) * limit

        cursor = (
            notes_collection
            .find(query)
            .sort(*sort_field)
            .skip(skip)
            .limit(limit)
        )

        result = []

        for note in cursor:
            result.append(_mongo_note_to_dict(note))

        return result, total

    parsed_user_id = _postgres_id(user_id) if user_id else None

    with PostgresSessionLocal() as session:
        query = session.query(NoteTable)

        if parsed_user_id:
            query = query.filter(NoteTable.user_id == parsed_user_id)

        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                or_(
                    NoteTable.title.ilike(search_pattern),
                    NoteTable.content.ilike(search_pattern),
                    cast(NoteTable.tags, Text).ilike(search_pattern),
                )
            )

        if tag:
            query = query.filter(NoteTable.tags.any(tag))

        if sort == "popular":
            query = query.order_by(NoteTable.upvote_count.desc())
        elif sort == "newest":
            query = query.order_by(NoteTable.created_at.desc())
        elif sort == "oldest":
            query = query.order_by(NoteTable.created_at.asc())
        else:
            raise ValueError("Invalid sort")

        total = query.count()

        offset = (page - 1) * limit

        notes = query.offset(offset).limit(limit).all()

        result = []

        for note in notes:
            result.append(_postgres_note_to_dict(session, note))

        return result, total


def get_note(note_id: str):
    if is_mongodb():
        oid = _mongo_object_id(note_id)

        note = notes_collection.find_one({
            "_id": oid
        })

        if not note:
            return None

        return _mongo_note_to_dict(note)

    parsed_id = _postgres_id(note_id)

    with PostgresSessionLocal() as session:
        note = (
            session.query(NoteTable)
            .filter(NoteTable.id == parsed_id)
            .first()
        )

        if not note:
            return None

        return _postgres_note_to_dict(session, note)


def create_note(title, content, tags, user_id):
    now = _now()

    if is_mongodb():
        document = {
            "title": title,
            "content": content,
            "tags": tags,
            "user_id": user_id,
            "created_at": now,
            "updated_at": now,
            "comment_count": 0,
            "upvote_count": 0,
        }

        result = notes_collection.insert_one(document)
        return str(result.inserted_id)

    parsed_user_id = _postgres_id(user_id)

    with PostgresSessionLocal() as session:
        note = NoteTable(
            title=title,
            content=content,
            tags=tags,
            user_id=parsed_user_id,
            created_at=now,
            updated_at=now,
            comment_count=0,
            upvote_count=0,
        )

        session.add(note)
        session.commit()
        session.refresh(note)

        return str(note.id)


def update_note(note_id, title, content, tags):
    if is_mongodb():
        oid = _mongo_object_id(note_id)

        result = notes_collection.update_one(
            {"_id": oid},
            {
                "$set": {
                    "title": title,
                    "content": content,
                    "tags": tags,
                    "updated_at": _now(),
                }
            },
        )

        return result.matched_count > 0

    parsed_id = _postgres_id(note_id)

    with PostgresSessionLocal() as session:
        note = (
            session.query(NoteTable)
            .filter(NoteTable.id == parsed_id)
            .first()
        )

        if not note:
            return False

        note.title = title
        note.content = content
        note.tags = tags
        note.updated_at = _now()

        session.commit()

        return True


def delete_note(note_id):
    if is_mongodb():
        oid = _mongo_object_id(note_id)

        result = notes_collection.delete_one({
            "_id": oid
        })

        comments_collection.delete_many({
            "note_id": note_id
        })

        votes_collection.delete_many({
            "note_id": note_id
        })

        return result.deleted_count > 0

    parsed_id = _postgres_id(note_id)

    with PostgresSessionLocal() as session:
        note = (
            session.query(NoteTable)
            .filter(NoteTable.id == parsed_id)
            .first()
        )

        if not note:
            return False

        session.delete(note)
        session.commit()

        return True


def get_tags():
    if is_mongodb():
        tags = notes_collection.distinct("tags")
        return sorted(tag for tag in tags if tag)

    with PostgresSessionLocal() as session:
        rows = session.query(NoteTable.tags).all()

        tags = set()

        for row in rows:
            for tag in row[0] or []:
                if tag:
                    tags.add(tag)

        return sorted(tags)


def _mongo_note_to_dict(note):
    username = None

    if note.get("user_id") and ObjectId.is_valid(note["user_id"]):
        user = users_collection.find_one({
            "_id": ObjectId(note["user_id"])
        })

        if user:
            username = user.get("username")

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
        "upvote_count": note.get("upvote_count", 0),
    }


def _postgres_note_to_dict(session, note):
    user = (
        session.query(UserTable)
        .filter(UserTable.id == note.user_id)
        .first()
    )

    return {
        "id": str(note.id),
        "title": note.title,
        "content": note.content,
        "user_id": str(note.user_id),
        "username": user.username if user else None,
        "tags": note.tags or [],
        "created_at": note.created_at,
        "updated_at": note.updated_at,
        "comment_count": note.comment_count,
        "upvote_count": note.upvote_count,
    }


# ---------------------------------------------------------------------------
# Comment operations
# ---------------------------------------------------------------------------

def get_comments(note_id):
    if is_mongodb():
        note_oid = _mongo_object_id(note_id)

        if not notes_collection.find_one({"_id": note_oid}):
            return None

        comments = (
            comments_collection
            .find({"note_id": note_id})
            .sort("created_at", 1)
        )

        result = []

        for comment in comments:
            username = None

            if comment.get("user_id") and ObjectId.is_valid(comment["user_id"]):
                user = users_collection.find_one({
                    "_id": ObjectId(comment["user_id"])
                })

                if user:
                    username = user.get("username")

            result.append({
                "id": str(comment["_id"]),
                "note_id": comment["note_id"],
                "user_id": comment["user_id"],
                "username": username,
                "content": comment["content"],
                "created_at": comment.get("created_at"),
                "updated_at": comment.get("updated_at"),
            })

        return result

    parsed_note_id = _postgres_id(note_id)

    with PostgresSessionLocal() as session:
        note = (
            session.query(NoteTable)
            .filter(NoteTable.id == parsed_note_id)
            .first()
        )

        if not note:
            return None

        comments = (
            session.query(CommentTable, UserTable.username)
            .join(UserTable, UserTable.id == CommentTable.user_id)
            .filter(CommentTable.note_id == parsed_note_id)
            .order_by(CommentTable.created_at.asc())
            .all()
        )

        return [
            {
                "id": str(comment.id),
                "note_id": str(comment.note_id),
                "user_id": str(comment.user_id),
                "username": username,
                "content": comment.content,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at,
            }
            for comment, username in comments
        ]


def create_comment(note_id, user_id, content):
    now = _now()

    if is_mongodb():
        note_oid = _mongo_object_id(note_id)

        note = notes_collection.find_one({"_id": note_oid})

        if not note:
            return None

        document = {
            "note_id": note_id,
            "user_id": user_id,
            "content": content,
            "created_at": now,
            "updated_at": now,
        }

        result = comments_collection.insert_one(document)

        notes_collection.update_one(
            {"_id": note_oid},
            {"$inc": {"comment_count": 1}},
        )

        return {
            "id": str(result.inserted_id),
            "note": note,
        }

    parsed_note_id = _postgres_id(note_id)
    parsed_user_id = _postgres_id(user_id)

    with PostgresSessionLocal() as session:
        note = (
            session.query(NoteTable)
            .filter(NoteTable.id == parsed_note_id)
            .first()
        )

        if not note:
            return None

        comment = CommentTable(
            note_id=parsed_note_id,
            user_id=parsed_user_id,
            content=content,
            created_at=now,
            updated_at=now,
        )

        session.add(comment)
        note.comment_count += 1

        session.commit()
        session.refresh(comment)

        return {
            "id": str(comment.id),
            "note": _postgres_note_to_dict(session, note),
        }


def get_comment(comment_id):
    if is_mongodb():
        oid = _mongo_object_id(comment_id)
        comment = comments_collection.find_one({"_id": oid})

        if comment:
            comment["_id"] = str(comment["_id"])

        return comment

    parsed_id = _postgres_id(comment_id)

    with PostgresSessionLocal() as session:
        comment = (
            session.query(CommentTable)
            .filter(CommentTable.id == parsed_id)
            .first()
        )

        if not comment:
            return None

        return {
            "_id": str(comment.id),
            "note_id": str(comment.note_id),
            "user_id": str(comment.user_id),
            "content": comment.content,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
        }


def update_comment(comment_id, content):
    if is_mongodb():
        oid = _mongo_object_id(comment_id)

        result = comments_collection.update_one(
            {"_id": oid},
            {
                "$set": {
                    "content": content,
                    "updated_at": _now(),
                }
            },
        )

        return result.matched_count > 0

    parsed_id = _postgres_id(comment_id)

    with PostgresSessionLocal() as session:
        comment = (
            session.query(CommentTable)
            .filter(CommentTable.id == parsed_id)
            .first()
        )

        if not comment:
            return False

        comment.content = content
        comment.updated_at = _now()

        session.commit()

        return True


def delete_comment(comment_id):
    if is_mongodb():
        oid = _mongo_object_id(comment_id)

        comment = comments_collection.find_one({"_id": oid})

        if not comment:
            return None

        comments_collection.delete_one({"_id": oid})

        notes_collection.update_one(
            {"_id": ObjectId(comment["note_id"])},
            {"$inc": {"comment_count": -1}},
        )

        return comment

    parsed_id = _postgres_id(comment_id)

    with PostgresSessionLocal() as session:
        comment = (
            session.query(CommentTable)
            .filter(CommentTable.id == parsed_id)
            .first()
        )

        if not comment:
            return None

        result = {
            "_id": str(comment.id),
            "note_id": str(comment.note_id),
            "user_id": str(comment.user_id),
        }

        note = (
            session.query(NoteTable)
            .filter(NoteTable.id == comment.note_id)
            .first()
        )

        if note and note.comment_count > 0:
            note.comment_count -= 1

        session.delete(comment)
        session.commit()

        return result


# ---------------------------------------------------------------------------
# Vote operations
# ---------------------------------------------------------------------------

def add_vote(note_id, user_id):
    if is_mongodb():
        note_oid = _mongo_object_id(note_id)

        note = notes_collection.find_one({"_id": note_oid})

        if not note:
            return None

        try:
            votes_collection.insert_one({
                "note_id": note_id,
                "user_id": user_id,
                "vote": 1,
            })
        except DuplicateKeyError:
            raise ValueError("You have already upvoted this note")

        notes_collection.update_one(
            {"_id": note_oid},
            {"$inc": {"upvote_count": 1}},
        )

        return note

    parsed_note_id = _postgres_id(note_id)
    parsed_user_id = _postgres_id(user_id)

    with PostgresSessionLocal() as session:
        note = (
            session.query(NoteTable)
            .filter(NoteTable.id == parsed_note_id)
            .first()
        )

        if not note:
            return None

        existing_vote = (
            session.query(VoteTable)
            .filter(
                VoteTable.note_id == parsed_note_id,
                VoteTable.user_id == parsed_user_id,
            )
            .first()
        )

        if existing_vote:
            raise ValueError("You have already upvoted this note")

        vote = VoteTable(
            note_id=parsed_note_id,
            user_id=parsed_user_id,
            vote=1,
        )

        session.add(vote)
        note.upvote_count += 1

        session.commit()

        return _postgres_note_to_dict(session, note)


def remove_vote(note_id, user_id):
    if is_mongodb():
        note_oid = _mongo_object_id(note_id)

        note = notes_collection.find_one({"_id": note_oid})

        if not note:
            return None

        existing_vote = votes_collection.find_one({
            "note_id": note_id,
            "user_id": user_id,
        })

        if not existing_vote:
            raise ValueError("You have not upvoted this note")

        votes_collection.delete_one({
            "_id": existing_vote["_id"]
        })

        notes_collection.update_one(
            {"_id": note_oid},
            {"$inc": {"upvote_count": -1}},
        )

        return note

    parsed_note_id = _postgres_id(note_id)
    parsed_user_id = _postgres_id(user_id)

    with PostgresSessionLocal() as session:
        note = (
            session.query(NoteTable)
            .filter(NoteTable.id == parsed_note_id)
            .first()
        )

        if not note:
            return None

        vote = (
            session.query(VoteTable)
            .filter(
                VoteTable.note_id == parsed_note_id,
                VoteTable.user_id == parsed_user_id,
            )
            .first()
        )

        if not vote:
            raise ValueError("You have not upvoted this note")

        session.delete(vote)

        if note.upvote_count > 0:
            note.upvote_count -= 1

        session.commit()

        return _postgres_note_to_dict(session, note)


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def get_user_statistics(user_id):
    if is_mongodb():
        user_notes = list(notes_collection.find({
            "user_id": user_id
        }))

        tag_counts = {}

        for note in user_notes:
            for tag in note.get("tags", []):
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        return {
            "notes_count": len(user_notes),
            "unique_tags": len(tag_counts),
            "upvotes_given": votes_collection.count_documents({
                "user_id": user_id
            }),
            "comments_written": comments_collection.count_documents({
                "user_id": user_id
            }),
            "tag_counts": dict(sorted(tag_counts.items())),
        }

    parsed_user_id = _postgres_id(user_id)

    with PostgresSessionLocal() as session:
        user_notes = (
            session.query(NoteTable)
            .filter(NoteTable.user_id == parsed_user_id)
            .all()
        )

        tag_counts = {}

        for note in user_notes:
            for tag in note.tags or []:
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        return {
            "notes_count": len(user_notes),
            "unique_tags": len(tag_counts),
            "upvotes_given": (
                session.query(VoteTable)
                .filter(VoteTable.user_id == parsed_user_id)
                .count()
            ),
            "comments_written": (
                session.query(CommentTable)
                .filter(CommentTable.user_id == parsed_user_id)
                .count()
            ),
            "tag_counts": dict(sorted(tag_counts.items())),
        }


def get_profile_statistics(user_id):
    if is_mongodb():
        user_notes = list(notes_collection.find({
            "user_id": user_id
        }))

        upvotes_received = sum(
            note.get("upvote_count", 0)
            for note in user_notes
        )

        return {
            "notes_count": len(user_notes),
            "upvotes_received": upvotes_received,
        }

    parsed_user_id = _postgres_id(user_id)

    with PostgresSessionLocal() as session:
        notes_count = (
            session.query(NoteTable)
            .filter(NoteTable.user_id == parsed_user_id)
            .count()
        )

        upvotes_received = (
            session.query(func.coalesce(func.sum(NoteTable.upvote_count), 0))
            .filter(NoteTable.user_id == parsed_user_id)
            .scalar()
        )

        return {
            "notes_count": notes_count,
            "upvotes_received": int(upvotes_received or 0),
        }
