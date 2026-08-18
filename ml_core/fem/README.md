# Finite Element Method (FEM) Integration & Lookup Table Validation

This directory contains FEM benchmark validation utilities for checking CANN neural constitutive models.

## Precomputed Lookup Tables (Phase 1)

In Phase 1, stress $\mathbf{P}(\mathbf{F})$ and material tangent stiffness tensors $\mathbb{C} = \frac{\partial^2 W}{\partial \mathbf{F} \partial \mathbf{F}}$ are precomputed from trained PyTorch CANNs into dense multidimensional lookup tables across Gauss points.

### Benchmark Problems Evaluated:
1. **Uniaxial Bar Tension**
2. **Cantilever Beam Bending**
3. **Rubber Block Compression**
4. **Plate with Hole Stress Concentration**

---

# Phase 2 (future work)

Live non-linear PyTorch-FEniCS coupling using custom C++ `ExternalOperator` wrappers or JAX-FEniCS automatic differentiation interfaces for online Gauss-point material evaluation directly within Newton-Raphson solvers.
