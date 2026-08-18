"""Celery Background Task for Long-Running Analysis Jobs."""

import os
import traceback
from datetime import datetime
import logging

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.models import AnalysisRun
from app.services.file_validation import validate_and_parse_csv
from app.services.ml_bridge import analyze
from app.services.report_builder import report_builder
from app.core.config import settings

logger = logging.getLogger("rubber_stress.tasks")

@celery_app.task(bind=True, name="tasks.run_analysis")
def run_analysis(self, run_id: str):
    """
    Asynchronous Celery task for running hyperelastic CANN model optimization.
    """
    db = SessionLocal()
    try:
        # 1. Load AnalysisRun row
        run = db.query(AnalysisRun).filter(AnalysisRun.id == run_id).first()
        if not run:
            logger.error(f"[run_id={run_id}] AnalysisRun row not found.")
            return

        run.status = "running"
        db.commit()
        logger.info(f"[run_id={run_id}, user_id={run.user_id}] Marked job as running.")

        # 2. Re-validate file (defense in depth)
        is_valid, err_msg, parsed_data = validate_and_parse_csv(run.input_file_path)
        if not is_valid:
            run.status = "failed"
            run.error_message = f"Defense-in-depth file validation failed: {err_msg}"
            run.completed_at = datetime.utcnow()
            db.commit()
            logger.warning(f"[run_id={run_id}] Job failed file validation: {err_msg}")
            return

        # 3. Call ml_bridge.analyze
        res = analyze(
            raw_data_path=run.input_file_path,
            deformation_mode=run.deformation_mode,
            config=run.config
        )

        # 4. On success: store result JSON, build report, mark status=done
        result_dict = {
            "fitted_params": res.fitted_params,
            "predicted_curves": res.predicted_curves,
            "metrics": res.metrics,
            "warnings": res.warnings
        }

        report_path = os.path.join(settings.REPORT_DIR, f"{run_id}_report.pdf")
        report_builder.generate_pdf_report(
            run_data={"id": run_id, "deformation_mode": run.deformation_mode, "result": result_dict},
            output_path=report_path
        )

        run.result = result_dict
        run.report_file_path = report_path
        run.status = "done"
        run.completed_at = datetime.utcnow()
        db.commit()
        logger.info(f"[run_id={run_id}] Job completed successfully.")

    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"[run_id={run_id}] Task encountered error: {str(e)}\n{tb}")
        db.rollback()
        run = db.query(AnalysisRun).filter(AnalysisRun.id == run_id).first()
        if run:
            run.status = "failed"
            run.error_message = f"Processing error: {str(e)}"
            run.completed_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()
