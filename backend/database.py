from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")

db = client["notes_db"]

users_collection = db["users"]
notes_collection = db["notes"]
comments_collection = db["comments"]
votes_collection = db["votes"]


# Prevent duplicate votes
votes_collection.create_index(
    [("user_id", 1), ("note_id", 1)],
    unique=True
)
