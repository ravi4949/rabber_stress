"""Arruda-Boyce 8-Chain Hyperelastic Model.

Theory reference:
W(I1) = mu * sum_{i=1}^5 C_i * (1/N^(i-1)) * (I1^i - 3^i) + (K/2)*(J - 1)^2
where N is the locking parameter (chain segments).
"""

import numpy as np

class ArrudaBoyce:
    def __init__(self, mu: float = 1.0, N: float = 20.0, K: float = 100.0):
        self.mu = mu
        self.N = N
        self.K = K
        # Taylor expansion coefficients for Inverse Langevin function
        self.c = [1/2, 1/(20*N), 11/(1050*N**2), 19/(7000*N**3), 519/(673750*N**4)]

    def strain_energy(self, I1: np.ndarray, J: np.ndarray) -> np.ndarray:
        W_iso = self.mu * (
            self.c[0] * (I1 - 3.0) +
            self.c[1] * (I1**2 - 9.0) +
            self.c[2] * (I1**3 - 27.0) +
            self.c[3] * (I1**4 - 81.0) +
            self.c[4] * (I1**5 - 243.0)
        )
        W_vol = (self.K / 2.0) * ((J - 1.0)**2)
        return W_iso + W_vol

    def first_piola_stress(self, F: np.ndarray) -> np.ndarray:
        J = np.linalg.det(F)
        C = F.T @ F
        I1 = np.trace(C)
        dW_dI1 = self.mu * (
            self.c[0] +
            2.0 * self.c[1] * I1 +
            3.0 * self.c[2] * (I1**2) +
            4.0 * self.c[3] * (I1**3) +
            5.0 * self.c[4] * (I1**4)
        )
        FinvT = np.linalg.inv(F).T
        P = 2.0 * dW_dI1 * F + self.K * (J - 1.0) * J * FinvT
        return P
