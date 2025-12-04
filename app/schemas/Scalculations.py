from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator, validator
from typing import Optional
from pytest import Session
from app import CRUD, database
from app.models import calculations
from app.models.Mcalculations import Calculation, CalculationType
from app.schemas import schemas
from sqlalchemy.orm import Session
from .. import CRUD, database, modelsScript

router = APIRouter(prefix="/calculations", tags=["calculations"])

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType

    @model_validator(mode="after")
    def check_division(self):
        if self.type == CalculationType.divide and self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self
    
@router.post("", response_model=schemas.CalculationRead)
def create_calc(calc: CalculationCreate, db: Session = Depends(database.get_db)):
    result = (
        calc.a + calc.b if calc.type == "add"
        else calc.a - calc.b if calc.type == "subtract"
        else None
    )
    new_calc = Calculation(a=calc.a, b=calc.b, type=calc.type, result=result)
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    return new_calc