from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import FieldAudit, User
from ..schemas import FieldAuditIn, FieldAuditOut
from ..deps import current_user

router = APIRouter(prefix="/audits", tags=["audits"])

@router.get("", response_model=List[FieldAuditOut])
def list_audits(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(FieldAudit).order_by(FieldAudit.audit_date.desc()).all()

@router.post("", response_model=FieldAuditOut)
def create_audit(payload: FieldAuditIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    a = FieldAudit(**payload.model_dump())
    db.add(a); db.commit(); db.refresh(a)
    return a