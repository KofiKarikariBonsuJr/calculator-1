from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.models.user import User, Base as UserBase
from app.models.calculations import Calculation, Base as CalcBase
from app.schemas.schemas import UserCreate, UserRead, CalculationCreate, CalculationRead
from app.database import engine, get_db
from app.security import verify_password, hash_password

app = FastAPI()

# ---------- Create tables for tests ----------
UserBase.metadata.create_all(bind=engine)
CalcBase.metadata.create_all(bind=engine)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# USERS
# =====================================================

@app.post("/users/register")
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    # Check unique constraints
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}



# =====================================================
# CALCULATIONS
# =====================================================

@app.post("/calculations", response_model=CalculationRead)
def create_calc(payload: CalculationCreate, db: Session = Depends(get_db)):
    # Perform the calculation
    if payload.type == "add":
        result = payload.a + payload.b
    elif payload.type == "subtract":
        result = payload.a - payload.b
    elif payload.type == "multiply":
        result = payload.a * payload.b
    elif payload.type == "divide":
        if payload.b == 0:
            raise HTTPException(status_code=400, detail="Division by zero")
        result = payload.a / payload.b
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    calc = Calculation(a=payload.a, b=payload.b, type=payload.type, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)

    return calc


@app.get("/calculations/{calc_id}", response_model=CalculationRead)
def read_calc(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc
