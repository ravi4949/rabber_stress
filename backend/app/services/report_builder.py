"""Report Builder Service for assembling downloadable PDF/CSV reports from AnalysisResult."""

import os
from typing import Dict, Any

class ReportBuilder:
    def generate_pdf_report(self, run_data: Dict[str, Any], output_path: str) -> str:
        """
        Generates a summary PDF report for an analysis run.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        run_id = run_data.get("id", "N/A")
        mode = run_data.get("deformation_mode", "uniaxial")
        result = run_data.get("result", {})
        metrics = result.get("metrics", {})
        params = result.get("fitted_params", {})
        warnings = result.get("warnings", [])

        content = f"""RubberStress Analysis Report
==========================================
Run ID: {run_id}
Deformation Mode: {mode}

Identified Parameters:
----------------------
{params}

Validation Metrics:
-------------------
R2 Score:   {metrics.get('r2_score', 'N/A')}
RMSE:       {metrics.get('rmse', 'N/A')} MPa
MAE:        {metrics.get('mae', 'N/A')} MPa

Warnings:
---------
{warnings if warnings else 'None'}
==========================================
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    def generate_csv_export(self, run_data: Dict[str, Any], output_path: str) -> str:
        """Exports predicted stress-strain curves to CSV format."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        result = run_data.get("result", {})
        curves = result.get("predicted_curves", {})
        uniaxial = curves.get("uniaxial", {"stretch": [], "stress": []})

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("stretch,predicted_stress_MPa\n")
            for lamb, p in zip(uniaxial.get("stretch", []), uniaxial.get("stress", [])):
                f.write(f"{lamb:.4f},{p:.4f}\n")

        return output_path

report_builder = ReportBuilder()
