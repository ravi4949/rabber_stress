"""FastAPI Application Main Entrypoint for RubberStress Backend."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, uploads, jobs, results, materials
from app.core.config import settings
from app.db.session import engine, Base
import app.models  # load ORM models

# Auto-create tables for local execution
Base.metadata.create_all(bind=engine)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("rubber_stress.api")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FastAPI Backend for CANN hyperelastic material characterization.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router Registrations
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(uploads.router, prefix=f"{settings.API_V1_STR}/analyses", tags=["analyses"])
app.include_router(jobs.router, prefix=f"{settings.API_V1_STR}/jobs", tags=["jobs"])
app.include_router(results.router, prefix=f"{settings.API_V1_STR}/analyses", tags=["results"])
app.include_router(materials.router, prefix=f"{settings.API_V1_STR}", tags=["materials"])

@app.get("/", tags=["root"])
def read_root():
    return {
        "message": "RubberStress API is running.",
        "docs_url": "/docs",
        "health_check": "/health"
    }

@app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

