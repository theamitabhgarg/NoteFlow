from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.note_routes import router as note_router
from routes.comment_routes import router as comment_router
from routes.vote_routes import router as vote_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "My Notes API is working!"
    }


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(note_router)
app.include_router(comment_router)
app.include_router(vote_router)
