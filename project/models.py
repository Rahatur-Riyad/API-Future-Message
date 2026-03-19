from pydantic import BaseModel
from pydantic_settings import BaseSettings
from datetime import datetime

class CreateUser(BaseModel):
    username :str
    password :str

class CreateMessage(BaseModel):
    message_id :str
    body :str
    opening_time :datetime

class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"

    class Config:
        env_file=".env"

