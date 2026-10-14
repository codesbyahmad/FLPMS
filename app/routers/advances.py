from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import Advance, Contract, User
from ..schemas import AdvanceIn, AdvanceOut
from ..deps import current_user

router = APIRouter(prefix="/contracts/{cid}/advances", tags=["advances"])

@router.get("", response_model=List[AdvanceOut])
def list_advances(cid: UUID, db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(Advance).filter(Advance.contract_id == cid).all()

@router.post("", response_model=AdvanceOut)
def add_advance(cid: UUID, payload: AdvanceIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    if not db.query(Contract).get(cid): raise HTTPException(404, "Contract not found")
    a = Advance(contract_id=cid, **payload.model_dump())
    db.add(a); db.commit(); db.refresh(a)
    return a