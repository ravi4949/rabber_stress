"""Ablation Baseline Models (Model B & Model C).

For comparative evaluation:
- Model B: Predicts Cauchy stress tensor sigma directly (9 outputs, no strain energy scalar, no autodiff).
- Model C: Predicts First Piola-Kirchhoff stress tensor P directly (9 outputs, no strain energy scalar, no autodiff).
"""

import torch
import torch.nn as nn

class ModelB_DirectCauchyStress(nn.Module):
    """Ablation baseline predicting 3x3 Cauchy stress tensor directly."""
    def __init__(self, input_dim: int = 3, hidden_dims: list = [32, 32]):
        super().__init__()
        layers = []
        in_d = input_dim
        for h in hidden_dims:
            layers.append(nn.Linear(in_d, h))
            layers.append(nn.ReLU())
            in_d = h
        layers.append(nn.Linear(in_d, 9))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.net(x)
        return out.view(-1, 3, 3)

class ModelC_DirectFirstPiolaStress(nn.Module):
    """Ablation baseline predicting 3x3 First Piola stress tensor directly."""
    def __init__(self, input_dim: int = 3, hidden_dims: list = [32, 32]):
        super().__init__()
        layers = []
        in_d = input_dim
        for h in hidden_dims:
            layers.append(nn.Linear(in_d, h))
            layers.append(nn.ReLU())
            in_d = h
        layers.append(nn.Linear(in_d, 9))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.net(x)
        return out.view(-1, 3, 3)
