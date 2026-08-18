"""Preprocessing module for deformation kinematics and strain invariants.

Computes:
- Right Cauchy-Green deformation tensor C = F^T @ F
- Principal invariants:
  I1 = tr(C)
  I2 = 0.5 * ( (tr C)^2 - tr(C^2) )
  I3 = det(C) = J^2
  J = sqrt(I3) = det(F)

Supports both PyTorch tensors (for autograd tracking) and NumPy arrays.
"""

import torch
import numpy as np
from typing import Tuple, Union

def compute_invariants_torch(F: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Computes invariants (I1, I2, I3, J) for PyTorch deformation gradient tensor F.
    F shape: (batch_size, 3, 3) or (3, 3).
    """
    if F.dim() == 2:
        F_batch = F.unsqueeze(0)
    else:
        F_batch = F

    C = torch.matmul(F_batch.transpose(-1, -2), F_batch)
    
    # I1 = tr(C)
    I1 = torch.diagonal(C, dim1=-2, dim2=-1).sum(-1)
    
    # C^2
    C2 = torch.matmul(C, C)
    tr_C2 = torch.diagonal(C2, dim1=-2, dim2=-1).sum(-1)
    
    # I2 = 0.5 * (I1^2 - tr(C^2))
    I2 = 0.5 * (I1**2 - tr_C2)
    
    # I3 = det(C)
    I3 = torch.linalg.det(C)
    
    # J = sqrt(I3) = det(F)
    J = torch.sqrt(torch.clamp(I3, min=1e-8))

    if F.dim() == 2:
        return I1.squeeze(0), I2.squeeze(0), I3.squeeze(0), J.squeeze(0)
    return I1, I2, I3, J

def compute_invariants_numpy(F: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Computes invariants (I1, I2, I3, J) for NumPy array F."""
    if F.ndim == 2:
        C = F.T @ F
        I1 = np.trace(C)
        I2 = 0.5 * (I1**2 - np.trace(C @ C))
        I3 = np.linalg.det(C)
        J = np.sqrt(np.maximum(I3, 1e-8))
        return I1, I2, I3, J
    else:
        C = np.einsum('...ji,...jk->...ik', F, F)
        I1 = np.trace(C, axis1=-2, axis2=-1)
        C2 = np.einsum('...ij,...jk->...ik', C, C)
        tr_C2 = np.trace(C2, axis1=-2, axis2=-1)
        I2 = 0.5 * (I1**2 - tr_C2)
        I3 = np.linalg.det(C)
        J = np.sqrt(np.maximum(I3, 1e-8))
        return I1, I2, I3, J
