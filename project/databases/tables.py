from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    username = Column(String(30),nullable= False, unique=True)
    password = Column(String(255),nullable=False)

class Messages(Base):
    __tablename__ = "messages"

    message_id = Column(String(255),nullable=False,unique=True, primary_key=True)
    user_id = Column(Integer, nullable=False)
    body = Column(Text, nullable= False)
    opening_time = Column(DateTime, nullable=False)