"""Pydantic v2 Request and Response Schemas for RubberStress Backend."""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

# --- Material Sample Schemas ---
class MaterialSampleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    notes: Optional[str] = None

class MaterialSampleOut(BaseModel):
    id: int
    user_id: int
    name: str
    notes: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# --- Analysis Schemas ---
class ManualPoint(BaseModel):
    stretch: float = Field(..., ge=1.0, description="Stretch ratio lambda >= 1.0")
    stress: float = Field(..., description="Stress value in MPa")

class AnalysisCreateManual(BaseModel):
    material_sample_id: Optional[int] = None
    deformation_mode: str = "uniaxial"
    points: List[ManualPoint]
    config: Optional[Dict[str, Any]] = None

class AnalysisRunOut(BaseModel):
    id: str
    user_id: int
    material_sample_id: Optional[int]
    status: str
    deformation_mode: str
    input_file_path: str
    config: Optional[Dict[str, Any]]
    result: Optional[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    class Config:
        from_attributes = True

class JobStatusOut(BaseModel):
    id: str
    status: str
    progress_pct: int
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
