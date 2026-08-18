"""Mooney-Rivlin Hyperelastic Constitutive Model.

Theory reference:
Strain energy density function W(I1, I2, J) = C10*(I1 - 3) + C01*(I2 - 3) + (K/2)*(J - 1)^2
where C10 and C01 are material constants (initial shear modulus mu = 2*(C10 + C01)).
"""

import numpy as np

class MooneyRivlin:
    def __init__(self, C10: float = 0.5, C01: float = 0.25, K: float = 100.0):
        """
        Args:
            C10: Material parameter C10 in MPa.
            C01: Material parameter C01 in MPa.
            K: Bulk modulus in MPa.
        """
        self.C10 = C10
        self.C01 = C01
        self.K = K

    def strain_energy(self, I1: np.ndarray, I2: np.ndarray, J: np.ndarray) -> np.ndarray:
        """Computes strain energy density W(I1, I2, J)."""
        W = self.C10 * (I1 - 3.0) + self.C01 * (I2 - 3.0) + (self.K / 2.0) * ((J - 1.0) ** 2)
        return W

    def cauchy_stress(self, F: np.ndarray) -> np.ndarray:
        """Computes Cauchy stress tensor for Mooney-Rivlin model."""
        J = np.linalg.det(F)
        B = F @ F.T if np.isscalar(J) else np.einsum('...ij,...kj->...ik', F, F)
        B2 = B @ B if np.isscalar(J) else np.einsum('...ij,...jk->...ik', B, B)
        I1 = np.trace(B) if np.isscalar(J) else np.trace(B, axis1=-2, axis2=-1)
        I = np.eye(3)
        
        if np.isscalar(J):
            term1 = (2.0 / J) * ((self.C10 + I1 * self.C01) * B - self.C01 * B2)
            p_vol = self.K * (J - 1.0) - (2.0 / (3.0 * J)) * (self.C10 * I1 + 2.0 * self.C01 * np.trace(B2))
            sigma = term1 + p_vol * I
        else:
            J_arr = J[..., np.newaxis, np.newaxis]
            I1_arr = I1[..., np.newaxis, np.newaxis]
            term1 = (2.0 / J_arr) * ((self.C10 + I1_arr * self.C01) * B - self.C01 * B2)
            trB2 = np.trace(B2, axis1=-2, axis2=-1)[..., np.newaxis, np.newaxis]
            p_vol = self.K * (J_arr - 1.0) - (2.0 / (3.0 * J_arr)) * (self.C10 * I1_arr + 2.0 * self.C01 * trB2)
            sigma = term1 + p_vol * I
            
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
