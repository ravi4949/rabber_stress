# Convexity & Material Stability Constraints

## Polyconvexity Constraints

To ensure physical stability, frame indifference, and material consistency, strain energy density functions $W$ must satisfy thermodynamic inequality constraints:

1. **Reference Normalization**: $W(\mathbf{I}) = 0$
2. **Stress-Free Reference State**: $\left.\frac{\partial W}{\partial \mathbf{C}}\right|_{\mathbf{C}=\mathbf{I}} = \mathbf{0}$
3. **Monotonicity & Convexity**: $\frac{\partial W}{\partial I_1} \ge 0$, $\frac{\partial W}{\partial I_2} \ge 0$, $\frac{\partial^2 W}{\partial I_1^2} \ge 0$

Input Convex Neural Networks (ICNN) guarantee non-negative weight constraints $W_{ij} \ge 0$ combined with convex activation functions (e.g. Softplus, ELU) to enforce polyconvexity by construction.
