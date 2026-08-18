"""Unit Tests for ml_core Package Modules."""

import pytest
import numpy as np
import torch
import os

from constitutive_models.neo_hookean import NeoHookean
from preprocessing.invariants import compute_invariants_torch, compute_invariants_numpy
from models.cann_model import CANNModelA
from physics.autodiff import compute_stresses_autodiff
from inference_service import analyze, AnalysisResult
from generate_dataset import generate_dataset_for_model

def test_neo_hookean_analytical():
    model = NeoHookean(mu=1.5, K=100.0)
    F_identity = np.eye(3)
    P_ref = model.first_piola_stress(F_identity)
    np.testing.assert_allclose(P_ref, np.zeros((3, 3)), atol=1e-5)

def test_invariants_identity():
    F = torch.eye(3)
    I1, I2, I3, J = compute_invariants_torch(F)
    assert abs(I1.item() - 3.0) < 1e-5
    assert abs(I2.item() - 3.0) < 1e-5
    assert abs(I3.item() - 1.0) < 1e-5
    assert abs(J.item() - 1.0) < 1e-5

def test_cann_model_reference_state():
    model = CANNModelA()
    ref_input = torch.tensor([[3.0, 3.0, 1.0]], dtype=torch.float32)
    W_ref = model(ref_input)
    assert abs(W_ref.item()) < 1e-4

def test_autodiff_stresses():
    model = CANNModelA()
    F = torch.eye(3)
    stresses = compute_stresses_autodiff(model, F)
    assert "W" in stresses and "P" in stresses and "sigma" in stresses
    assert stresses["P"].shape == (3, 3)

def test_inference_service():
    csv_path = generate_dataset_for_model("neo_hookean", output_dir="data", n_points=20)
    result = analyze(csv_path, deformation_mode="uniaxial")
    assert isinstance(result, AnalysisResult)
    assert "r2_score" in result.metrics
    assert "uniaxial" in result.predicted_curves
