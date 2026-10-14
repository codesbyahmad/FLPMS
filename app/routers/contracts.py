from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import Contract, User, ContractStatus
from ..schemas import ContractIn, ContractOut, ContractMath
from ..deps import current_user
from ..services.pension import contract_math, compute_advance

router = APIRouter(prefix="/contracts", tags=["contracts"])

@router.get("", response_model=List[ContractOut])
def list_contracts(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(Contract).all()

@router.post("", response_model=ContractOut)
def create_contract(payload: ContractIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    adv = compute_advance(payload.advance_mode, payload.area_acres,
                          payload.advance_rate_per_acre, payload.advance_lump_sum)
    c = Contract(**payload.model_dump(), advance_amount=adv, status=ContractStatus.DRAFT)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("/{cid}/math", response_model=ContractMath)
def get_math(cid: UUID, db: Session = Depends(get_db), _: User = Depends(current_user)):
    c = db.query(Contract).get(cid)
    if not c: raise HTTPException(404, "Contract not found")
    return contract_math(c.area_acres, c.rate_per_acre, c.advance_amount)

@router.post("/{cid}/activate", response_model=ContractOut)
def activate(cid: UUID, db: Session = Depends(get_db), _: User = Depends(current_user)):
    c = db.query(Contract).get(cid)
    if not c: raise HTTPException(404, "Contract not found")
    c.status = ContractStatus.ACTIVE
    db.commit(); db.refresh(c)
    # Trigger creates pension schedule automatically
    return c

@router.post("/preview-math", response_model=ContractMath)
def preview_math(payload: ContractIn, _: User = Depends(current_user)):
    adv = compute_advance(payload.advance_mode, payload.area_acres,
                          payload.advance_rate_per_acre, payload.advance_lump_sum)
    return contract_math(payload.area_acres, payload.rate_per_acre, adv)