# NoteFlow Backend

## Run

From this `backend` folder:

```bash
uvicorn main:app --reload
```

## Database selection

Set `DATABASE_TYPE` in `.env`:

```env
DATABASE_TYPE=mongodb
```

or:

```env
DATABASE_TYPE=postgresql
```

## Structure

- `main.py` - creates the FastAPI application and initializes the selected database.
- `database.py` - MongoDB implementation, PostgreSQL SQLAlchemy models, database connection and database-independent CRUD operations.
- `models.py` - Pydantic request models.
- `auth.py` - password hashing, JWT configuration and current-user authentication.
- `routes/auth_routes.py` - registration and login.
- `routes/user_routes.py` - admin user creation, profiles and statistics.
- `routes/note_routes.py` - note CRUD, search, tags, sorting and pagination.
- `routes/comment_routes.py` - comment CRUD.
- `routes/vote_routes.py` - upvote and remove-upvote endpoints.
- `../seed_postgresql.py` - creates sample PostgreSQL users, notes, comments and votes.

The routes use the database abstraction layer, so they do not need to know whether MongoDB or PostgreSQL is active.
