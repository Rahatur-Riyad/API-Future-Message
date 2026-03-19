from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from zoneinfo import ZoneInfo
from project.models import Settings

settings = Settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRE_MINUTES = 2

def hash_password(password) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hased = bcrypt.hashpw(password_bytes, salt=salt)
    return hased.decode('utf-8')

def verify_password(plain_password, hased_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hased_password.encode('utf-8'))

def create_token(username: str, id: int, expires_delta: timedelta | None = None) -> str:
    to_encode = {"sub": username, "id": id}
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        id = payload.get("id")
        if (username is None) or (id is None):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username":username, "id":id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )