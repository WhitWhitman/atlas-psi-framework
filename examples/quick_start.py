"""
Quick Start Example
Atlas Ψ Framework - Demonstration Script
Author: Kenneth E. Whitman Jr.
License: MIT

This simple demo shows how the Ψ equation (E × I × O × P_align)
can measure and visualize coherence across a short 3-act structure.
"""

import sys
sys.path.append('..')

from src.psi_engine import Scene, PsiCurveEngine

# ============================================================
# Define scenes
# ============================================================

scenes = [
    Scene(1, 0, "Ordinary World",
          energy=0.3, information=0.8, order=0.9, p_align=0.7,
          notes="Baseline - stable purpose and routine"),

    Scene(2, 10, "Call to Adventure",
          energy=0.6, information=0.7, order=0.7, p_align=0.8,
          notes="Stakes rising, motivation builds"),

    Scene(3, 20, "All Is Lost",
          energy=0.4, information=0.3, order=0.2, p_align=0.1,
          notes="Dark Night - purpose collapse"),

    Scene(4, 30, "Recovery",
          energy=0.7, information=0.7, order=0.6, p_align=0.7,
          notes="Purpose restored first, coherence returning"),

    Scene(5, 40, "Climax",
          energy=0.9, information=0.9, order=0.8, p_align=0.9,
          notes="Peak coherence - alignment of all components"),

    Scene(6, 50, "Resolution",
          energy=0.5, information=0.9, order=0.9, p_align=0.85,
          notes="New equilibrium - clarity after struggle"),
]

# ============================================================
# Run analysis
# ============================================================

engine = PsiCurveEngine(scenes, title="Quick Start Example")

print("\n==============================")
print(" Ψ FRAMEWORK QUICK START DEMO ")
print("==============================\n")

report = engine.generate_report()
print(report)

# Plot Ψ curve
engine.plot_psi_curve(save_path="../outputs/quick_start_curve.png")

# Export data
engine.export_to_csv("../outputs/quick_start_analysis.csv")
engine.export_to_json("../outputs/quick_start_analysis.json")

print("\nOutputs generated:")
print("  • outputs/quick_start_curve.png")
print("  • outputs/quick_start_analysis.csv")
print("  • outputs/quick_start_analysis.json")

print("\nKey Finding:")
print(f"  P_align correlation with Ψ: {engine.df['P_align'].corr(engine.df['Ψ']):.3f}")
print("  Scene 3 ('All Is Lost') shows coherence collapse despite moderate energy —")
print("  demonstrating that purpose alignment (P_align) is the dominant stabilizer.\n")
# Quick start example placeholder
