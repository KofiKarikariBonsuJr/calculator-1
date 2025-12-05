from sqlalchemy.orm import Session
from app.models.Mcalculations import Calculation
from app.schemas.Scalculations import CalculationCreate

def create_calculation(db: Session, payload: CalculationCreate | None = None) -> Calculation:

    db_obj = Calculation(
        a=payload.a,
        b=payload.b,
        type=payload.type,

    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
