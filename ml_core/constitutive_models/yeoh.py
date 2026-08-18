"""Yeoh 3-Parameter Hyperelastic Model.

Theory reference:
W(I1, J) = C10*(I1 - 3) + C20*(I1 - 3)^2 + C30*(I1 - 3)^3 + (K/2)*(J - 1)^2
"""

import numpy as np

class Yeoh:
    def __init__(self, C10: float = 0.5, C20: float = -0.05, C30: float = 0.01, K: float = 100.0):
        self.C10 = C10
        self.C20 = C20
        self.C30 = C30
        self.K = K

    def strain_energy(self, I1: np.ndarray, J: np.ndarray) -> np.ndarray:
        term = I1 - 3.0
        W = self.C10 * term + self.C20 * (term**2) + self.C30 * (term**3) + (self.K / 2.0) * ((J - 1.0)**2)
        return W

    def first_piola_stress(self, F: np.ndarray) -> np.ndarray:
        J = np.linalg.det(F)
        C = F.T @ F
        I1 = np.trace(C)
        dW_dI1 = self.C10 + 2.0 * self.C20 * (I1 - 3.0) + 3.0 * self.C30 * ((I1 - 3.0)**2)
        FinvT = np.linalg.inv(F).T
        P = 2.0 * dW_dI1 * F + self.K * (J - 1.0) * J * FinvT
        return P
