"""Jobs Status Polling & Tagging Endpoint (GET/PATCH /analyses/{run_id})."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.db.session import get_db
from app.models import User, AnalysisRun
from app.core.security import get_current_user
from app.schemas import AnalysisRunOut

router = APIRouter()

class AnalysisRunUpdate(BaseModel):
    material_sample_id: Optional[int] = None

@router.get("/{run_id}", response_model=AnalysisRunOut)
def get_analysis_status(
    run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Polls the status of an analysis job by ID.
    Returns 404 if the job does not exist or does not belong to current user.
    """
    run = db.query(AnalysisRun).filter(
        AnalysisRun.id == run_id,
        AnalysisRun.user_id == current_user.id
    ).first()

    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis run not found."
        )

    return run

@router.patch("/{run_id}", response_model=AnalysisRunOut)
def update_analysis_run(
    run_id: str,
    update_in: AnalysisRunUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates the material_sample_id tag of an existing analysis run in history.
    """
    run = db.query(AnalysisRun).filter(
        AnalysisRun.id == run_id,
        AnalysisRun.user_id == current_user.id
    ).first()

    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis run not found."
        )

    run.material_sample_id = update_in.material_sample_id
    db.commit()
    db.refresh(run)
    return run
