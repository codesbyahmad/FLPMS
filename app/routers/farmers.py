from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import Farmer, User
from ..schemas import FarmerIn, FarmerOut
from ..deps import current_user

router = APIRouter(prefix="/farmers", tags=["farmers"])

@router.get("", response_model=List[FarmerOut])
def list_farmers(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(Farmer).filter(Farmer.is_active == True).all()

@router.post("", response_model=FarmerOut)
def create_farmer(payload: FarmerIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    f = Farmer(**payload.model_dump())
    db.add(f); db.commit(); db.refresh(f)
    return f

@router.get("/{fid}", response_model=FarmerOut)
def get_farmer(fid: UUID, db: Session = Depends(get_db), _: User = Depends(current_user)):
    f = db.query(Farmer).get(fid)
    if not f: raise HTTPException(404, "Farmer not found")
    return f