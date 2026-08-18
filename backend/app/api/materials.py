"""History Listing (GET /analyses) & Material Samples Catalog."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models import User, AnalysisRun, MaterialSample
from app.core.security import get_current_user
from app.schemas import AnalysisRunOut, MaterialSampleCreate, MaterialSampleOut

router = APIRouter()

# --- Analysis History ---
@router.get("/analyses", response_model=List[AnalysisRunOut])
def list_user_analyses(
    material_sample_id: Optional[int] = Query(None, description="Filter by material sample ID"),
    uncategorized: Optional[bool] = Query(None, description="Filter uncategorized runs (material_sample_id IS NULL)"),
    deformation_mode: Optional[str] = Query(None, description="Filter by deformation mode"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns a paginated list of past analysis runs for the authenticated user.
    """
    query = db.query(AnalysisRun).filter(AnalysisRun.user_id == current_user.id)
    
    if uncategorized:
        query = query.filter(AnalysisRun.material_sample_id.is_(None))
    elif material_sample_id is not None:
        query = query.filter(AnalysisRun.material_sample_id == material_sample_id)
        
    if deformation_mode is not None and deformation_mode != "" and deformation_mode != "all":
        query = query.filter(AnalysisRun.deformation_mode == deformation_mode)

    runs = query.order_by(AnalysisRun.created_at.desc()).offset(skip).limit(limit).all()
    return runs

# --- Material Samples Catalog ---
@router.post("/materials", response_model=MaterialSampleOut, status_code=status.HTTP_201_CREATED)
def create_material_sample(
    sample_in: MaterialSampleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates a new logical grouping for tracking material test runs over time."""
    sample = MaterialSample(
        user_id=current_user.id,
        name=sample_in.name,
        notes=sample_in.notes
    )
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return sample

@router.get("/materials", response_model=List[MaterialSampleOut])
def list_material_samples(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists all material formulation samples owned by current user."""
    samples = db.query(MaterialSample).filter(MaterialSample.user_id == current_user.id).all()
    return samples
