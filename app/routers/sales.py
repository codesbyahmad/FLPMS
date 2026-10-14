from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from decimal import Decimal
from ..database import get_db
from ..models import MarketSale, CropCycle, User
from ..schemas import MarketSaleIn, MarketSaleOut
from ..deps import current_user

router = APIRouter(tags=["sales"])

@router.get("/crop-cycles/{cid}/sales", response_model=List[MarketSaleOut])
def list_sales(cid: UUID, db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(MarketSale).filter(MarketSale.crop_cycle_id == cid).all()

@router.post("/crop-cycles/{cid}/sales", response_model=MarketSaleOut)
def add_sale(cid: UUID, payload: MarketSaleIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    if not db.query(CropCycle).get(cid): raise HTTPException(404, "Cycle not found")
    gross = (payload.quantity * payload.rate).quantize(Decimal("0.01"))
    net = (gross - payload.market_fee - payload.commission - payload.transport - payload.other_deduction).quantize(Decimal("0.01"))
    s = MarketSale(crop_cycle_id=cid, gross_amount=gross, net_amount=net, **payload.model_dump())
    db.add(s); db.commit(); db.refresh(s)
    return s