from sqlalchemy.orm import Session
from . import modelsScript, schemas, security

def create_user(db: Session, user_in: schemas.UserCreate):
    hashed = security.hash_password(user_in.password)
    user = modelsScript.User(username=user_in.username, email=user_in.email, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(modelsScript.User).filter(modelsScript.User.username == username).first()

def create_calculation(db: Session, calc_in: schemas.CalculationCreate, user_id: int | None = None, persist_result: bool = True):
    # compute result
    a, b = calc_in.a, calc_in.b
    if calc_in.type == schemas.CalcType.add:
        r = a + b
    elif calc_in.type == schemas.CalcType.subtract:
        r = a - b
    elif calc_in.type == schemas.CalcType.multiply:
        r = a * b
    elif calc_in.type == schemas.CalcType.divide:
        r = a / b
    else:
        raise ValueError("unknown type")

    calc = modelsScript.Calculation(a=a, b=b, type=calc_in.type, result=(r if persist_result else None), user_id=user_id)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc
