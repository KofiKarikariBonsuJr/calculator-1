from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database, security

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=schemas.UserRead)
def register(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing = db.query(crud.models.User).filter((crud.models.User.username == user_in.username) | (crud.models.User.email == user_in.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="username or email already exists")
    return crud.create_user(db, user_in)

@router.post("/login")
def login(payload: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(crud.models.User).filter(crud.models.User.username == payload.username).first()
    if not user or not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = security.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
