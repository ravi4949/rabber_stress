"""Input Convex Neural Network (ICNN) Variant for Strict Polyconvexity.

Enforces strain energy convexity W(I1, I2, J) by construction:
- Non-negative weight matrices W^(z) >= 0 for hidden connections.
- Convex, monotonically non-decreasing activation functions (Softplus).
"""

import torch
import torch.nn as nn
from typing import List

class ICNNModel(nn.Module):
    def __init__(self, input_dim: int = 3, hidden_dims: List[int] = [32, 32]):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dims = hidden_dims
        
        # Direct pass-through weights from input to hidden layers
        self.w_x = nn.ModuleList()
        # Non-negative weights connecting hidden layers
        self.w_z = nn.ModuleList()

        prev_z_dim = 0
        for h_dim in hidden_dims:
            self.w_x.append(nn.Linear(input_dim, h_dim))
            if prev_z_dim > 0:
                self.w_z.append(nn.Linear(prev_z_dim, h_dim, bias=False))
            prev_z_dim = h_dim

        self.w_out_x = nn.Linear(input_dim, 1)
        self.w_out_z = nn.Linear(prev_z_dim, 1, bias=False)
        self.act = nn.Softplus()

        self.register_buffer("ref_input", torch.tensor([[3.0, 3.0, 1.0]], dtype=torch.float32))

    def _apply_weight_constraints(self):
        """Clips hidden-to-hidden weights to non-negative values W^(z) >= 0."""
        with torch.no_grad():
            for layer in self.w_z:
                layer.weight.clamp_(min=0.0)
            self.w_out_z.weight.clamp_(min=0.0)

    def forward(self, invariants: torch.Tensor) -> torch.Tensor:
        self._apply_weight_constraints()
        
        z = None
        for i, layer_x in enumerate(self.w_x):
            if i == 0:
                z = self.act(layer_x(invariants))
            else:
                z = self.act(layer_x(invariants) + self.w_z[i - 1](z))

        W_raw = self.w_out_x(invariants) + self.w_out_z(z)

        # Normalize W(I=3, I2=3, J=1) = 0
        z_ref = None
        for i, layer_x in enumerate(self.w_x):
            if i == 0:
                z_ref = self.act(layer_x(self.ref_input))
            else:
                z_ref = self.act(layer_x(self.ref_input) + self.w_z[i - 1](z_ref))
        W_ref = self.w_out_x(self.ref_input) + self.w_out_z(z_ref)

        W_final = nn.functional.softplus(W_raw - W_ref)
        return W_final
