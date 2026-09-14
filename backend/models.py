from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class Note(BaseModel):
    title: str
    content: str
    tags: list[str] = []


class Comment(BaseModel):
    content: str