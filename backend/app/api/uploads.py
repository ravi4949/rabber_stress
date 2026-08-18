"""Analysis Upload & Submission Endpoint (POST /analyses)."""

import os
import uuid
import json
import pandas as pd
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Body
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User, AnalysisRun, MaterialSample
from app.core.security import get_current_user
from app.core.config import settings
from app.services.file_validation import validate_and_parse_csv
from app.schemas import AnalysisCreateManual

router = APIRouter()

@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def submit_analysis(
    file: Optional[UploadFile] = File(None),
    material_sample_id: Optional[int] = Form(None),
    deformation_mode: str = Form("uniaxial"),
    manual_data_json: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submits raw stress-strain test data via CSV upload OR manual points JSON.
    Validates CSV schema and enqueues background Celery job.
    """
    if file is None and manual_data_json is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Exactly one of 'file' (CSV upload) or 'manual_data_json' must be provided."
        )

    if file is not None and manual_data_json is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Provide either 'file' or 'manual_data_json', not both."
        )

    run_id = str(uuid.uuid4())
    saved_file_path = os.path.join(settings.UPLOAD_DIR, f"{run_id}.csv")

    if file is not None:
        contents = await file.read()
        with open(saved_file_path, "wb") as f:
            f.write(contents)

        # Validate CSV file format
        is_valid, err_msg, _ = validate_and_parse_csv(saved_file_path)
        if not is_valid:
            os.remove(saved_file_path)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=err_msg
            )
    else:
        # Parse manual JSON data points
        try:
            points = json.loads(manual_data_json)
            df = pd.DataFrame(points)
            if "stretch" not in df.columns or "stress" not in df.columns:
                raise ValueError("Manual points must contain 'stretch' and 'stress' keys.")
            df.to_csv(saved_file_path, index=False)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid manual data JSON format: {str(e)}"
            )

    # Validate material_sample_id ownership if provided
    if material_sample_id is not None:
        sample = db.query(MaterialSample).filter(
            MaterialSample.id == material_sample_id,
            MaterialSample.user_id == current_user.id
        ).first()
        if not sample:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Material sample not found or access denied."
            )

    # Create AnalysisRun row
    analysis_run = AnalysisRun(
        id=run_id,
        user_id=current_user.id,
        material_sample_id=material_sample_id,
        status="queued",
        input_file_path=saved_file_path,
        deformation_mode=deformation_mode
    )
    db.add(analysis_run)
    db.commit()
    db.refresh(analysis_run)

    # Enqueue background Celery job
    try:
        from app.tasks.run_analysis import run_analysis
        run_analysis.delay(run_id)
    except Exception as e:
        # Fallback synchronous execution if Celery/Redis is offline in dev
        from app.services.ml_bridge import analyze
        res = analyze(saved_file_path, deformation_mode)
        analysis_run.result = {
            "fitted_params": res.fitted_params,
            "predicted_curves": res.predicted_curves,
            "metrics": res.metrics,
            "warnings": res.warnings
        }
        analysis_run.status = "done"
        db.commit()

    return {
        "run_id": run_id,
        "status": analysis_run.status,
        "message": "Analysis job queued successfully."
    }
