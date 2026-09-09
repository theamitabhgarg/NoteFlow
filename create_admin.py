from pymongo import MongoClient
from pwdlib import PasswordHash


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")

db = client["notes_db"]

users_collection = db["users"]

password_hash = PasswordHash.recommended()


# Admin credentials
username = "admin"
password = "admin123"


# Check if admin already exists
existing_user = users_collection.find_one(
    {"username": username}
)


if existing_user:

    print("Admin already exists")

else:

    hashed_password = password_hash.hash(
        password
    )

    users_collection.insert_one(
        {
            "username": username,
            "password": hashed_password,
            "role": "admin"
        }
    )

    print("Admin created successfully")