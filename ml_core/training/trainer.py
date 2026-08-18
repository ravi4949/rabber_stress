"""PyTorch Training Engine for Physics-Informed CANN Models.

Includes:
- Adam optimizer
- LR Scheduler
- Early stopping
- Gradient clipping
- Checkpoint management
- Physics-informed autodiff stress loss combined with energy loss
"""

import os
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
from typing import Dict, Any, Tuple

from physics.autodiff import compute_stresses_autodiff

class CANNTrainer:
    def __init__(
        self,
        model: nn.Module,
        lr: float = 1e-3,
        weight_decay: float = 1e-5,
        patience: int = 15,
        grad_clip: float = 1.0,
        checkpoint_dir: str = "checkpoints"
    ):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, mode='min', factor=0.5, patience=5)
        self.patience = patience
        self.grad_clip = grad_clip
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)

    def train_epoch(self, dataloader: DataLoader) -> float:
        self.model.train()
        total_loss = 0.0

        for batch_F, batch_invariants, batch_W, batch_P in dataloader:
            self.optimizer.zero_grad()
            
            # Forward pass energy
            W_pred = self.model(batch_invariants)
            loss_W = nn.functional.mse_loss(W_pred.squeeze(), batch_W)

            # Physics autodiff stress loss
            stresses = compute_stresses_autodiff(self.model, batch_F)
            P_pred = stresses["P"]
            loss_P = nn.functional.mse_loss(P_pred, batch_P)

            loss = loss_W + 0.5 * loss_P

            loss.backward()
            if self.grad_clip > 0:
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_clip)
            self.optimizer.step()

            total_loss += loss.item()

        return total_loss / len(dataloader)

    def fit(
        self,
        train_data: Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor],
        val_data: Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor],
        epochs: int = 100,
        batch_size: int = 32
    ) -> Dict[str, Any]:
        train_dataset = TensorDataset(*train_data)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

        val_F, val_invariants, val_W, val_P = val_data

        best_val_loss = float("inf")
        patience_counter = 0
        history = {"train_loss": [], "val_loss": []}

        for epoch in range(1, epochs + 1):
            train_loss = self.train_epoch(train_loader)
            
            # Validation loss
            self.model.eval()
            with torch.no_grad():
                val_W_pred = self.model(val_invariants)
                val_loss_W = nn.functional.mse_loss(val_W_pred.squeeze(), val_W).item()

            self.scheduler.step(val_loss_W)
            history["train_loss"].append(train_loss)
            history["val_loss"].append(val_loss_W)

            if val_loss_W < best_val_loss:
                best_val_loss = val_loss_W
                patience_counter = 0
                torch.save(self.model.state_dict(), os.path.join(self.checkpoint_dir, "best_cann_model.pt"))
            else:
                patience_counter += 1

            if patience_counter >= self.patience:
                print(f"Early stopping triggered at epoch {epoch}")
                break

        return history
