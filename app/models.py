import uuid
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import (
    String, Boolean, Numeric, Date, DateTime, ForeignKey, Enum, Text, SmallInteger
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
import enum

class PaymentMode(str, enum.Enum):
    CASH = "CASH"; BANK = "BANK"; JAZZCASH = "JAZZCASH"
    EASYPAISA = "EASYPAISA"; CHEQUE = "CHEQUE"; OTHER = "OTHER"

class AdvanceMode(str, enum.Enum):
    RATE_BASED = "RATE_BASED"; LUMP_SUM = "LUMP_SUM"

class RateSetting(str, enum.Enum):
    ANNUAL = "ANNUAL"; PER_SEASON = "PER_SEASON"

class InflationMode(str, enum.Enum):
    COMPOUND = "COMPOUND"; FLAT = "FLAT"

class SeasonType(str, enum.Enum):
    RABI = "RABI"; KHARIF = "KHARIF"; ZAID = "ZAID"

class PensionStatus(str, enum.Enum):
    PENDING = "PENDING"; PAID = "PAID"; PARTIAL = "PARTIAL"; OVERDUE = "OVERDUE"; WAIVED = "WAIVED"

class AuditFrequency(str, enum.Enum):
    MONTHLY = "MONTHLY"; QUARTERLY = "QUARTERLY"; PER_SEASON = "PER_SEASON"

class ContractStatus(str, enum.Enum):
    DRAFT = "DRAFT"; ACTIVE = "ACTIVE"; EXPIRED = "EXPIRED"; TERMINATED = "TERMINATED"; RENEWED = "RENEWED"

class UserRole(str, enum.Enum):
    OWNER = "OWNER"; MANAGER = "MANAGER"; ACCOUNTANT = "ACCOUNTANT"
    FIELD_SUPERVISOR = "FIELD_SUPERVISOR"; FARMER = "FARMER"

class DisplayUnit(str, enum.Enum):
    KILA = "KILA"; ACRE = "ACRE"; KANAL = "KANAL"; MARLA = "MARLA"

def _uuid():
    return uuid.uuid4()

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    display_unit: Mapped[DisplayUnit] = mapped_column(Enum(DisplayUnit, name="display_unit"), default=DisplayUnit.KILA)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class Farm(Base):
    __tablename__ = "farms"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    code: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    village: Mapped[str] = mapped_column(String)
    tehsil: Mapped[str] = mapped_column(String)
    district: Mapped[str] = mapped_column(String)
    total_area_acres: Mapped[Decimal] = mapped_column(Numeric(12,4))
    gps_lat: Mapped[Decimal | None] = mapped_column(Numeric(10,7))
    gps_lng: Mapped[Decimal | None] = mapped_column(Numeric(10,7))
    water_source: Mapped[str | None] = mapped_column(String)
    soil_type: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class Farmer(Base):
    __tablename__ = "farmers"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    code: Mapped[str] = mapped_column(String, unique=True)
    full_name: Mapped[str] = mapped_column(String)
    father_name: Mapped[str | None] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String)
    address: Mapped[str | None] = mapped_column(String)
    village: Mapped[str | None] = mapped_column(String)
    photo_url: Mapped[str | None] = mapped_column(String)
    reliability_score: Mapped[Decimal] = mapped_column(Numeric(4,2), default=0)
    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class Contract(Base):
    __tablename__ = "contracts"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    contract_no: Mapped[str] = mapped_column(String, unique=True)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("farms.id"))
    farmer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("farmers.id"))
    status: Mapped[ContractStatus] = mapped_column(Enum(ContractStatus, name="contract_status"), default=ContractStatus.DRAFT)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    area_acres: Mapped[Decimal] = mapped_column(Numeric(12,4))
    rate_per_acre: Mapped[Decimal] = mapped_column(Numeric(14,2))
    rate_setting: Mapped[RateSetting] = mapped_column(Enum(RateSetting, name="rate_setting"), default=RateSetting.ANNUAL)
    advance_mode: Mapped[AdvanceMode] = mapped_column(Enum(AdvanceMode, name="advance_mode"), default=AdvanceMode.RATE_BASED)
    advance_rate_per_acre: Mapped[Decimal | None] = mapped_column(Numeric(14,2))
    advance_lump_sum: Mapped[Decimal | None] = mapped_column(Numeric(14,2))
    advance_amount: Mapped[Decimal] = mapped_column(Numeric(14,2))
    inflation_mode: Mapped[InflationMode] = mapped_column(Enum(InflationMode, name="inflation_mode"), default=InflationMode.COMPOUND)
    inflation_rate_pct: Mapped[Decimal | None] = mapped_column(Numeric(6,3))
    inflation_flat_inc: Mapped[Decimal | None] = mapped_column(Numeric(14,2))
    audit_frequency: Mapped[AuditFrequency] = mapped_column(Enum(AuditFrequency, name="audit_frequency"), default=AuditFrequency.PER_SEASON)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class Advance(Base):
    __tablename__ = "advances"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    contract_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="CASCADE"))
    amount: Mapped[Decimal] = mapped_column(Numeric(14,2))
    received_date: Mapped[date] = mapped_column(Date)
    payment_mode: Mapped[PaymentMode] = mapped_column(Enum(PaymentMode, name="payment_mode"), default=PaymentMode.CASH)
    reference_no: Mapped[str | None] = mapped_column(String)
    receipt_url: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class PensionSchedule(Base):
    __tablename__ = "pension_schedules"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    contract_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="CASCADE"))
    installment_no: Mapped[int] = mapped_column(SmallInteger)
    due_date: Mapped[date] = mapped_column(Date)
    amount_due: Mapped[Decimal] = mapped_column(Numeric(14,2))
    status: Mapped[PensionStatus] = mapped_column(Enum(PensionStatus, name="pension_status"), default=PensionStatus.PENDING)

class PensionPayment(Base):
    __tablename__ = "pension_payments"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    schedule_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pension_schedules.id", ondelete="CASCADE"))
    amount_paid: Mapped[Decimal] = mapped_column(Numeric(14,2))
    paid_date: Mapped[date] = mapped_column(Date)
    payment_mode: Mapped[PaymentMode] = mapped_column(Enum(PaymentMode, name="payment_mode"), default=PaymentMode.CASH)
    reference_no: Mapped[str | None] = mapped_column(String)
    receipt_url: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class CropCycle(Base):
    __tablename__ = "crop_cycles"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("farms.id"))
    contract_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="CASCADE"))
    season: Mapped[SeasonType] = mapped_column(Enum(SeasonType, name="season_type"))
    crop_name: Mapped[str] = mapped_column(String)
    area_acres: Mapped[Decimal] = mapped_column(Numeric(12,4))
    sowing_date: Mapped[date | None] = mapped_column(Date)
    harvest_date: Mapped[date | None] = mapped_column(Date)
    seed_variety: Mapped[str | None] = mapped_column(String)
    expected_yield: Mapped[Decimal | None] = mapped_column(Numeric(14,3))
    actual_yield: Mapped[Decimal | None] = mapped_column(Numeric(14,3))
    yield_unit: Mapped[str] = mapped_column(String, default="MAUND")
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class CropInput(Base):
    __tablename__ = "crop_inputs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    crop_cycle_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("crop_cycles.id", ondelete="CASCADE"))
    input_type: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text)
    quantity: Mapped[Decimal | None] = mapped_column(Numeric(14,3))
    unit: Mapped[str | None] = mapped_column(String)
    rate: Mapped[Decimal | None] = mapped_column(Numeric(14,2))
    cost: Mapped[Decimal] = mapped_column(Numeric(14,2))
    input_date: Mapped[date] = mapped_column(Date)
    paid_by: Mapped[str] = mapped_column(String, default="FARMER")
    receipt_url: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class MarketSale(Base):
    __tablename__ = "market_sales"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    crop_cycle_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("crop_cycles.id", ondelete="CASCADE"))
    mandi_name: Mapped[str] = mapped_column(String)
    buyer_name: Mapped[str | None] = mapped_column(String)
    arthi_name: Mapped[str | None] = mapped_column(String)
    sale_date: Mapped[date] = mapped_column(Date)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14,3))
    unit: Mapped[str] = mapped_column(String, default="MAUND")
    rate: Mapped[Decimal] = mapped_column(Numeric(14,2))
    gross_amount: Mapped[Decimal] = mapped_column(Numeric(14,2))
    market_fee: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    commission: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    transport: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    other_deduction: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    net_amount: Mapped[Decimal] = mapped_column(Numeric(14,2))
    slip_photo_url: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class FieldAudit(Base):
    __tablename__ = "field_audits"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("farms.id"))
    contract_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="SET NULL"))
    audit_date: Mapped[date] = mapped_column(Date)
    area_verified: Mapped[Decimal | None] = mapped_column(Numeric(12,4))
    crop_verified: Mapped[str | None] = mapped_column(String)
    condition_notes: Mapped[str | None] = mapped_column(Text)
    photos: Mapped[dict | None] = mapped_column(JSONB)
    gps_lat: Mapped[Decimal | None] = mapped_column(Numeric(10,7))
    gps_lng: Mapped[Decimal | None] = mapped_column(Numeric(10,7))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    alert_type: Mapped[str] = mapped_column(String)
    farm_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"))
    contract_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="CASCADE"))
    severity: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(Text)
    due_date: Mapped[date | None] = mapped_column(Date)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    entity: Mapped[str] = mapped_column(String)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    action: Mapped[str] = mapped_column(String)
    old_value: Mapped[dict | None] = mapped_column(JSONB)
    new_value: Mapped[dict | None] = mapped_column(JSONB)
    ip_address: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)