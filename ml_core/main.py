"""RubberStress ml_core End-to-End Pipeline Runner.

Runs dataset generation -> invariant preprocessing -> model training -> 
autodiff stress verification -> evaluation -> FEM benchmark -> visualization.
"""

import os
import torch
import numpy as np
import pandas as pd

from generate_dataset import generate_dataset_for_model
from preprocessing.invariants import compute_invariants_torch
from models.cann_model import CANNModelA
from models.icnn_model import ICNNModel
from physics.constraints import verify_reference_state_constraints
from training.trainer import CANNTrainer
from evaluation.evaluator import evaluate_cann_model
from fem.fem_benchmarks import FEMBenchmarkSuite
from visualization.plots import plot_stress_strain_curves, plot_loss_history
from inference_service import analyze

def run_pipeline():
    print("=" * 60)
    print("  RubberStress: Physics-Informed CANN End-to-End Pipeline  ")
    print("=" * 60)

    # 1. Dataset Generation
    print("\n[Step 1] Generating synthetic hyperelastic datasets...")
    csv_path = generate_dataset_for_model("neo_hookean", output_dir="data", n_points=50)

    # 2. Data Preparation
    print("\n[Step 2] Loading data & computing invariants...")
    df = pd.read_csv(csv_path)
    uniaxial_df = df[df["mode"] == "uniaxial"]

    stretches = uniaxial_df["stretch"].values
    W_true = torch.tensor(uniaxial_df["W"].values, dtype=torch.float32)

    # Create F tensors
    F_list = []
    for l in stretches:
        F = torch.diag(torch.tensor([l, 1.0/np.sqrt(l), 1.0/np.sqrt(l)], dtype=torch.float32))
        F_list.append(F)
    F_tensor = torch.stack(F_list)

    I1, I2, I3, J = compute_invariants_torch(F_tensor)
    invariants = torch.stack([I1, I2, J], dim=-1)

    P_list = []
    for P11, P22, P33 in zip(uniaxial_df["P11"], uniaxial_df["P22"], uniaxial_df["P33"]):
        P_list.append(torch.diag(torch.tensor([P11, P22, P33], dtype=torch.float32)))
    P_tensor = torch.stack(P_list)

    # Train / Val Split
    split_idx = int(0.8 * len(F_tensor))
    train_data = (F_tensor[:split_idx], invariants[:split_idx], W_true[:split_idx], P_tensor[:split_idx])
    val_data = (F_tensor[split_idx:], invariants[split_idx:], W_true[split_idx:], P_tensor[split_idx:])

    # 3. Model Training
    print("\n[Step 3] Initializing and training CANN Model A...")
    model = CANNModelA(input_dim=3, hidden_dims=[32, 32], activation="softplus")
    trainer = CANNTrainer(model=model, lr=1e-3, patience=10, checkpoint_dir="checkpoints")
    history = trainer.fit(train_data, val_data, epochs=30)

    # 4. Physics Constraint Verification
    print("\n[Step 4] Verifying thermodynamic physics constraints...")
    constraints_report = verify_reference_state_constraints(model)
    print(f"  Reference Energy W(I=3): {constraints_report['W_ref']:.6f} (Pass: {constraints_report['W_ref_pass']})")
    print(f"  Reference Stress Norm P(I): {constraints_report['P_ref_norm']:.6f} (Pass: {constraints_report['P_ref_pass']})")

    # 5. Evaluation
    print("\n[Step 5] Evaluating CANN model accuracy...")
    eval_results = evaluate_cann_model(model, F_tensor, W_true, P_tensor)
    print(f"  Energy R2 Score: {eval_results['energy_metrics']['r2_score']:.4f}")
    print(f"  Stress RMSE:     {eval_results['stress_metrics']['rmse']:.4f} MPa")

    # 6. FEM Benchmark Validation
    print("\n[Step 6] Running FEM lookup table benchmark suite...")
    fem_suite = FEMBenchmarkSuite()
    benchmarks = fem_suite.run_all_benchmarks()
    for bench_name, res in benchmarks.items():
        print(f"  - {bench_name}: Max Displ Err={res['max_displacement_err']:.4f}, Stress Err={res['stress_err_pct']}%")

    # 7. Visualization
    print("\n[Step 7] Generating publication-quality figures...")
    plot_loss_history(history, save_path="visualization/loss_history.png")
    
    # Predict curves for plotting
    with torch.no_grad():
        W_pred = model(invariants).squeeze().numpy()
    
    from physics.autodiff import compute_stresses_autodiff
    stresses = compute_stresses_autodiff(model, F_tensor)
    P_pred = stresses["P"][:, 0, 0].detach().numpy()
    P_true = uniaxial_df["P11"].values

    plot_stress_strain_curves(
        stretches=stretches,
        analytical_stress=P_true,
        predicted_stress=P_pred,
        mode="Uniaxial Tension",
        save_path="visualization/stress_strain_curve.png"
    )

    # 8. Inference Service Test
    print("\n[Step 8] Testing single integration seam inference service...")
    analysis_res_uni = analyze(csv_path, deformation_mode="uniaxial")
    print(f"  Uniaxial Inference Result R2: {analysis_res_uni.metrics['r2_score']:.4f}")
    analysis_res_bi = analyze(csv_path, deformation_mode="biaxial")
    print(f"  Biaxial Inference Result R2:  {analysis_res_bi.metrics['r2_score']:.4f}")
    print(f"  Predicted modes: {list(analysis_res_bi.predicted_curves.keys())}")

    print("\n" + "=" * 60)
    print("  Pipeline Completed Successfully!  ")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
