from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routers import (
    auth, farms, farmers, contracts, advances,
    pension, crops, sales, audits, alerts, reports
)

app = FastAPI(title="FLPMS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(farms.router)
app.include_router(farmers.router)
app.include_router(contracts.router)
app.include_router(advances.router)
app.include_router(pension.router)
app.include_router(crops.router)
app.include_router(sales.router)
app.include_router(audits.router)
app.include_router(alerts.router)
app.include_router(reports.router)

@app.get("/health")
def health():
    return {"status": "ok"}