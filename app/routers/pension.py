from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from decimal import Decimal
from ..database import get_db
from ..models import PensionSchedule, PensionPayment, User, PensionStatus
from ..schemas import PensionScheduleOut, PensionPaymentIn, PensionPaymentOut
from ..deps import current_user

router = APIRouter(tags=["pension"])

@router.get("/contracts/{cid}/pension-schedule", response_model=List[PensionScheduleOut])
def schedule(cid: UUID, db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(PensionSchedule).filter(PensionSchedule.contract_id == cid)\
             .order_by(PensionSchedule.installment_no).all()

@router.post("/pension/schedules/{sid}/pay", response_model=PensionPaymentOut)
def pay(sid: UUID, payload: PensionPaymentIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    s = db.query(PensionSchedule).get(sid)
    if not s: raise HTTPException(404, "Schedule not found")
    p = PensionPayment(schedule_id=sid, **payload.model_dump())
    db.add(p); db.flush()

    paid_total = sum([x.amount_paid for x in db.query(PensionPayment).filter(PensionPayment.schedule_id == sid).all()])
    if paid_total >= s.amount_due:
        s.status = PensionStatus.PAID
    elif paid_total > 0:
        s.status = PensionStatus.PARTIAL
    db.commit(); db.refresh(p)
    return p

@router.get("/pension/overdue", response_model=List[PensionScheduleOut])
def overdue(db: Session = Depends(get_db), _: User = Depends(current_user)):
    from datetime import date, timedelta
    cutoff = date.today() - timedelta(days=1)
    return db.query(PensionSchedule).filter(
        PensionSchedule.status.in_([PensionStatus.PENDING, PensionStatus.PARTIAL]),
        PensionSchedule.due_date < cutoff
    ).all()