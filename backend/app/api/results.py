"""Report Download Endpoints (GET /analyses/{run_id}/report)."""

import os
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User, AnalysisRun
from app.core.security import get_current_user
from app.services.report_builder import report_builder
from app.core.config import settings

router = APIRouter()

@router.get("/{run_id}/report")
def download_analysis_report(
    run_id: str,
    format: str = Query("pdf", pattern="^(pdf|csv)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Downloads downloadable PDF report or CSV curve export for a completed analysis run.
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

    if run.status != "done":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot generate report for run with status '{run.status}'."
        )

    if format == "pdf":
        file_path = run.report_file_path
        if not file_path or not os.path.exists(file_path):
            file_path = os.path.join(settings.REPORT_DIR, f"{run_id}_report.pdf")
            report_builder.generate_pdf_report(
                run_data={"id": run_id, "deformation_mode": run.deformation_mode, "result": run.result},
                output_path=file_path
            )
        return FileResponse(file_path, media_type="application/pdf", filename=f"RubberStress_{run_id}.pdf")
    else:
        csv_path = os.path.join(settings.REPORT_DIR, f"{run_id}_export.csv")
        report_builder.generate_csv_export(
            run_data={"id": run_id, "result": run.result},
            output_path=csv_path
        )
        return FileResponse(csv_path, media_type="text/csv", filename=f"RubberStress_{run_id}.csv")
