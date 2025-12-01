from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import CalculationCreate, CalculationRead, CalculationUpdate
from app import crud

router = APIRouter(prefix="/calculations", tags=["Calculations"])


@router.get("/", response_model=list[CalculationRead])
def get_all(db: Session = Depends(get_db)):
    return crud.get_all_calculations(db)


@router.get("/{calc_id}", response_model=CalculationRead)
def get_one(calc_id: int, db: Session = Depends(get_db)):
    result = crud.get_calculation(db, calc_id)
    if not result:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return result


@router.post("/", response_model=CalculationRead)
def create(calc: CalculationCreate, db: Session = Depends(get_db)):
    return crud.create_calculation(db, calc)


@router.put("/{calc_id}", response_model=CalculationRead)
def update(calc_id: int, updates: CalculationUpdate, db: Session = Depends(get_db)):
    updated = crud.update_calculation(db, calc_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return updated


@router.delete("/{calc_id}")
def delete(calc_id: int, db: Session = Depends(get_db)):
    success = crud.delete_calculation(db, calc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return {"message": "Deleted"}
