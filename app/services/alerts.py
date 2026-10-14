from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..models import PensionSchedule, PensionStatus, Alert, Contract, ContractStatus

def generate_alerts(db: Session):
    today = date.today()
    # Pension overdue
    overdue = (db.query(PensionSchedule)
               .filter(PensionSchedule.status.in_([PensionStatus.PENDING, PensionStatus.PARTIAL]),
                       PensionSchedule.due_date < today - timedelta(days=15))
               .all())
    for s in overdue:
        exists = (db.query(Alert)
                  .filter(Alert.contract_id == s.contract_id,
                          Alert.alert_type == "PENSION_OVERDUE",
                          Alert.is_resolved == False)
                  .first())
        if not exists:
            db.add(Alert(
                alert_type="PENSION_OVERDUE",
                contract_id=s.contract_id,
                severity="HIGH",
                message=f"Pension installment {s.installment_no} overdue since {s.due_date}",
                due_date=s.due_date,
            ))
    # Contract expiry
    soon = today + timedelta(days=60)
    expiring = db.query(Contract).filter(
        Contract.status == ContractStatus.ACTIVE,
        Contract.end_date <= soon,
        Contract.end_date >= today,
    ).all()
    for c in expiring:
        exists = (db.query(Alert)
                  .filter(Alert.contract_id == c.id,
                          Alert.alert_type == "CONTRACT_EXPIRING",
                          Alert.is_resolved == False).first())
        if not exists:
            db.add(Alert(
                alert_type="CONTRACT_EXPIRING",
                contract_id=c.id,
                severity="MEDIUM",
                message=f"Contract {c.contract_no} expires on {c.end_date}",
                due_date=c.end_date,
            ))
    db.commit()