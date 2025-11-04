from fastapi import FastAPI
from Calculator.Addition import addition
from Calculator.Subtraction import subtraction
from Calculator.Division import division
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()

@app.get("/add")
def add(a: float, b: float):
    return {"result": addition(a, b)}

@app.get("/subtract")
def subtract(a: float, b: float):
    return {"result": subtraction(a, b)}

@app.get("/divide")
def divide(a: float, b: float):
    return {"result": division(a, b)}
