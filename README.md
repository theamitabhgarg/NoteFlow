# NoteFlow

NoteFlow is a full-stack note-taking application that allows users to create, manage, search, and interact with notes.

The project is built using **React + Vite** for the frontend, **FastAPI** for the backend, and **MongoDB** as the database.

It also includes user authentication using **JWT**, password hashing, comments, voting/upvoting, pagination, search, tags, and role-based access control.

---

## Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Project Structure](#-project-structure)
- [How the Application Works](#-how-the-application-works)
- [Authentication](#-authentication)
- [Database](#-database)
- [API Endpoints](#-api-endpoints)
- [Pagination](#-pagination)
- [Search and Tags](#-search-and-tags)
- [Authorization](#-authorization)
- [Getting Started](#-getting-started)
- [Backend Setup](#-backend-setup)
- [Frontend Setup](#-frontend-setup)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [Git and GitHub](#-git-and-github)
- [Future Improvements](#-future-improvements)
- [Learning Objectives](#-learning-objectives)
- [Author](#-author)

---

# About the Project

**NoteFlow** is a full-stack web application designed to provide a simple and efficient platform for managing personal notes.

Users can:

- Register an account
- Log in securely
- Create notes
- View notes
- Edit their notes
- Delete their notes
- Search notes
- Organize notes using tags
- Comment on notes
- Upvote notes
- Remove their upvotes
- View their profile
- View note statistics
- Navigate through notes using pagination

The backend exposes a REST-style API built using FastAPI, while the frontend communicates with the backend using HTTP requests.

MongoDB is used as the primary database because of its flexible document-based data model.

---

# Features

## User Authentication

NoteFlow provides user authentication using:

- User registration
- User login
- Password hashing
- JWT-based authentication
- Protected API endpoints
- Current-user authentication
- Admin authentication

Passwords are never stored directly in plain text. Password hashing is handled using `pwdlib`.

---

## Note Management

Authenticated users can:

- Create notes
- View notes
- Update notes
- Delete notes
- View their own notes
- Search notes
- Filter notes using tags

Users can manage their own notes, while administrators have additional permissions.

---

## Comments

Users can interact with notes using comments.

Comment functionality includes:

- Creating comments
- Viewing comments
- Updating comments
- Deleting comments

Users can modify their own comments, while administrators have additional permissions.

---

## Voting / Upvoting

Users can upvote notes.

The application also prevents the same user from repeatedly voting on the same note.

A unique database index is used on:

```text
user_id + note_id
