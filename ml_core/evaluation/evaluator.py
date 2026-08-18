"""Model Evaluation Engine for Hyperelastic Models & Baselines.

Computes:
- Regression metrics: MSE, RMSE, MAE, Relative Error, R2
- Energy prediction vs Stress prediction breakdown
- Out-of-distribution generalization testing across deformation paths
"""

import numpy as np
import torch
from typing import Dict, Any

from physics.autodiff import compute_stresses_autodiff

def compute_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculates regression metrics MSE, RMSE, MAE, Relative Error, R2."""
    mse = float(np.mean((y_true - y_pred) ** 2))
    rmse = float(np.sqrt(mse))
    mae = float(np.mean(np.abs(y_true - y_pred)))
    
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    ss_res = float(np.sum((y_true - y_pred) ** 2))
    r2 = 1.0 - (ss_res / (ss_tot + 1e-8))
    
    rel_error = float(np.mean(np.abs(y_true - y_pred) / (np.abs(y_true) + 1e-6)))

    return {
        "mse": mse,
        "rmse": rmse,
        "mae": mae,
        "rel_error": rel_error,
        "r2_score": max(r2, -1.0)
    }

def evaluate_cann_model(model: torch.nn.Module, F_test: torch.Tensor, W_test: torch.Tensor, P_test: torch.Tensor) -> Dict[str, Any]:
    """Evaluates CANN Model A predictions against ground truth strain energy W and First Piola stress P."""
    model.eval()
    
    # Invariant computation for input
    from preprocessing.invariants import compute_invariants_torch
    I1, I2, I3, J = compute_invariants_torch(F_test)
    invariants = torch.stack([I1, I2, J], dim=-1)

    # Predicted energy W
    with torch.no_grad():
        W_pred = model(invariants).squeeze().cpu().numpy()
    W_true = W_test.cpu().numpy()

    energy_metrics = compute_regression_metrics(W_true, W_pred)

    # Predicted stress P via autodiff
    stresses = compute_stresses_autodiff(model, F_test)
    P_pred = stresses["P"].detach().cpu().numpy()
    P_true = P_test.cpu().numpy()

    stress_metrics = compute_regression_metrics(P_true.flatten(), P_pred.flatten())

    return {
        "energy_metrics": energy_metrics,
        "stress_metrics": stress_metrics,
        "overall_r2": (energy_metrics["r2_score"] + stress_metrics["r2_score"]) / 2.0
    }
