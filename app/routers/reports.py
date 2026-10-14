from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from ..database import get_db
from ..models import Farm, CropCycle, CropInput, MarketSale, Contract, PensionSchedule, PensionPayment, User
from ..deps import current_user

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _: User = Depends(current_user)):
    total_acres = db.query(func.coalesce(func.sum(Farm.total_area_acres), 0)).scalar()
    total_contracts = db.query(func.count(Contract.id)).scalar()
    annual_pension = db.query(
        func.coalesce(func.sum(Contract.rate_per_acre * Contract.area_acres), 0)
    ).scalar()
    collected = db.query(func.coalesce(func.sum(PensionPayment.amount_paid), 0)).scalar()
    return {
        "total_acres": float(total_acres),
        "total_contracts": int(total_contracts),
        "annual_pension_contracted": float(annual_pension),
        "pension_collected": float(collected),
        "pension_outstanding": float(annual_pension - collected),
        "recovery_pct": round(100.0 * float(collected) / float(annual_pension), 2) if annual_pension else 0,
    }

@router.get("/farm/{fid}/kpi")
def farm_kpi(fid: UUID, db: Session = Depends(get_db), _: User = Depends(current_user)):
    farm = db.query(Farm).get(fid)
    cultivated = db.query(func.coalesce(func.sum(CropCycle.area_acres), 0))\
                   .filter(CropCycle.farm_id == fid).scalar()
    input_cost = db.query(func.coalesce(func.sum(CropInput.cost), 0))\
                   .join(CropCycle, CropCycle.id == CropInput.crop_cycle_id)\
                   .filter(CropCycle.farm_id == fid).scalar()
    revenue = db.query(func.coalesce(func.sum(MarketSale.net_amount), 0))\
                .join(CropCycle, CropCycle.id == MarketSale.crop_cycle_id)\
                .filter(CropCycle.farm_id == fid).scalar()
    return {
        "farm_id": str(fid),
        "farm_name": farm.name if farm else None,
        "total_acres": float(farm.total_area_acres) if farm else 0,
        "cultivated_acres": float(cultivated),
        "input_cost": float(input_cost),
        "revenue": float(revenue),
        "cost_per_acre": round(float(input_cost) / float(cultivated), 2) if cultivated else 0,
        "revenue_per_acre": round(float(revenue) / float(cultivated), 2) if cultivated else 0,
    }