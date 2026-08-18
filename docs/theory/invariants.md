# Mathematical Justification for Invariant-Based Input Representations

## 1. Frame Invariance (Principle of Material Frame Indifference)

In continuum mechanics, physical laws must be invariant under rigid body rotations of the current configuration (Objectivity).

For any proper orthogonal transformation tensor $\mathbf{Q} \in S O(3)$ (where $\mathbf{Q}^T \mathbf{Q} = \mathbf{I}$ and $\det \mathbf{Q} = 1$), the transformed deformation gradient is:

$$\mathbf{F}^* = \mathbf{Q} \mathbf{F}$$

If raw deformation gradient $\mathbf{F}$ is supplied as neural network input, the network $W(\mathbf{F})$ will generally fail objectivity unless forced via explicit data augmentation or loss penalties:

$$W(\mathbf{Q}\mathbf{F}) \neq W(\mathbf{F}) \quad \text{(Violation of Objectivity)}$$

By constructing the Right Cauchy-Green deformation tensor $\mathbf{C} = \mathbf{F}^T \mathbf{F}$:

$$\mathbf{C}^* = (\mathbf{F}^*)^T \mathbf{F}^* = (\mathbf{Q}\mathbf{F})^T (\mathbf{Q}\mathbf{F}) = \mathbf{F}^T \mathbf{Q}^T \mathbf{Q} \mathbf{F} = \mathbf{F}^T \mathbf{F} = \mathbf{C}$$

Thus, $\mathbf{C}$ and its invariants are **strictly frame-indifferent by construction**.

## 2. Material Isotropy

For isotropic materials, strain energy density $W$ must also be invariant under rigid body rotations of the reference configuration:

$$W(\mathbf{F} \mathbf{Q}_0) = W(\mathbf{F}) \quad \forall \mathbf{Q}_0 \in S O(3)$$

The representation theorem of isotropic tensor functions proves that a scalar function $W(\mathbf{C})$ is isotropic if and only if it depends exclusively on the principal scalar invariants of $\mathbf{C}$:

$$W(\mathbf{C}) = \hat{W}(I_1, I_2, I_3)$$

where:
$$I_1 = \mathrm{tr}(\mathbf{C})$$
$$I_2 = \frac{1}{2}\left( (\mathrm{tr} \mathbf{C})^2 - \mathrm{tr}(\mathbf{C}^2) \right)$$
$$I_3 = \det(\mathbf{C}) = J^2$$

## 3. Dimensionality Reduction & Lossless Representation

Feeding raw $\mathbf{F} \in \mathbb{R}^{3 \times 3}$ requires 9 inputs, 6 of which represent rigid rotations and shear orientations. Using invariants $(I_1, I_2, J)$ reduces the input space to 3 physically meaningful scalar invariants, eliminating non-physical degree-of-freedom redundancies and accelerating training convergence.
