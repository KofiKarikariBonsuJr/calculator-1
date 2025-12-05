from fastapi import FastAPI, Depends, HTTPException
from pathlib import Path
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import status

from app.database import get_db
from app.models.Mcalculations import Calculation
from app.models.Muser import User
from app.schemas.auth import LoginIn, RegisterIn, TokenOut
from app.schemasScript import (
    CalculationCreate, CalculationRead, 
    UserCreate, UserRead
)
from passlib.context import CryptContext

from app.security import create_access_token, hash_password, verify_password

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


app = FastAPI()

@app.post("/add")
async def add_numbers(payload: dict):
    return {"result": payload["a"] + payload["b"]}

@app.post("/calculations", response_model=CalculationRead)
def create_calculation(calc: CalculationCreate, db: Session = Depends(get_db)):
    result = calc.perform()
    db_obj = Calculation(a=calc.a, b=calc.b, type=calc.type.value, result=result)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get("/calculations/{calc_id}", response_model=CalculationRead)
def get_calculation(calc_id: int, db: Session = Depends(get_db)):
    obj = db.query(Calculation).get(calc_id)
    if not obj:
        raise HTTPException(404)
    return obj

@app.post("/users/register", response_model=TokenOut)
def register(user_in: RegisterIn, db: Session = Depends(get_db)):

    if db.query(User).filter((User.email == user_in.email) | (User.username == user_in.username)).first():
        raise HTTPException(status_code=400, detail="username or email already exists")

    u = User(username=user_in.username, email=user_in.email, password_hash=hash_password(user_in.password))
    db.add(u)
    db.commit()
    db.refresh(u)

    token = create_access_token({"sub": user_in.email})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/users/login", response_model=TokenOut)
def login(login_in: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.username == login_in.username).first()
    if not u or not verify_password(login_in.password, u.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=str(u.id))
    return {"access_token": token, "token_type": "bearer"}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    return Path("static/index.html").read_text()

@app.get("/register", response_class=HTMLResponse)
def register_page():
    return FileResponse("static/register.html")

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return FileResponse("static/login.html")