"""Ogden Hyperelastic Constitutive Model.

Theory reference:
W(lambda1, lambda2, lambda3) = sum_i (mu_i / alpha_i) * (lambda1^alpha_i + lambda2^alpha_i + lambda3^alpha_i - 3) + (K/2)*(J - 1)^2
"""

import numpy as np
from typing import List, Tuple

class Ogden:
    def __init__(self, mu_list: List[float] = [1.2, -0.1, 0.05], alpha_list: List[float] = [1.3, -2.0, 4.5], K: float = 100.0):
        self.mu_list = np.array(mu_list)
        self.alpha_list = np.array(alpha_list)
        self.K = K

    def strain_energy(self, principal_stretches: Tuple[float, float, float], J: float = 1.0) -> float:
        l1, l2, l3 = principal_stretches
        W_iso = 0.0
        for mu_i, alpha_i in zip(self.mu_list, self.alpha_list):
            W_iso += (mu_i / alpha_i) * (l1**alpha_i + l2**alpha_i + l3**alpha_i - 3.0)
        W_vol = (self.K / 2.0) * ((J - 1.0)**2)
        return W_iso + W_vol

    def first_piola_stress(self, F: np.ndarray) -> np.ndarray:
        U, s, Vt = np.linalg.svd(F)
        J = np.prod(s)
        P_diag = np.zeros(3)
        for i in range(3):
            val = 0.0
            for mu_k, alpha_k in zip(self.mu_list, self.alpha_list):
                val += mu_k * (s[i]**(alpha_k - 1.0))
            P_diag[i] = val + self.K * (J - 1.0) * (J / s[i])
        return U @ np.diag(P_diag) @ Vt
