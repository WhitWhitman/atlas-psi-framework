"""
Unforgiven (1992) — Ψ-Curve Demonstration
Atlas Ψ Framework Example

Shows how coherence (Ψ = E × I × O × P_align) changes over a narrative arc.
Each scene is manually scored 0–1 for Energy, Information, Order, and Purpose Alignment.

Author: Kenneth E. Whitman Jr.
License: MIT
"""

from src.psi_engine import Scene, PsiCurveEngine


# --------------------------------------------------------------------------
# Scene Data (validated scoring)
# --------------------------------------------------------------------------
scenes = [
    Scene(1, 0, "Pig Farmer – Reformed Life",
          energy=0.3, information=0.8, order=0.7, p_align=0.6,
          notes="Low-stakes domestic life; ex-killer turned farmer."),
    Scene(2, 15, "Schofield Kid Arrives",
          energy=0.5, information=0.7, order=0.7, p_align=0.5,
          notes="Temptation to return to violence."),
    Scene(3, 25, "Decision to Go",
          energy=0.6, information=0.7, order=0.6, p_align=0.7,
          notes="Purpose: provide for children."),
    Scene(4, 35, "Recruit Ned Logan",
          energy=0.6, information=0.8, order=0.7, p_align=0.8,
          notes="Partnership; plan clear."),
    Scene(5, 50, "Arrive in Big Whiskey",
          energy=0.7, information=0.7, order=0.6, p_align=0.7,
          notes="Opposition introduced; town’s moral order exposed."),
    Scene(6, 60, "Little Bill Beats Munny",
          energy=0.8, information=0.5, order=0.2, p_align=0.4,
          notes="Violent collapse; questioning purpose."),
    Scene(7, 80, "First Kill – Davey Bunting",
          energy=0.7, information=0.6, order=0.4, p_align=0.3,
          notes="Moral conflict; remorse and doubt."),
    Scene(8, 95, "Ned Captured",
          energy=0.8, information=0.5, order=0.3, p_align=0.3,
          notes="Mission falters; loss of control."),
    Scene(9, 105, "Ned’s Death – News Arrives",
          energy=0.9, information=0.4, order=0.1, p_align=0.05,
          notes="DARK NIGHT — total collapse of coherence."),
    Scene(10, 110, "Munny Drinks Whiskey",
          energy=0.9, information=0.6, order=0.3, p_align=0.2,
          notes="Rage focus; purpose reforms."),
    Scene(11, 115, "I've Killed Everything That Walked or Crawled",
          energy=0.95, information=0.8, order=0.6, p_align=0.8,
          notes="Identity acceptance; controlled violence."),
    Scene(12, 120, "Saloon Confrontation – Kills Little Bill",
          energy=0.95, information=0.9, order=0.8, p_align=0.9,
          notes="Moral authority restored; climax."),
    Scene(13, 125, "You Better Bury Ned Right",
          energy=0.7, information=0.9, order=0.9, p_align=0.85,
          notes="Justice; order restored."),
    Scene(14, 130, "Epilogue",
          energy=0.4, information=0.8, order=0.7, p_align=0.7,
          notes="Ambiguous peace; coherence regained.")
]


# --------------------------------------------------------------------------
# Run analysis
# --------------------------------------------------------------------------
engine = PsiCurveEngine(scenes, title="Unforgiven (1992)")

print(engine.generate_report())

print("\nGenerating visualizations...")
engine.plot_psi_curve(save_path="../outputs/unforgiven_psi_curve.png")

print("\nExporting data...")
engine.export_to_csv("../outputs/unforgiven_analysis.csv")
engine.export_to_json("../outputs/unforgiven_analysis.json")

print("\nAnalysis complete.")
print("Files written to /outputs:")
print(" - unforgiven_psi_curve.png")
print(" - unforgiven_analysis.csv")
print(" - unforgiven_analysis.json")
