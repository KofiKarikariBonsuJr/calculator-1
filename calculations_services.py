from sqlalchemy.orm import Session
from app.models.calculations import Calculation
from app.schemas.Scalculations import CalculationCreate

def create_calculation(db: Session, payload: CalculationCreate, user_id: int | None = None) -> Calculation:

    db_obj = Calculation(
        a=payload.a,
        b=payload.b,
        type=payload.type,
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
