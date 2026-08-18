"""CSV Schema & Unit Validation Service for Experimental Rubber Test Data."""

import pandas as pd
from typing import Tuple, Dict, Any, List

def validate_and_parse_csv(file_path_or_buffer) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validates CSV file against required column schema and value constraints.
    
    Returns:
        (is_valid: bool, error_message: str, parsed_data: dict)
    """
    try:
        df = pd.read_csv(file_path_or_buffer)
    except Exception as e:
        return False, f"Failed to parse CSV file format: {str(e)}", {}

    if df.empty:
        return False, "Uploaded CSV file is completely empty.", {}

    cols_lower = [str(c).strip().lower() for c in df.columns]

    # Map acceptable column variations
    stretch_col = None
    stress_col = None

    for idx, c in enumerate(cols_lower):
        if c in ["stretch", "stretch_ratio", "lambda", "lmbda"]:
            stretch_col = df.columns[idx]
        elif c in ["stress", "stress_mpa", "nominal_stress", "cauchy_stress", "p11", "sigma11"]:
            stress_col = df.columns[idx]

    missing = []
    if not stretch_col:
        missing.append("stretch (or 'stretch_ratio', 'lambda')")
    if not stress_col:
        missing.append("stress (or 'stress_MPa', 'nominal_stress')")

    if missing:
        actual_cols = list(df.columns)
        return (
            False,
            f"CSV file is missing required columns: {', '.join(missing)}; got columns: {actual_cols}",
            {}
        )

    # Check numeric types
    try:
        df[stretch_col] = pd.to_numeric(df[stretch_col])
        df[stress_col] = pd.to_numeric(df[stress_col])
    except ValueError:
        return False, "CSV contains non-numeric values in stretch or stress columns.", {}

    # Check for NaN / Inf
    if df[stretch_col].isnull().any() or df[stress_col].isnull().any():
        return False, "CSV contains null or NaN values in stretch/stress data rows.", {}

    # Range checks: Stretch lambda >= 1.0 (or close to 1.0 for small compression)
    min_stretch = float(df[stretch_col].min())
    if min_stretch < 0.5:
        return (
            False,
            f"Invalid stretch ratio detected (minimum stretch = {min_stretch:.3f}). Stretch must be >= 0.5.",
            {}
        )

    return True, "CSV validation successful.", {
        "stretch": df[stretch_col].tolist(),
        "stress": df[stress_col].tolist(),
        "n_points": len(df)
    }
