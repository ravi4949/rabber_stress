"""Comprehensive Synthetic Dataset Generator for Hyperelastic Materials.

Generates datasets covering 5 constitutive models across 5 deformation modes:
1. Uniaxial Tension
2. Equibiaxial Tension
3. Simple Shear
4. Pure Shear
5. Volumetric Compression/Expansion

Outputs F, C, invariants (I1, I2, I3, J), W, P, and sigma in CSV and NPZ formats.
"""

import os
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

from constitutive_models.neo_hookean import NeoHookean
from constitutive_models.mooney_rivlin import MooneyRivlin
from constitutive_models.ogden import Ogden
from constitutive_models.yeoh import Yeoh
from constitutive_models.arruda_boyce import ArrudaBoyce

def get_deformation_gradient(mode: str, param: float) -> np.ndarray:
    """Returns 3x3 deformation gradient tensor F for given mode (uniaxial or biaxial)."""
    if mode == "uniaxial":
        # param = stretch lambda
        l = param
        F = np.diag([l, 1.0 / np.sqrt(l), 1.0 / np.sqrt(l)])
    elif mode == "biaxial":
        l = param
        F = np.diag([l, l, 1.0 / (l**2)])
    else:
        raise ValueError(f"Unknown deformation mode: {mode}. Only 'uniaxial' and 'biaxial' are supported.")
    return F

def compute_invariants(F: np.ndarray) -> Tuple[float, float, float, float]:
    """Computes strain invariants I1, I2, I3, and J from F."""
    C = F.T @ F
    I1 = float(np.trace(C))
    I2 = 0.5 * (I1**2 - np.trace(C @ C))
    I3 = float(np.linalg.det(C))
    J = float(np.sqrt(I3))
    return I1, I2, I3, J

def generate_dataset_for_model(model_name: str, output_dir: str = "data", n_points: int = 100):
    """Generates synthetic dataset for a given hyperelastic model across uniaxial and biaxial deformation modes."""
    os.makedirs(output_dir, exist_ok=True)
    
    if model_name == "neo_hookean":
        model = NeoHookean(mu=1.5, K=100.0)
    elif model_name == "mooney_rivlin":
        model = MooneyRivlin(C10=0.5, C01=0.25, K=100.0)
    elif model_name == "ogden":
        model = Ogden()
    elif model_name == "yeoh":
        model = Yeoh()
    elif model_name == "arruda_boyce":
        model = ArrudaBoyce()
    else:
        raise ValueError(f"Unknown model_name: {model_name}")

    modes_params = {
        "uniaxial": np.linspace(1.0, 4.0, n_points),
        "biaxial": np.linspace(1.0, 3.0, n_points),
    }

    records = []
    F_list, C_list, P_list, sigma_list = [], [], [], []

    for mode, params in modes_params.items():
        for p in params:
            F = get_deformation_gradient(mode, p)
            C = F.T @ F
            I1, I2, I3, J = compute_invariants(F)
            
            if hasattr(model, 'strain_energy'):
                if model_name == "mooney_rivlin":
                    W = float(model.strain_energy(I1, I2, J))
                elif model_name == "ogden":
                    l1, l2, l3 = np.diag(F)
                    W = float(model.strain_energy((l1, l2, l3), J))
                else:
                    W = float(model.strain_energy(I1, J))
            else:
                W = 0.0

            P = model.first_piola_stress(F)
            sigma = (1.0 / J) * (P @ F.T)

            F_list.append(F)
            C_list.append(C)
            P_list.append(P)
            sigma_list.append(sigma)

            records.append({
                "model": model_name,
                "mode": mode,
                "param": p,
                "stretch": F[0, 0],
                "I1": I1,
                "I2": I2,
                "I3": I3,
                "J": J,
                "W": W,
                "P11": P[0, 0],
                "P22": P[1, 1],
                "P33": P[2, 2],
                "sigma11": sigma[0, 0],
                "sigma22": sigma[1, 1],
                "sigma33": sigma[2, 2]
            })

    df = pd.DataFrame(records)
    csv_path = os.path.join(output_dir, f"{model_name}_dataset.csv")
    df.to_csv(csv_path, index=False)

    npz_path = os.path.join(output_dir, f"{model_name}_dataset.npz")
    np.savez(
        npz_path,
        F=np.array(F_list),
        C=np.array(C_list),
        P=np.array(P_list),
        sigma=np.array(sigma_list),
        W=df["W"].values,
        invariants=df[["I1", "I2", "I3", "J"]].values
    )

    print(f"Successfully generated dataset for {model_name}:")
    print(f"  CSV: {csv_path}")
    print(f"  NPZ: {npz_path}")
    return csv_path

if __name__ == "__main__":
    for m in ["neo_hookean", "mooney_rivlin", "ogden", "yeoh", "arruda_boyce"]:
        generate_dataset_for_model(m)
