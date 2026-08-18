"""Publication-Quality Figure Generation for CANN Constitutive Models.

Generates:
- Stress-strain curves per deformation mode
- Strain energy density W(I1) curves
- Predicted vs Analytical stress scatter plots
- Loss history trajectories
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List

plt.style.use('ggplot')

def plot_stress_strain_curves(
    stretches: np.ndarray,
    analytical_stress: np.ndarray,
    predicted_stress: np.ndarray,
    mode: str = "Uniaxial Tension",
    save_path: str = "visualization/stress_strain_curve.png"
):
    """Plots analytical vs predicted stress-strain curve for a deformation mode."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(stretches, analytical_stress, 'k-', label='Analytical Ground Truth', linewidth=2)
    ax.plot(stretches, predicted_stress, 'r--', label='CANN Prediction', linewidth=2)
    
    ax.set_xlabel(r'Stretch $\lambda$', fontsize=12)
    ax.set_ylabel('Nominal Stress $P_{11}$ (MPa)', fontsize=12)
    ax.set_title(f'Hyperelastic Response ({mode})', fontsize=14)
    ax.legend(frameon=True)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    fig.tight_layout()
    fig.savefig(save_path, dpi=300)
    plt.close(fig)
    return save_path

def plot_loss_history(
    history: Dict[str, List[float]],
    save_path: str = "visualization/loss_history.png"
):
    """Plots training and validation loss curves over epochs."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(7, 5))
    epochs = range(1, len(history["train_loss"]) + 1)
    
    ax.plot(epochs, history["train_loss"], 'b-', label='Training Loss')
    ax.plot(epochs, history["val_loss"], 'g--', label='Validation Loss')
    
    ax.set_yscale('log')
    ax.set_xlabel('Epochs', fontsize=12)
    ax.set_ylabel('MSE Loss (Log Scale)', fontsize=12)
    ax.set_title('CANN Training Loss Trajectory', fontsize=14)
    ax.legend(frameon=True)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    fig.tight_layout()
    fig.savefig(save_path, dpi=300)
    plt.close(fig)
    return save_path
