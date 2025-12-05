from sqlalchemy.orm import Session

from app.models import Muser
from app.models import Mcalculations
from . import schemasScript, security
from app.models.Muser import User
from app.models.Mcalculations import Calculation


def create_user(db: Session, user_in: schemasScript.UserCreate):
    hashed = security.hash_password(user_in.password)
    user = Muser.User(username=user_in.username, email=user_in.email, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(Muser.User).filter(Muser.User.username == username).first()

def create_calculation(db: Session, calc_in: schemasScript.CalculationCreate | None = None, persist_result: bool = True):

    a, b = calc_in.a, calc_in.b
    if calc_in.type == schemasScript.CalcType.add:
        r = a + b
    elif calc_in.type == schemasScript.CalcType.subtract:
        r = a - b
    elif calc_in.type == schemasScript.CalcType.multiply:
        r = a * b
    elif calc_in.type == schemasScript.CalcType.divide:
        r = a / b
    else:
        raise ValueError("unknown type")

    calc = Mcalculations.Calculation(a=a, b=b, type=calc_in.type, result=(r if persist_result else None))
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc
