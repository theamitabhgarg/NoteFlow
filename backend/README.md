# NoteFlow Backend - Refactored

## Run

From this `backend` folder:

```bash
uvicorn main:app --reload
```

## Structure

- `main.py` - creates the FastAPI application and registers routers.
- `database.py` - MongoDB connection, collections, and database indexes.
- `models.py` - Pydantic request models.
- `auth.py` - password hashing, JWT configuration, and current-user authentication.
- `routes/auth_routes.py` - registration and login.
- `routes/user_routes.py` - admin user creation, profiles, and statistics.
- `routes/note_routes.py` - note CRUD, search, tags, sorting, and pagination.
- `routes/comment_routes.py` - comment CRUD.
- `routes/vote_routes.py` - upvote and remove-upvote endpoints.
