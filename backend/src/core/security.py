from datetime import datetime, timedelta,timezone
from jose import jwt
import bcrypt
from src.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings
from src.db.models import User
from sqlalchemy.orm import Session
from src.db.session import get_db

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# OAuth2PasswordBearer is used to retrieve the token from the "Authorization" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get the current authenticated user based on the JWT token.
    """
    try:
        # Decode the token using the secret key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Query the user by the extracted user ID
        user = db.query(User).filter(User.uuid == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")