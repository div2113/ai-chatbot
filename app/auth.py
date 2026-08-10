from datetime import datetime,timedelta,timezone
import os

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException , status

from sqlalchemy.orm import Session

from pwdlib import PasswordHash
from jose import JWTError , jwt
from dotenv import load_dotenv

from app.database import get_db
from app import models

load_dotenv()
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password:str):
    return password_hash.verify(password , hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update(
        {
            "exp": expire,
            "type": "access"
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def create_refresh_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update(
        {
            "exp": expire,
            "type":"refresh"
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def get_current_user(
        token:str= Depends(oauth2_scheme),
        db:Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload= jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email=payload.get("sub")
        token_type=payload.get("type")

        if email is None or token_type != "access":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user= db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception

    return user

def get_current_admin(
        current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )

    return current_user

def verify_token(token:str , token_type:str):
    credential_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )

    try:
        payload= jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email =payload.get("sub")
        token_kind = payload.get("type")

        if email is None or token_kind != token_type:
            raise credential_exception

        return email
    
    except JWTError:
        raise credential_exception
