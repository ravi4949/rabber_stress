# Continuum Mechanics & Hyperelasticity

## Kinematics of Deformation

Let $\mathbf{X}$ denote a point in the reference configuration $\Omega_0$ and $\mathbf{x} = \boldsymbol{\chi}(\mathbf{X})$ the corresponding point in the current configuration $\Omega$. The deformation gradient tensor $\mathbf{F}$ is defined as:

$$\mathbf{F} = \frac{\partial \mathbf{x}}{\partial \mathbf{X}} = \nabla_{\mathbf{X}} \boldsymbol{\chi}$$

The Jacobian $J$ represents volumetric change:
$$J = \det \mathbf{F} > 0$$

The Right Cauchy-Green deformation tensor $\mathbf{C}$ is given by:
$$\mathbf{C} = \mathbf{F}^T \mathbf{F}$$

## Strain Energy Density Function $W(\mathbf{C})$

For hyperelastic materials, there exists a scalar strain energy density function $W = W(\mathbf{C})$ such that the second Piola-Kirchhoff stress tensor $\mathbf{S}$ and Cauchy stress tensor $\boldsymbol{\sigma}$ are obtained via:

$$\mathbf{S} = 2 \frac{\partial W}{\partial \mathbf{C}}$$
$$\boldsymbol{\sigma} = \frac{1}{J} \mathbf{F} \mathbf{S} \mathbf{F}^T = \frac{2}{J} \mathbf{F} \frac{\partial W}{\partial \mathbf{C}} \mathbf{F}^T$$
