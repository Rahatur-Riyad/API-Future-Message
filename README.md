## Future Messaging System

A simple, secure, and modern messaging system built with FastAPI and SQLite, deployed live on Render.
Users can send messages that are stored safely and can be retrieved instantly.

## Features

-> User authentication (signup/login)
-> Send messages with text body
-> Store messages securely in SQLite database
-> Fully asynchronous API powered by FastAPI
-> Easy to deploy on cloud (Render)
-> Lightweight and beginner-friendly backend project

## Tech Stack

-> Backend: Python 3.11, FastAPI
-> Database: SQLite (local, file-based)
-> Deployment: Render (Free Plan)
-> Dependencies: SQLAlchemy (Async), Uvicorn, aiosqlite, bcrypt

## Live Demo

Deployed and live here: https://your-app-name.onrender.com
Swagger UI: https://your-app-name.onrender.com/docs
Test endpoints directly via browser or Postman

## Folder structure
api-future-message/
├─ project/
│  ├─ databases/
│  │ ├─ db.py          # Database connection (SQLite async)
│  │ └─ tables.py      # SQLAlchemy models (Users, Messages)
│  ├─ auth.py          # JWT auth
│  ├─ main.py          # FastAPI app
│  └─ models.py        # Pydantic validating models (CreateUser, CreateMessage, Settings)
│  
├─ README.md
├─ .env
├─ .gitignore
├─ app.db              #SQLite database
└─ requirements.txt    # Dependencies

## Future Improvements

-> Add frontend UI for users
-> Use PostgreSQL or MySQL for production-ready deployment
-> Add email notifications

## License

This project is open-source. Feel free to use and modify for learning or personal projects.
