from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from .models import (
    PaymentMode, AdvanceMode, RateSetting, InflationMode,
    SeasonType, PensionStatus, AuditFrequency, ContractStatus,
    UserRole, DisplayUnit
)

class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# AUTH
class LoginIn(BaseModel):
    phone: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"

class UserOut(ORM):
    id: UUID
    full_name: str
    phone: str
    email: Optional[str]
    role: UserRole
    display_unit: DisplayUnit

class UserCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[str] = None
    password: str
    role: UserRole = UserRole.MANAGER
    display_unit: DisplayUnit = DisplayUnit.KILA

# FARM
class FarmIn(BaseModel):
    code: str
    name: str
    village: str
    tehsil: str
    district: str
    total_area_acres: Decimal
    gps_lat: Optional[Decimal] = None
    gps_lng: Optional[Decimal] = None
    water_source: Optional[str] = None
    soil_type: Optional[str] = None
    notes: Optional[str] = None

class FarmOut(ORM, FarmIn):
    id: UUID
    is_active: bool

# FARMER
class FarmerIn(BaseModel):
    code: str
    full_name: str
    father_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    village: Optional[str] = None
    photo_url: Optional[str] = None
    notes: Optional[str] = None

class FarmerOut(ORM, FarmerIn):
    id: UUID
    reliability_score: Decimal
    is_active: bool

# CONTRACT
class ContractIn(BaseModel):
    contract_no: str
    farm_id: UUID
    farmer_id: UUID
    start_date: date
    end_date: date
    area_acres: Decimal
    rate_per_acre: Decimal
    rate_setting: RateSetting = RateSetting.ANNUAL
    advance_mode: AdvanceMode = AdvanceMode.RATE_BASED
    advance_rate_per_acre: Optional[Decimal] = None
    advance_lump_sum: Optional[Decimal] = None
    inflation_mode: InflationMode = InflationMode.COMPOUND
    inflation_rate_pct: Optional[Decimal] = None
    inflation_flat_inc: Optional[Decimal] = None
    audit_frequency: AuditFrequency = AuditFrequency.PER_SEASON
    notes: Optional[str] = None

class ContractOut(ORM):
    id: UUID
    contract_no: str
    farm_id: UUID
    farmer_id: UUID
    status: ContractStatus
    start_date: date
    end_date: date
    area_acres: Decimal
    rate_per_acre: Decimal
    rate_setting: RateSetting
    advance_mode: AdvanceMode
    advance_amount: Decimal
    audit_frequency: AuditFrequency
    notes: Optional[str]

class ContractMath(BaseModel):
    annual_pension: Decimal
    advance: Decimal
    pension_1: Decimal
    pension_2: Decimal
    year_total: Decimal

# ADVANCE
class AdvanceIn(BaseModel):
    amount: Decimal
    received_date: date
    payment_mode: PaymentMode = PaymentMode.CASH
    reference_no: Optional[str] = None
    receipt_url: Optional[str] = None
    notes: Optional[str] = None

class AdvanceOut(ORM, AdvanceIn):
    id: UUID
    contract_id: UUID

# PENSION
class PensionScheduleOut(ORM):
    id: UUID
    contract_id: UUID
    installment_no: int
    due_date: date
    amount_due: Decimal
    status: PensionStatus

class PensionPaymentIn(BaseModel):
    amount_paid: Decimal
    paid_date: date
    payment_mode: PaymentMode = PaymentMode.CASH
    reference_no: Optional[str] = None
    receipt_url: Optional[str] = None
    notes: Optional[str] = None

class PensionPaymentOut(ORM, PensionPaymentIn):
    id: UUID
    schedule_id: UUID

# CROPS
class CropCycleIn(BaseModel):
    farm_id: UUID
    contract_id: UUID
    season: SeasonType
    crop_name: str
    area_acres: Decimal
    sowing_date: Optional[date] = None
    harvest_date: Optional[date] = None
    seed_variety: Optional[str] = None
    expected_yield: Optional[Decimal] = None
    actual_yield: Optional[Decimal] = None
    yield_unit: str = "MAUND"
    notes: Optional[str] = None

class CropCycleOut(ORM, CropCycleIn):
    id: UUID

class CropInputIn(BaseModel):
    input_type: str
    description: Optional[str] = None
    quantity: Optional[Decimal] = None
    unit: Optional[str] = None
    rate: Optional[Decimal] = None
    cost: Decimal
    input_date: date
    paid_by: str = "FARMER"
    receipt_url: Optional[str] = None

class CropInputOut(ORM, CropInputIn):
    id: UUID
    crop_cycle_id: UUID

# MARKET SALES
class MarketSaleIn(BaseModel):
    mandi_name: str
    buyer_name: Optional[str] = None
    arthi_name: Optional[str] = None
    sale_date: date
    quantity: Decimal
    unit: str = "MAUND"
    rate: Decimal
    market_fee: Decimal = Decimal(0)
    commission: Decimal = Decimal(0)
    transport: Decimal = Decimal(0)
    other_deduction: Decimal = Decimal(0)
    slip_photo_url: Optional[str] = None
    notes: Optional[str] = None

class MarketSaleOut(ORM):
    id: UUID
    crop_cycle_id: UUID
    mandi_name: str
    buyer_name: Optional[str]
    sale_date: date
    quantity: Decimal
    rate: Decimal
    gross_amount: Decimal
    net_amount: Decimal

# AUDIT
class FieldAuditIn(BaseModel):
    farm_id: UUID
    contract_id: Optional[UUID] = None
    audit_date: date
    area_verified: Optional[Decimal] = None
    crop_verified: Optional[str] = None
    condition_notes: Optional[str] = None
    photos: Optional[dict] = None
    gps_lat: Optional[Decimal] = None
    gps_lng: Optional[Decimal] = None

class FieldAuditOut(ORM, FieldAuditIn):
    id: UUID

# ALERTS
class AlertOut(ORM):
    id: UUID
    alert_type: str
    severity: str
    message: str
    due_date: Optional[date]
    is_resolved: bool

TokenOut.model_rebuild()