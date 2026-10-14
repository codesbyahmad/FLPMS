from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime
from ..database import get_db
from ..models import Alert, User
from ..schemas import AlertOut
from ..deps import current_user
from ..services.alerts import generate_alerts

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("", response_model=List[AlertOut])
def list_alerts(db: Session = Depends(get_db), _: User = Depends(current_user)):
    generate_alerts(db)
    return db.query(Alert).filter(Alert.is_resolved == False)\
             .order_by(Alert.severity.desc(), Alert.created_at.desc()).all()

@router.patch("/{aid}/resolve", response_model=AlertOut)
def resolve(aid: UUID, db: Session = Depends(get_db), _: User = Depends(current_user)):
    a = db.query(Alert).get(aid)
    a.is_resolved = True
    a.resolved_at = datetime.utcnow()
    db.commit(); db.refresh(a)
    return a