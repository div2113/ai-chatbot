from pwdlib import PasswordHash
from jose import JWTError , jwt
from dotenv import load_dotenv

from datetime import datetime,timedelta,timezone
import os


load_dotenv()
password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password:str):
    return password_hash.verify(password , hashed_password)