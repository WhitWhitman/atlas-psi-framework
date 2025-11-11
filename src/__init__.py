"""
Atlas Ψ Framework
A Universal Coherence Metric for Crisis Detection in AI

This package provides:
- psi_engine: Core Ψ (coherence) computation and analysis
- monitor: Real-time coherence tracking
- ethical_runtime: Policy enforcement layer (Safety → Coherence → Truth)

Author: Kenneth E. Whitman Jr.
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Kenneth E. Whitman Jr."
__license__ = "MIT"

from .psi_engine import PsiCurveEngine, Scene
from .monitor import PsiMonitor
from .ethical_runtime import EthicalRuntime

__all__ = [
    "PsiCurveEngine",
    "Scene",
    "PsiMonitor",
    "EthicalRuntime"
]
