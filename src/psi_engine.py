"""
Atlas Ψ Framework: Core Engine
Ψ = E × I × O × P_align

Mathematical framework for coherence dynamics detection.
Validated through independent AI replication.

Author: Kenneth E. Whitman Jr.
License: MIT
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import json

# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

@dataclass
class Scene:
    """
    Represents a single narrative scene or conversational moment.
    Components scored 0–1:
      E = Emotional intensity
      I = Information clarity
      O = Order or control
      P_align = Purpose alignment (meaning)
    """
    scene_number: int
    timestamp: float
    title: str
    energy: float
    information: float
    order: float
    p_align: float
    characters: Optional[List[str]] = None
    location: str = ""
    notes: str = ""

    def calculate_psi(self) -> float:
        """Compute Ψ = E × I × O × P_align"""
        return self.energy * self.information * self.order * self.p_align

    def __post_init__(self):
        for name, val in [('energy', self.energy), ('information', self.information),
                          ('order', self.order), ('p_align', self.p_align)]:
            if not 0.0 <= val <= 1.0:
                raise ValueError(f"{name} must be between 0–1 (got {val}).")

# ============================================================================
# EMOTIONAL CLASSIFICATION
# ============================================================================

EMOTION_BANDS = [
    ("Transcendence", 0.7, float('inf')),
    ("Resolve", 0.4, 0.7),
    ("Hope", 0.08, 0.4),
    ("Stable", -0.1, 0.08),
    ("Fear", -0.4, -0.1),
    ("Despair", -0.7, -0.4),
    ("Collapse", float('-inf'), -0.7),
]

DARK_MIN, DARK_MAX = 0.005, 0.05

# ============================================================================
# MAIN ENGINE
# ============================================================================

class PsiCurveEngine:
    """Calculates coherence dynamics (Ψ) and emotional derivatives (dΨ/dt)."""

    def __init__(self, scenes: List[Scene], title: str = "Analysis"):
        if len(scenes) < 2:
            raise ValueError("At least two scenes required for derivative.")
        self.scenes = scenes
        self.title = title
        self.df = None
        self._compute()

    def _compute(self):
        t = [s.timestamp for s in self.scenes]
        psi = [s.calculate_psi() for s in self.scenes]
        dpsi = np.gradient(psi, t)
        emo = [self._classify(d) for d in dpsi]
        self.df = pd.DataFrame({
            "scene": [s.scene_number for s in self.scenes],
            "timestamp": t,
            "title": [s.title for s in self.scenes],
            "E": [s.energy for s in self.scenes],
            "I": [s.information for s in self.scenes],
            "O": [s.order for s in self.scenes],
            "P_align": [s.p_align for s in self.scenes],
            "Ψ": psi,
            "dΨ/dt": dpsi,
            "emotion": emo,
            "notes": [s.notes for s in self.scenes]
        })
        self.df["dark_night"] = self.df["Ψ"].between(DARK_MIN, DARK_MAX)
        self.df["collapse"] = self.df["Ψ"] < DARK_MIN

    def _classify(self, rate):
        for name, lo, hi in EMOTION_BANDS:
            if lo <= rate < hi:
                return name
        return "Unknown"

    def summary(self) -> Dict:
        d = self.df
        return {
            "mean_psi": d["Ψ"].mean(),
            "min_psi": d["Ψ"].min(),
            "max_psi": d["Ψ"].max(),
            "dark_nights": d["dark_night"].sum(),
            "extreme_collapses": d["collapse"].sum(),
            "p_align_corr": d["P_align"].corr(d["Ψ"]),
        }

    def plot(self, save_path=None):
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(self.df["timestamp"], self.df["Ψ"], color="blue", lw=2)
        ax.scatter(self.df["timestamp"], self.df["Ψ"], color="navy", s=40)
        ax.axhspan(DARK_MIN, DARK_MAX, color="red", alpha=0.15, label="Dark Night")
        ax.set_title(f"{self.title} Ψ-Curve")
        ax.set_xlabel("Time")
        ax.set_ylabel("Ψ (Coherence)")
        ax.legend()
        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    def export_json(self, path="psi_results.json"):
        with open(path, "w") as f:
            json.dump(self.df.to_dict(orient="records"), f, indent=2)
        print(f"Exported results to {path}")

# ============================================================================
# EXAMPLE
# ============================================================================

if __name__ == "__main__":
    s = [
        Scene(1, 0, "Opening", 0.4, 0.8, 0.9, 0.7),
        Scene(2, 10, "Crisis", 0.9, 0.4, 0.3, 0.2),
        Scene(3, 20, "Recovery", 0.7, 0.9, 0.8, 0.9),
    ]
    e = PsiCurveEngine(s, title="Demo Narrative")
    print(e.summary())
    e.plot()
# Core Ψ engine placeholder
