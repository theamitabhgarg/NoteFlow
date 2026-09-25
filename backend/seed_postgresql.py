
import random

from pwdlib import PasswordHash

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from database import (
    DATABASE_TYPE,
    add_vote,
    create_comment,
    create_note,
    create_user,
    get_user_by_username,
    initialize_database,
)

if DATABASE_TYPE != "postgresql":
    raise SystemExit(
        "Set DATABASE_TYPE=postgresql in backend/.env before running this script."
    )

initialize_database()

password_hash = PasswordHash.recommended()

users_data = [
    ("alex", "alex@example.com"),
    ("priya", "priya@example.com"),
    ("rahul", "rahul@example.com"),
    ("ananya", "ananya@example.com"),
    ("karan", "karan@example.com"),
    ("meera", "meera@example.com"),
]

user_ids = []

for username, email in users_data:
    user = get_user_by_username(username)

    if not user:
        user = create_user(
            username=username,
            email=email,
            password=password_hash.hash("password123"),
            role="user",
        )

    user_ids.append(str(user["_id"]))


notes_data = [
    ("Learning PostgreSQL", "Today I started learning relational databases.", ["postgresql", "sql"]),
    ("FastAPI Notes", "FastAPI makes it easy to build REST APIs in Python.", ["python", "fastapi"]),
    ("Machine Learning", "A collection of notes about supervised learning.", ["ml", "python"]),
    ("OpenCV Project", "Ideas for improving my computer vision projects.", ["opencv", "computer-vision"]),
    ("Git Commands", "Useful Git commands for everyday development.", ["git", "github"]),
    ("Database Design", "Thinking about tables, keys, relationships and indexes.", ["postgresql", "database"]),
    ("SQL Joins", "INNER JOIN, LEFT JOIN and other useful joins.", ["sql", "postgresql"]),
    ("Backend Architecture", "Separating API logic from database logic.", ["fastapi", "backend"]),
    ("Python Tips", "Small Python techniques that are useful in projects.", ["python"]),
    ("Project Ideas", "Ideas for future backend and machine learning projects.", ["projects"]),
]

note_ids = []

# Only add the sample notes if they do not already exist in this seed run.
# The script is intentionally simple: running it again adds another sample set.
for index, (title, content, tags) in enumerate(notes_data):
    user_id = user_ids[index % len(user_ids)]

    note_id = create_note(
        title=title,
        content=content,
        tags=tags,
        user_id=user_id,
    )

    note_ids.append(note_id)

for index, note_id in enumerate(note_ids):
    comment_user = user_ids[(index + 1) % len(user_ids)]

    create_comment(
        note_id=note_id,
        user_id=comment_user,
        content=random.choice([
            "Great note!",
            "This was useful.",
            "I want to learn this too.",
            "Nice explanation.",
            "Adding this to my revision list.",
        ]),
    )

    # Add a few more comments to some notes.
    if index % 3 == 0:
        create_comment(
            note_id=note_id,
            user_id=user_ids[(index + 2) % len(user_ids)],
            content="Thanks for sharing this.",
        )

    # Randomly add 1-4 votes.
    voters = random.sample(
        user_ids,
        k=random.randint(1, min(4, len(user_ids))),
    )

    for voter_id in voters:
        try:
            add_vote(
                note_id=note_id,
                user_id=voter_id,
            )
        except ValueError:
            pass

print("PostgreSQL sample data created successfully.")
print(f"Users: {len(user_ids)}")
print(f"Notes: {len(note_ids)}")
print("Comments and votes were generated randomly.")
print("All sample user passwords are: password123")
