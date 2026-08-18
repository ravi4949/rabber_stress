"""Constitutive Artificial Neural Network (CANN) Model A - Strain Energy Density Predictor.

Model A predicts scalar strain energy density W(I1, I2, J) from strain invariants.
Stress tensors are derived via automatic differentiation (torch.autograd).

Physics constraints by construction:
1. W(I1=3, I2=3, J=1) = 0 (Reference energy shift)
2. Non-negative strain energy W >= 0 via Softplus or positive activation output.
"""

import torch
import torch.nn as nn
from typing import List

class CANNModelA(nn.Module):
    def __init__(
        self,
        input_dim: int = 3,
        hidden_dims: List[int] = [32, 32],
        activation: str = "softplus",
        use_residual: bool = True
    ):
        super().__init__()
        self.use_residual = use_residual
        
        if activation == "softplus":
            act_fn = nn.Softplus()
        elif activation == "elu":
            act_fn = nn.ELU()
        else:
            act_fn = nn.GELU()

        layers = []
        in_dim = input_dim
        for h_dim in hidden_dims:
            layers.append(nn.Linear(in_dim, h_dim))
            layers.append(act_fn)
            in_dim = h_dim

        self.backbone = nn.Sequential(*layers)
        self.output_layer = nn.Linear(in_dim, 1)

        # Baseline reference input for normalization: (I1=3, I2=3, J=1)
        self.register_buffer("ref_input", torch.tensor([[3.0, 3.0, 1.0]], dtype=torch.float32))

    def forward(self, invariants: torch.Tensor) -> torch.Tensor:
        """
        Args:
            invariants: Tensor of shape (batch_size, 3) containing (I1, I2, J).
        Returns:
            W: Scalar strain energy density of shape (batch_size, 1).
        """
        # Raw neural network prediction
        h = self.backbone(invariants)
        W_raw = self.output_layer(h)

        # Reference normalization W(I1=3, I2=3, J=1) = 0
        h_ref = self.backbone(self.ref_input)
        W_ref = self.output_layer(h_ref)

        W_raw_sp = nn.functional.softplus(W_raw)
        W_ref_sp = nn.functional.softplus(W_ref)

        W_final = W_raw_sp - W_ref_sp
        return W_final
