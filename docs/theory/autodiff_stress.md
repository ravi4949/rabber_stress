# Mathematical Derivations of Automatic Differentiation for Stress Tensors

## 1. Strain Energy Density $W(\mathbf{F})$

In hyperelastic continuum mechanics, the strain energy density per unit reference volume is represented by a scalar potential function $W(\mathbf{F})$.

## 2. First Piola-Kirchhoff Stress Tensor $\mathbf{P}$

The First Piola-Kirchhoff stress tensor $\mathbf{P}$ measures force in the current configuration per unit reference area:

$$\mathbf{P} = \frac{\partial W}{\partial \mathbf{F}}$$

In PyTorch, for a scalar strain energy output $W$, this tensor is computed directly via reverse-mode automatic differentiation:
```python
P = torch.autograd.grad(outputs=W, inputs=F, grad_outputs=torch.ones_like(W))[0]
```

## 3. Second Piola-Kirchhoff Stress Tensor $\mathbf{S}$

The Second Piola-Kirchhoff stress tensor $\mathbf{S}$ is symmetric and operates entirely in the reference configuration:

$$\mathbf{S} = 2 \frac{\partial W}{\partial \mathbf{C}} = \mathbf{F}^{-1} \mathbf{P}$$

## 4. Cauchy Stress Tensor $\boldsymbol{\sigma}$

The Cauchy stress tensor $\boldsymbol{\sigma}$ (true stress) in the current deformed configuration is obtained via push-forward transformation:

$$\boldsymbol{\sigma} = \frac{1}{J} \mathbf{F} \mathbf{S} \mathbf{F}^T = \frac{1}{J} \mathbf{P} \mathbf{F}^T$$

where $J = \det \mathbf{F} > 0$ is the volume ratio.
