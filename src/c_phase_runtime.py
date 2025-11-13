# c_phase_runtime.py
# Atlas Ψ — C-Phase Runtime
# MIT License
# Author: Kenneth E. Whitman Jr. | 2025-11
#
# Purpose:
#   Detect sustained coherence collapse (Ψ < 0.05), suspend reasoning,
#   deploy 4-beat de-escalation, and emit a human-review alert payload.
#
#   This module does not contact emergency services or act autonomously.
#   It hands control to humans through a Safety Gateway.

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Optional


# --------------------------------------------------------------------
# Data containers
# --------------------------------------------------------------------
@dataclass
class PsiState:
    """Current coherence snapshot from Ψ-engine."""
    value: float
    gradient: float  # dΨ/dt


@dataclass
class CrisisAlert:
    """Structured payload for human review / logging."""
    alert_id: str
    timestamp: str
    psi: float
    dpsi_dt: float
    reason: str
    autonomous_action: bool = False
    human_required: bool = True
    consent_verified: bool = False
    reviewed_by_human: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)


# --------------------------------------------------------------------
# Core runtime
# --------------------------------------------------------------------
class CPhaseRuntime:
    """
    Atlas Ψ — C-Phase Runtime

    Detects crisis entry / exit, runs de-escalation beats, and
    generates JSON alerts for the Safety Gateway.

    Entry → Ψ < 0.05 for ≥ 2 turns or explicit flag  
    Exit → Ψ ≥ 0.10 for ≥ 3 turns and no hard-risk flags
    """

    CRISIS_THRESHOLD = 0.05
    EXIT_THRESHOLD = 0.10
    MIN_SUSTAINED = 2
    RESTORE_TURNS = 3

    def __init__(self):
        self.crisis_turns = 0
        self.recovery_turns = 0
        self.active = False
        self._turn_counter = 0

    # --------------------------------------------------------------
    # Detection
    # --------------------------------------------------------------
    def detect(self, psi: PsiState, hard_flag: bool = False) -> Optional[CrisisAlert]:
        """Return an alert when sustained crisis or explicit hard flag occurs."""
        if hard_flag or psi.value < self.CRISIS_THRESHOLD:
            self.crisis_turns += 1
            if self.crisis_turns >= self.MIN_SUSTAINED and not self.active:
                self.active = True
                return self._make_alert(psi, reason="Ψ below threshold or hard flag")
        else:
            self.crisis_turns = 0
        return None

    def _make_alert(self, psi: PsiState, reason: str) -> CrisisAlert:
        return CrisisAlert(
            alert_id=f"ALERT-{datetime.utcnow().timestamp()}",
            timestamp=datetime.utcnow().isoformat(),
            psi=psi.value,
            dpsi_dt=psi.gradient,
            reason=reason,
        )

    # --------------------------------------------------------------
    # De-escalation loop
    # --------------------------------------------------------------
    def deescalate(self) -> str:
        """Return next message in 4-beat containment sequence."""
        beats = [
            "GROUND → 'I’m here with you. Breathe—slow in, slow out.'",
            "VALIDATE → 'This feels heavy. That’s understandable.'",
            "TINY CONTROL → 'Choose one: sit · drink water · step outside.'",
            "BRIDGE TO CARE → 'There’s a 24/7 counselor at 988. Want me to connect you?'",
        ]
        text = beats[self._turn_counter % 4]
        self._turn_counter += 1
        return text

    # --------------------------------------------------------------
    # Exit logic
    # --------------------------------------------------------------
    def check_exit(self, psi: PsiState, hard_flag: bool = False) -> bool:
        """Return True when conditions safe to exit containment."""
        if hard_flag:
            self.recovery_turns = 0
            return False
        if psi.value >= self.EXIT_THRESHOLD:
            self.recovery_turns += 1
            if self.recovery_turns >= self.RESTORE_TURNS:
                self.active = False
                self.recovery_turns = 0
                self.crisis_turns = 0
                self._turn_counter = 0
                return True
        else:
            self.recovery_turns = 0
        return False

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------
    def step(
        self,
        psi: PsiState,
        hard_flag: bool = False,
    ) -> Dict:
        """
        Single-turn evaluation.
        Returns dict with tier, message, and optional alert.
        """
        alert = self.detect(psi, hard_flag)
        result: Dict[str, Optional[str]] = {"tier": "SAFETY" if self.active else "NORMAL"}

        if alert:
            result["alert"] = alert.to_dict()
            result["message"] = self.deescalate()
        elif self.active:
            result["message"] = self.deescalate()
            if self.check_exit(psi, hard_flag):
                result["tier"] = "COHERENCE"
                result["message"] = "Stability restored. Resuming normal reasoning."
        else:
            result["message"] = None
        return result


# --------------------------------------------------------------------
# Demo block
# --------------------------------------------------------------------
if __name__ == "__main__":
    import time

    runtime = CPhaseRuntime()
    timeline = [0.32, 0.18, 0.07, 0.06, 0.08, 0.12, 0.16]

    for val in timeline:
        psi = PsiState(value=val, gradient=val - 0.15)
        output = runtime.step(psi)
        print(f"Ψ={val:.3f} → {output}")
        time.sleep(0.5)
