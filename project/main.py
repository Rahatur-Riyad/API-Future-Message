from fastapi import FastAPI, Depends, HTTPException, Form, status
from project.auth import verify_password, hash_password, create_token, decode_token
from fastapi.security import OAuth2PasswordBearer
from project.databases.db import get_db, engine
from project.databases.tables import Base, Users, Messages
from sqlalchemy import select
from project.models import CreateUser, CreateMessage
from datetime import datetime, timezone

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    payload = decode_token(token)
    user_id = payload.get("id")
    
    # Fetch user from DB
    query = select(Users).where(Users.id == user_id)
    result = await db.execute(query)
    user_db = result.scalars().first()
    
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": user_db.username, "id": user_db.id}


@app.get("/")
async def root(user = Depends(get_current_user)):
    # This route requires a valid JWT bearer token via Authorization header.
    return {"message": f"Hello {user['username']}"}

@app.post("/register")
async def register(user :CreateUser, db = Depends(get_db)):
    hased_password = hash_password(user.password)
    new_user = Users(username=user.username, password=hased_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"result":"User registered successfully!"}

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db = Depends(get_db)):
    query = select(Users).where(Users.username == username)
    result = await db.execute(query)
    user_db = result.scalars().first()
    if not user_db or not verify_password(password, user_db.password):
        raise HTTPException(status_code=400, detail="Invalid")
    token = create_token(username=user_db.username, id=user_db.id)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/create")
async def create(message :CreateMessage, user = Depends(get_current_user), db = Depends(get_db)):
    new_message = Messages(message_id=message.message_id, user_id=user['id'], body=message.body, opening_time=message.opening_time)
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return {"result":"Message saved successfully!"}

@app.get("/{message_id}")
async def get_message(message_id, user=Depends(get_current_user), db = Depends(get_db)):
    query = select(Messages).where(Messages.message_id == message_id)
    result = await db.execute(query)
    message_db = result.scalars().first()

    if not message_db:
        raise HTTPException(status_code=404, detail="Message not found")

    if message_db.user_id != user["id"]:
        raise HTTPException(status_code=403, detail="You can't access other's data")
    
    if datetime.now() < message_db.opening_time:
        return {"state":"closed","opening_time":f"{message_db.opening_time}"}
    return {"state":"opened","message_body":f"{message_db.body}"}