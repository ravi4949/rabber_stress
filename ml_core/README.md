# Physics-Informed Constitutive Artificial Neural Network (CANN) Engine (`ml_core`)

`ml_core` is a standalone, research-grade Python package for hyperelastic rubber constitutive modeling using physics-informed neural networks.

## Core Capabilities

1. **Analytical Constitutive Laws**: Neo-Hookean, Mooney-Rivlin, Ogden, Yeoh, and Arruda-Boyce 8-Chain models.
2. **Deformation Modes**: Synthetic data generation and constitutive modeling for Uniaxial tension and Equibiaxial tension deformation modes.
3. **Kinematics & Invariants**: Tensor transformation $F \to C \to (I_1, I_2, I_3, J)$ guaranteeing frame invariance (objectivity) and material isotropy by construction.
4. **Physics-Informed Neural Network (Model A)**: Predicts scalar strain energy density $W(I_1, I_2, J)$ with reference normalization $W(\mathbf{I}) = 0$ and non-negative energy constraints.
5. **Autodiff Stress Engine**: Exact First Piola $\mathbf{P} = \partial W / \partial \mathbf{F}$ and Cauchy stress $\boldsymbol{\sigma} = \frac{1}{J} \mathbf{F} \mathbf{S} \mathbf{F}^T$ derived via `torch.autograd`.
6. **Convexity / Polyconvexity**: Input Convex Neural Network (ICNN) architecture with non-negative weight constraints $W^{(z)} \ge 0$ and Softplus activation functions.
7. **Single Seam Integration**: Exposes `analyze()` and `AnalysisResult` dataclass in `inference_service.py` for web backends.
8. **FEM Lookup-Table Benchmarks**: Precomputed Gauss-point validation suite across 4 benchmark problems (Uniaxial bar, Cantilever beam, Block compression, Plate with hole).

---

## Running the Pipeline & Tests

### Execute End-to-End Pipeline
```bash
python ml_core/main.py
```

### Run Unit Test Suite
```bash
pytest ml_core/tests
```

---

## Limitations & Future Work

1. **Anisotropic Materials**: Current invariants $(I_1, I_2, I_3)$ assume isotropic response. Fiber-reinforced composites require structural tensor invariants $I_4 = \mathbf{a}_0 \cdot \mathbf{C} \mathbf{a}_0$ and $I_5$.
2. **Viscoelasticity (vCANN)**: Time-dependent history effects (Mullins effect, rate-dependence) can be integrated using internal variable dynamics or recurrent state transitions.
3. **Live FEM Coupling**: Phase 2 integration will extend `fem/` to support live non-linear PyTorch-FEniCS Newton-Raphson solvers via custom C++ `ExternalOperator` bindings.
