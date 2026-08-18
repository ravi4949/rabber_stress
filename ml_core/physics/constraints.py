"""Physics Constraint Verification Utilities."""

import torch
from physics.autodiff import compute_stresses_autodiff

def verify_reference_state_constraints(model: torch.nn.Module) -> dict:
    """Verifies W(F=I) = 0 and P(F=I) = 0 reference state conditions."""
    I = torch.eye(3, dtype=torch.float32)
    stresses = compute_stresses_autodiff(model, I)
    
    W_ref = float(stresses["W"].detach().numpy())
    P_ref_norm = float(torch.norm(stresses["P"]).detach().numpy())
    
    return {
        "W_ref": W_ref,
        "P_ref_norm": P_ref_norm,
        "W_ref_pass": abs(W_ref) < 1e-4,
        "P_ref_pass": P_ref_norm < 1e-3
    }
