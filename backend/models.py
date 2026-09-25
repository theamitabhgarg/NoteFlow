
from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class Note(BaseModel):
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)


class Comment(BaseModel):
    content: str
