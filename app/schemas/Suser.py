from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.Muser import User
from .. import CRUD, database, security


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str   

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: str

    class Config:
        orm_mode = True

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = security.hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(payload: UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"access_token": "dummy-token", "token_type": "bearer"}