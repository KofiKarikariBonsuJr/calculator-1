from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.Mcalculations import Calculation
from app.models.Muser import User
from app.schemasScript import (
    CalculationCreate, CalculationRead, 
    UserCreate, UserRead
)

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

@app.post("/users/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email already exists")

    u = User(username=user.username, email=user.email, password_hash=user.password)
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"id": u.id}

@app.post("/users/login")
def login(user: UserRead, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.username == user.username).first()
    if not u or u.password_hash != user.password:
        raise HTTPException(400, "Invalid credentials")
    return {"access_token": "FAKE_TOKEN"}

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    return """
    <html>
        <body>
            <input id="a" type="number">
            <input id="b" type="number">
            <select id="operation">
                <option value="add">Add</option>
                <option value="subtract">Subtract</option>
                <option value="multiply">Multiply</option>
                <option value="divide">Divide</option>
            </select>
            <button id="calculate">Calculate</button>
            <div id="result"></div>
            <script>
                document.getElementById('calculate').onclick = async () => {
                    const a = Number(document.getElementById('a').value);
                    const b = Number(document.getElementById('b').value);
                    const op = document.getElementById('operation').value;
                    const r = await fetch('/' + op, {
                        method: 'POST',
                        headers: {'Content-Type':'application/json'},
                        body: JSON.stringify({a, b})
                    });
                    const data = await r.json();
                    document.getElementById('result').innerText = data.result;
                };
            </script>
        </body>
    </html>
    """