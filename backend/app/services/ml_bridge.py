"""Integration Seam Bridge to ml_core.inference_service.

This is the SINGLE file in the backend codebase that imports `ml_core`.
If `ml_core` is unavailable, it uses a stub implementation returning an AnalysisResult matching structure.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import sys
import os
import logging

logger = logging.getLogger(__name__)

# Ensure ml_core is in sys.path
ml_core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml_core"))
if ml_core_path not in sys.path:
    sys.path.insert(0, ml_core_path)

try:
    from inference_service import analyze as real_analyze, AnalysisResult
    HAS_ML_CORE = True
except ImportError:
    HAS_ML_CORE = False

    @dataclass
    class AnalysisResult:
        fitted_params: Dict[str, Any]
        predicted_curves: Dict[str, Dict[str, List[float]]]
        metrics: Dict[str, float]
        warnings: List[str] = field(default_factory=list)

def analyze(
    raw_data_path: str,
    deformation_mode: str = "uniaxial",
    config: Optional[Dict[str, Any]] = None
) -> AnalysisResult:
    """
    Bridge function calling ml_core.inference_service.analyze.
    """
    if HAS_ML_CORE:
        logger.info(f"Invoking real ml_core.inference_service.analyze on {raw_data_path}")
        return real_analyze(raw_data_path=raw_data_path, deformation_mode=deformation_mode, config=config)
    else:
        # TODO: replace with real ml_core.inference_service.analyze
        logger.warning(f"ml_core not detected in path. Using stub analyze fallback for {raw_data_path}")
        
        stretches = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
        stresses = [0.0, 1.25, 2.85, 4.90, 7.55, 10.80, 14.90]

        predicted_curves = {
            "uniaxial": {"stretch": stretches, "stress": stresses},
            "biaxial": {"stretch": stretches, "stress": [0.0, 1.8, 4.2, 7.5, 12.1, 18.0, 25.4]}
        }

        return AnalysisResult(
            fitted_params={"C10": 0.742, "C01": 0.158, "mu_effective": 1.80},
            predicted_curves=predicted_curves,
            metrics={"r2_score": 0.998, "rmse": 0.042, "mae": 0.031},
            warnings=["Fallback stub implementation utilized; ml_core import pending."]
        )
