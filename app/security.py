from datetime import datetime, timedelta
from passlib.context import CryptContext
import bcrypt
import os
from jose import jwt

PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = os.getenv("JWT_SECRET", "change-me-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*7

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(subject: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"sub": subject, "exp": expire}

    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])