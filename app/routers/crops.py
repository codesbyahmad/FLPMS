from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import CropCycle, CropInput, User
from ..schemas import CropCycleIn, CropCycleOut, CropInputIn, CropInputOut
from ..deps import current_user

router = APIRouter(tags=["crops"])

@router.get("/crop-cycles", response_model=List[CropCycleOut])
def list_cycles(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(CropCycle).all()

@router.post("/crop-cycles", response_model=CropCycleOut)
def create_cycle(payload: CropCycleIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    c = CropCycle(**payload.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("/crop-cycles/{cid}/inputs", response_model=List[CropInputOut])
def list_inputs(cid: UUID, db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(CropInput).filter(CropInput.crop_cycle_id == cid).all()

@router.post("/crop-cycles/{cid}/inputs", response_model=CropInputOut)
def add_input(cid: UUID, payload: CropInputIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    if not db.query(CropCycle).get(cid): raise HTTPException(404, "Cycle not found")
    ci = CropInput(crop_cycle_id=cid, **payload.model_dump())
    db.add(ci); db.commit(); db.refresh(ci)
    return ci