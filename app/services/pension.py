from decimal import Decimal
from ..models import Contract, AdvanceMode

TWO = Decimal("2")

def contract_math(area: Decimal, rate: Decimal, advance: Decimal) -> dict:
    annual = (rate * area).quantize(Decimal("0.01"))
    adv = advance.quantize(Decimal("0.01"))
    p1 = ((annual - adv) / TWO).quantize(Decimal("0.01"))
    p2 = ((annual - adv) / TWO).quantize(Decimal("0.01"))
    return {
        "annual_pension": annual,
        "advance": adv,
        "pension_1": p1,
        "pension_2": p2,
        "year_total": (adv + p1 + p2).quantize(Decimal("0.01")),
    }

def compute_advance(mode: AdvanceMode, area: Decimal, rate_per_acre, lump_sum) -> Decimal:
    if mode == AdvanceMode.LUMP_SUM and lump_sum is not None:
        return Decimal(lump_sum).quantize(Decimal("0.01"))
    if rate_per_acre is None:
        return Decimal("0.00")
    return (Decimal(rate_per_acre) * area).quantize(Decimal("0.01"))