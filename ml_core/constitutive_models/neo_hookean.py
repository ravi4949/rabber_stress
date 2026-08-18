"""Neo-Hookean Hyperelastic Constitutive Model.

Theory reference:
Strain energy density function W(I1, J) = (mu/2)*(I1 - 3 - 2*ln(J)) + (K/2)*(J - 1)^2
where mu is the initial shear modulus and K is the bulk modulus.
"""

import numpy as np
from typing import Tuple, Dict

class NeoHookean:
    def __init__(self, mu: float = 1.5, K: float = 100.0):
        """
        Args:
            mu: Shear modulus in MPa.
            K: Bulk modulus in MPa.
        """
        self.mu = mu
        self.K = K

    def strain_energy(self, I1: np.ndarray, J: np.ndarray) -> np.ndarray:
        """Computes strain energy density W(I1, J)."""
        W = (self.mu / 2.0) * (I1 - 3.0 - 2.0 * np.log(J)) + (self.K / 2.0) * ((J - 1.0) ** 2)
        return W

    def cauchy_stress(self, F: np.ndarray) -> np.ndarray:
        """
        Computes Cauchy stress tensor sigma = (mu/J)*(B - I) + K*(J - 1)*I
        where B = F @ F.T.
        F is expected to have shape (..., 3, 3).
        """
        J = np.linalg.det(F)
        if np.isscalar(J):
            B = F @ F.T
            I = np.eye(3)
            sigma = (self.mu / J) * (B - I) + self.K * (J - 1.0) * I
        else:
            B = np.einsum('...ij,...kj->...ik', F, F)
            I = np.eye(3)
            J_arr = J[..., np.newaxis, np.newaxis]
            sigma = (self.mu / J_arr) * (B - I) + self.K * (J_arr - 1.0) * I
        return sigma

    def first_piola_stress(self, F: np.ndarray) -> np.ndarray:
        """Computes First Piola-Kirchhoff stress P = J * sigma @ F^(-T)."""
        J = np.linalg.det(F)
        sigma = self.cauchy_stress(F)
        if np.isscalar(J):
            FinvT = np.linalg.inv(F).T
            P = J * (sigma @ FinvT)
        else:
            FinvT = np.linalg.inv(F).swapaxes(-1, -2)
            J_arr = J[..., np.newaxis, np.newaxis]
            P = J_arr * np.einsum('...ij,...jk->...ik', sigma, FinvT)
        return P
