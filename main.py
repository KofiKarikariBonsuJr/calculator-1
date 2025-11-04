from fastapi import FastAPI
from Calculator.Addition import addition
from Calculator.Subtraction import subtraction
from Calculator.Division import division
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()

class Numbers(BaseModel):
    a: float
    b: float

@app.post("/add")
def add(nums: Numbers):
    return {"result": nums.a + nums.b}

@app.post("/subtract")
def subtract(nums: Numbers):
    return {"result": nums.a - nums.b}

@app.post("/divide")
def divide(nums: Numbers):
    return {"result": nums.a / nums.b}
