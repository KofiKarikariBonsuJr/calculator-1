from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.security import hash_password
from Calculator.Addition import addition
from Calculator.Subtraction import subtraction
from Calculator.Division import division
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("calculator")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()

class Numbers(BaseModel):
    a: float
    b: float

@app.post("/add")
def add(nums: Numbers):
     logger.info(f"Received add request: {nums.a} + {nums.b}")
     return {"result": nums.a + nums.b}

@app.post("/subtract")
def subtract(nums: Numbers):
       logger.info(f"Received add request: {nums.a} - {nums.b}")
       return {"result": nums.a - nums.b}

@app.post("/divide")
def divide(nums: Numbers):
       logger.info(f"Received add request: {nums.a} / {nums.b}")
       return {"result": nums.a / nums.b}

app.mount("/", StaticFiles(directory="static", html=True), name="static")