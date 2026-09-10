# 📝 NoteFlow

NoteFlow is a full-stack note-taking application built with **React, FastAPI, and MongoDB**. It allows users to securely create, manage, search, comment on, and upvote notes.

## 🚀 Features

- User registration and login
- JWT-based authentication
- Secure password hashing
- Create, view, update, and delete notes
- Search notes
- Tags for organizing notes
- Pagination
- Comments on notes
- Upvote and remove upvote
- User profiles and statistics
- Admin functionality
- Role-based authorization
- MongoDB indexing to prevent duplicate votes

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI, Pydantic |
| Authentication | JWT, OAuth2 |
| Database | MongoDB, PyMongo |
| Server | Uvicorn |
| Version Control | Git, GitHub |

## 🏗️ Architecture

```text
┌──────────────────────┐
│   React + Vite       │
│      Frontend        │
└──────────┬───────────┘
           │
           │ HTTP / REST API
           ▼
┌──────────────────────┐
│       FastAPI        │
│       Backend        │
└──────────┬───────────┘
           │
           │ Database Queries
           ▼
┌──────────────────────┐
│       MongoDB        │
│       Database       │
└──────────────────────┘
