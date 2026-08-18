"""Automatic Differentiation Stress Calculations.

Computes exact hyperelastic stress tensors directly from strain energy density W(F) or W(C):
- First Piola-Kirchhoff stress P = dW/dF
- Second Piola-Kirchhoff stress S = 2 * dW/dC
- Cauchy stress sigma = (1/J) * F @ S @ F^T = (1/J) * P @ F^T
"""

import torch
from preprocessing.invariants import compute_invariants_torch

def compute_stresses_autodiff(model: torch.nn.Module, F: torch.Tensor) -> dict:
    """
    Computes P, S, and sigma from trained CANN strain energy model using torch.autograd.
    
    Args:
        model: PyTorch module taking (batch_size, 3) invariant inputs and outputting (batch_size, 1) energy W.
        F: Deformation gradient tensor of shape (batch_size, 3, 3) or (3, 3).
        
    Returns:
        Dictionary with keys "W", "P", "S", "sigma".
    """
    is_unbatched = (F.dim() == 2)
    if is_unbatched:
        F_batch = F.unsqueeze(0)
    else:
        F_batch = F

    F_batch = F_batch.clone().detach().requires_grad_(True)
    
    # Compute invariants I1, I2, I3, J
    I1, I2, I3, J = compute_invariants_torch(F_batch)
    invariants = torch.stack([I1, I2, J], dim=-1)

    # Forward pass energy W
    W = model(invariants)  # shape (batch_size, 1)

    # 1. First Piola stress P = dW/dF
    grad_outputs = torch.ones_like(W)
    P = torch.autograd.grad(
        outputs=W,
        inputs=F_batch,
        grad_outputs=grad_outputs,
        create_graph=True,
        retain_graph=True
    )[0]

    # 2. Cauchy stress sigma = (1/J) * P @ F^T
    FinvT = torch.linalg.inv(F_batch).transpose(-1, -2)
    J_arr = J.unsqueeze(-1).unsqueeze(-1)
    
    # sigma = (1/J) * P @ F^T
    F_trans = F_batch.transpose(-1, -2)
    sigma = (1.0 / J_arr) * torch.matmul(P, F_trans)

    # 3. Second Piola stress S = F^(-1) @ P
    Finv = torch.linalg.inv(F_batch)
    S = torch.matmul(Finv, P)

    if is_unbatched:
        return {
            "W": W.squeeze(0),
            "P": P.squeeze(0),
            "S": S.squeeze(0),
            "sigma": sigma.squeeze(0)
        }
    return {"W": W, "P": P, "S": S, "sigma": sigma}
