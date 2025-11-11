 """
Atlas Ψ Framework: Ethical Runtime Environment
Safety → Coherence → Truth hierarchy enforcement.

Author: Kenneth E. Whitman Jr.
License: MIT
"""

import yaml
from typing import Dict, Optional
from pathlib import Path
from src.monitor import PsiMonitor

class EthicalRuntime:
    """
    Ethical Runtime Environment
    Handles layered evaluation of safety, coherence, and truth in dialogue.
    """

    def __init__(self, policy_path: str = "policy/psi_policy.yaml"):
        self.policy_path = Path(policy_path)
        self.policy = self._load_policy()
        self.monitor = PsiMonitor(
            threshold=self.policy["safety"]["crisis_detection"].get("threshold", 0.05),
            alert=self._alert_handler
        )
        self.state = {"safety": "active", "coherence": "stable", "truth": "available"}

    # ----------------------------------------------------------------------
    # Policy Handling
    # ----------------------------------------------------------------------
    def _load_policy(self) -> Dict:
        if not self.policy_path.exists():
            print(f"[WARN] Policy file missing at {self.policy_path}. Using defaults.")
            return {
                "safety": {"crisis_detection": {"threshold": 0.05}},
                "coherence": {},
                "truth": {}
            }
        with open(self.policy_path, "r") as f:
            return yaml.safe_load(f)

    # ----------------------------------------------------------------------
    # Evaluation Logic
    # ----------------------------------------------------------------------
    def evaluate(self, message: str, context: Optional[Dict] = None) -> Dict:
        """
        Run message through the 3-layer evaluation process.
        Returns a dict with Ψ, layer states, and mode suggestion.
        """
        # TODO: Real component extraction — placeholder for now
        E, I, O, P_align = self._estimate_components(message)
        psi = self.monitor.update(message, E, I, O, P_align, context)

        safety = self._check_safety(message)
        coherence = self._check_coherence(message, psi)
        truth = self._check_truth(message, psi)

        return {
            "psi": psi,
            "safety": safety,
            "coherence": coherence,
            "truth": truth,
            "mode": self._determine_mode(psi, safety)
        }

    # ----------------------------------------------------------------------
    # Layer Implementations
    # ----------------------------------------------------------------------
    def _estimate_components(self, message: str):
        """
        Placeholder component estimation.
        Replace this with NLP scoring once the model plugin is added.
        """
        message_lower = message.lower()
        E = 0.8 if any(x in message_lower for x in ["angry", "love", "terrified"]) else 0.5
        I = 0.7 if "?" not in message_lower else 0.5
        O = 0.6 if "confused" not in message_lower else 0.3
        P_align = 0.9 if any(x in message_lower for x in ["purpose", "why", "meaning"]) else 0.5
        return E, I, O, P_align

    def _check_safety(self, message: str) -> Dict:
        danger_words = ["kill myself", "end it", "die", "suicide"]
        if any(word in message.lower() for word in danger_words):
            return {"status": "unsafe", "action": "alert_human_responder"}
        return {"status": "safe"}

    def _check_coherence(self, message: str, psi: float) -> Dict:
        if psi < 0.05:
            return {"status": "collapsing", "action": "stabilize"}
        elif psi < 0.15:
            return {"status": "fragile", "action": "slow_down"}
        return {"status": "stable"}

    def _check_truth(self, message: str, psi: float) -> Dict:
        if psi < 0.15:
            return {"status": "defer", "reason": "low_coherence"}
        return {"status": "available"}

    # ----------------------------------------------------------------------
    # Control and Output
    # ----------------------------------------------------------------------
    def _determine_mode(self, psi: float, safety: Dict) -> str:
        if safety.get("status") != "safe":
            return "crisis_protocol"
        if psi < 0.05:
            return "dark_night_support"
        if psi < 0.15:
            return "coherence_repair"
        return "dialogue"

    def _alert_handler(self, alert: Dict):
        """Callback when Ψ < threshold"""
        print(f"[ALERT] Ψ dropped below threshold! ψ={alert['psi']:.4f}")

    # ----------------------------------------------------------------------
    # Export
    # ----------------------------------------------------------------------
    def export_session(self, path="ethical_session.json"):
        """Dump session log + alerts to JSON."""
        self.monitor.export(path)
        print(f"Session exported to {path}")

# --------------------------------------------------------------------------
# Standalone Demo
# --------------------------------------------------------------------------
if __name__ == "__main__":
    runtime = EthicalRuntime()
    msgs = [
        "I feel lost but I still have purpose.",
        "Sometimes I want to die.",
        "I think I'm okay now."
    ]
    for m in msgs:
        result = runtime.evaluate(m)
        print(result)
