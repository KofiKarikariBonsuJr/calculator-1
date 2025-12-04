# app/routers/calculations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import modelsScript, schemas, crud, database

router = APIRouter(prefix="/calculations", tags=["calculations"])

@router.post("", response_model=schemas.CalculationRead)
def add_calc(calc_in: schemas.CalculationCreate, db: Session = Depends(database.get_db)):
    calc = crud.create_calculation(db, calc_in)
    return calc

@router.get("", response_model=list[schemas.CalculationRead])
def browse(db: Session = Depends(database.get_db)):
    return db.query(modelsScript.Calculation).all()

@router.get("/{id}", response_model=schemas.CalculationRead)
def read_calc(id: int, db: Session = Depends(database.get_db)):
    calc = db.get(modelsScript.Calculation, id)
    if not calc:
        raise HTTPException(status_code=404, detail="not found")
    return calc

@router.put("/{id}", response_model=schemas.CalculationRead)
def update_calc(id: int, calc_in: schemas.CalculationCreate, db: Session = Depends(database.get_db)):
    calc = db.get(modelsScript.Calculation, id)
    if not calc:
        raise HTTPException(status_code=404, detail="not found")
    # update fields and recompute
    calc.a = calc_in.a
    calc.b = calc_in.b
    calc.type = calc_in.type
    calc.result = crud.create_calculation(db, calc_in, persist_result=True).result
    db.commit()
    db.refresh(calc)
    return calc

@router.delete("/{id}", status_code=204)
def delete_calc(id: int, db: Session = Depends(database.get_db)):
    calc = db.get(modelsScript.Calculation, id)
    if not calc:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(calc)
    db.commit()
    return
