
from database import create_user, get_user_by_username, initialize_database
from pwdlib import PasswordHash


initialize_database()

username = "admin"
password = "admin123"
email = "admin@noteflow.local"

password_hash = PasswordHash.recommended()


if get_user_by_username(username):
    print("Admin already exists")
else:
    create_user(
        username=username,
        email=email,
        password=password_hash.hash(password),
        role="admin",
    )

    print("Admin created successfully")
