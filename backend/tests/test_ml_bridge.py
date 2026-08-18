"""Unit Tests for ml_bridge Integration."""

import os
from app.services.ml_bridge import analyze

def test_ml_bridge_stub_and_real_fallback(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("stretch,stress\n1.0,0.0\n2.0,3.0\n3.0,7.0\n")

    res = analyze(str(csv_file), deformation_mode="uniaxial")
    assert res is not None
    assert "r2_score" in res.metrics
    assert "uniaxial" in res.predicted_curves
