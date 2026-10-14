from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import Farm, User
from ..schemas import FarmIn, FarmOut
from ..deps import current_user

router = APIRouter(prefix="/farms", tags=["farms"])

@router.get("", response_model=List[FarmOut])
def list_farms(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(Farm).filter(Farm.is_active == True).all()

@router.post("", response_model=FarmOut)
def create_farm(payload: FarmIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    f = Farm(**payload.model_dump())
    db.add(f); db.commit(); db.refresh(f)
    return f

@router.get("/{farm_id}", response_model=FarmOut)
def get_farm(farm_id: UUID, db: Session = Depends(get_db), _: User = Depends(current_user)):
    f = db.query(Farm).get(farm_id)
    if not f: raise HTTPException(404, "Farm not found")
    return f

@router.patch("/{farm_id}", response_model=FarmOut)
def update_farm(farm_id: UUID, payload: FarmIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    f = db.query(Farm).get(farm_id)
    if not f: raise HTTPException(404, "Farm not found")
    for k, v in payload.model_dump().items():
        setattr(f, k, v)
    db.commit(); db.refresh(f)
    return f