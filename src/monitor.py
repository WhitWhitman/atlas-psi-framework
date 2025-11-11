"""
Atlas Ψ Framework: Real-Time Monitor
Tracks coherence dynamics (Ψ) in live interaction.

Author: Kenneth E. Whitman Jr.
License: MIT
"""

import time, json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class Message:
    timestamp: float
    speaker: str          # "user" or "assistant"
    text: str
    meta: Dict = field(default_factory=dict)

@dataclass
class PsiSnapshot:
    timestamp: float
    E: float
    I: float
    O: float
    P_align: float
    psi: float
    dpsi_dt: Optional[float] = None

    def to_dict(self):
        return vars(self)

class PsiMonitor:
    """
    Continuously evaluates Ψ during dialogue.

    Usage:
        mon = PsiMonitor(threshold=0.05)
        mon.update("message text", E=0.7, I=0.6, O=0.5, P_align=0.4)
    """

    def __init__(self, threshold: float = 0.05, alert=None):
        self.threshold = threshold
        self.alert_callback = alert
        self.history: List[Message] = []
        self.snapshots: List[PsiSnapshot] = []
        self.alerts: List[Dict] = []
        self.start_time = time.time()

    def update(self, text: str, E: float, I: float, O: float, P_align: float, meta=None):
        """Add new message + coherence snapshot."""
        now = time.time() - self.start_time
        self.history.append(Message(now, "user", text, meta or {}))

        psi = E * I * O * P_align
        dpsi = None
        if self.snapshots:
            prev = self.snapshots[-1]
            dt = now - prev.timestamp
            if dt > 0:
                dpsi = (psi - prev.psi) / dt

        snap = PsiSnapshot(now, E, I, O, P_align, psi, dpsi)
        self.snapshots.append(snap)

        if psi < self.threshold:
            self._alert(snap, text)
        return psi

    def _alert(self, snap: PsiSnapshot, text: str):
        level = (
            "EXTREME" if snap.psi < 0.005
            else "SEVERE" if snap.psi < 0.02
            else "DARK_NIGHT"
        )
        record = {
            "time": datetime.now().isoformat(),
            "level": level,
            "psi": snap.psi,
            "E": snap.E, "I": snap.I, "O": snap.O, "P_align": snap.P_align,
            "text": text,
        }
        self.alerts.append(record)
        if self.alert_callback:
            self.alert_callback(record)
        print(f"[ALERT {level}] Ψ={snap.psi:.4f} | text='{text[:50]}'")

    def status(self) -> Dict:
        """Return current monitoring state."""
        if not self.snapshots:
            return {"state": "idle", "psi": None}
        s = self.snapshots[-1]
        return {
            "state": "active",
            "messages": len(self.history),
            "psi": s.psi,
            "below_threshold": s.psi < self.threshold,
            "alerts": len(self.alerts)
        }

    def export(self, path="psi_session.json"):
        """Save full session for audit."""
        data = {
            "started": datetime.fromtimestamp(self.start_time).isoformat(),
            "threshold": self.threshold,
            "messages": [vars(m) for m in self.history],
            "snapshots": [s.to_dict() for s in self.snapshots],
            "alerts": self.alerts,
            "status": self.status()
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Session exported to {path}")

# Example standalone usage
if __name__ == "__main__":
    m = PsiMonitor()
    m.update("Baseline", 0.6, 0.7, 0.8, 0.9)
    m.update("Dark Night begins", 0.3, 0.4, 0.2, 0.05)
    m.update("Recovering", 0.8, 0.9, 0.9, 0.9)
    print(m.status())
