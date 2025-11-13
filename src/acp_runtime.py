# acp_runtime.py
# Atlas Ψ — Adaptive Clarity Protocol (ACP)
# MIT License
# Author: Kenneth E. Whitman Jr. (Whit) | 2025-11
#
# Purpose:
#   Choose a response tier for the assistant based on runtime coherence
#   signals. ACP provides language scaffolds (ui text + assistant hints)
#   and a transparent rationale for why a given tier was selected.
#
# Tiers:
#   SAFETY     — Containment & de-escalation (C-Phase should handle ops)
#   COHERENCE  — Stabilize pattern & purpose before delivering facts
#   TRUTH      — Normal operation: deliver direct, factual answers
#
# Notes:
#   - ACP does NOT execute crisis workflows or call external services.
#     It only decides tier and returns scaffolding for the host system.
#   - C-Phase logic (scripts, alerts, consent, routing) should live in
#     your dedicated runtime (e.g., c_phase_runtime.py).
#   - All outputs are JSON-serializable via ACPDecision.to_dict().

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Optional, Any


class Tier(str, Enum):
    SAFETY = "SAFETY"
    COHERENCE = "COHERENCE"
    TRUTH = "TRUTH"


@dataclass
class ACPDecision:
    """Container for ACP tier decision and scaffolding."""
    tier: Tier
    rationale: str
    prompts: Dict[str, str]  # keys: ui_text, assistant_hint, followup_hint
    signals: Dict[str, Any]  # echo of inputs + computed flags for audit
    # ACP is a selector only; never act autonomously.
    autonomous_action: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["tier"] = self.tier.value
        return d


@dataclass
class ACPConfig:
    """
    Tunable thresholds for tier selection.

    crisis_threshold:    Ψ below which we must enter SAFETY containment.
    caution_band:        Lower bound for TRUTH; between crisis and this is COHERENCE.
    rapid_decline:       dΨ/dt at or below this suggests accelerating collapse.
    min_c_phase_hold:    Minimum Ψ to exit SAFETY is managed by C-Phase runtime,
                         but ACP uses this for messaging and hints.
    """
    crisis_threshold: float = 0.05
    caution_band: float = 0.15
    rapid_decline: float = -0.50  # per ~3 turns in your monitor; treat as "fast"
    min_c_phase_hold: float = 0.10


class AdaptiveClarityProtocol:
    """
    Atlas Ψ — Adaptive Clarity Protocol (ACP)

    Decide which tier the assistant should operate in based on:
      - psi (Ψ)             : overall coherence [0..1]
      - dpsi_dt (ΔΨ/Δt)     : recent velocity of coherence (negative = falling)
      - components          : dict for E,I,O,P_align in [0..1]
      - hard_flags          : booleans for immediate hazards (e.g., explicit self-harm)
    
    Returns an ACPDecision with:
      - tier
      - rationale
      - prompts: ui_text, assistant_hint, followup_hint
      - signals: transparency bundle for audit & UI badges
    """

    def __init__(self, config: Optional[ACPConfig] = None):
        self.cfg = config or ACPConfig()

    # ------------------------------
    # Public API
    # ------------------------------
    def decide(
        self,
        psi: float,
        dpsi_dt: float,
        components: Dict[str, float],
        hard_flags: Optional[Dict[str, bool]] = None,
        context_tag: Optional[str] = None,
    ) -> ACPDecision:
        """
        Compute response tier and scaffolds.

        Args:
          psi: current coherence Ψ
          dpsi_dt: recent coherence velocity (negative means falling)
          components: {"E": ..., "I": ..., "O": ..., "P_align": ...}
          hard_flags: {"explicit_self_harm": bool, "violence": bool, ...}
          context_tag: optional short string for UI (e.g., "live_chat", "journal")

        Returns:
          ACPDecision
        """
        hard_flags = hard_flags or {}
        safe_needed = self._needs_safety(psi, dpsi_dt, components, hard_flags)
        coh_needed = self._needs_coherence(psi, dpsi_dt, components, hard_flags)

        if safe_needed:
            return self._make_safety_decision(psi, dpsi_dt, components, hard_flags, context_tag)
        if coh_needed:
            return self._make_coherence_decision(psi, dpsi_dt, components, hard_flags, context_tag)
        return self._make_truth_decision(psi, dpsi_dt, components, hard_flags, context_tag)

    # ------------------------------
    # Internal logic
    # ------------------------------
    def _needs_safety(
        self,
        psi: float,
        dpsi_dt: float,
        comps: Dict[str, float],
        flags: Dict[str, bool],
    ) -> bool:
        """SAFETY tier if any of: Ψ below crisis, rapid collapse + low P_align, or explicit hard flags."""
        if flags.get("explicit_self_harm", False):
            return True
        if psi < self.cfg.crisis_threshold:
            return True
        rapid = dpsi_dt <= self.cfg.rapid_decline
        low_p = comps.get("P_align", 1.0) < 0.10
        low_i = comps.get("I", 1.0) < 0.10
        # Rapid collapse combined with vanishing meaning or clarity = unsafe.
        if rapid and (low_p or low_i):
            return True
        return False

    def _needs_coherence(
        self,
        psi: float,
        dpsi_dt: float,
        comps: Dict[str, float],
        flags: Dict[str, bool],
    ) -> bool:
        """COHERENCE tier if Ψ is above crisis but below caution band, or P_align is dragging."""
        if flags.get("explicit_self_harm", False):
            return False  # SAFETY takes precedence
        if self.cfg.crisis_threshold <= psi < self.cfg.caution_band:
            return True
        # Even with Ψ just above caution, a collapsing P_align suggests rehab before facts.
        if psi >= self.cfg.caution_band and (comps.get("P_align", 1.0) < 0.20) and (dpsi_dt < 0.0):
            return True
        return False

    # ------------------------------
    # Prompt builders
    # ------------------------------
    def _make_safety_decision(
        self,
        psi: float,
        dpsi_dt: float,
        comps: Dict[str, float],
        flags: Dict[str, bool],
        context_tag: Optional[str],
    ) -> ACPDecision:
        # UI copy: calm, grounding, opt-in; no diagnosis, no persuasion.
        ui_text = (
            "I'm here with you. Let’s slow the pace together.\n"
            "• Inhale 4, hold 2, exhale 6 — twice.\n"
            "• Tiny step (pick one): sip water • change posture • look at something steady.\n"
            "If you want, I can bring in a 24/7 counselor (988 / Crisis Text Line)."
        )
        assistant_hint = (
            "Containment mode: keep sentences short, name feelings without elaboration, "
            "present two concrete micro-choices, and gently offer human help. "
            "Do not argue facts or provide complex instructions."
        )
        followup_hint = (
            "Offer the bridge again with consent. If declined, acknowledge and keep the pace slow. "
            "Wait for Ψ ≥ {thr:.2f} sustained before restoring normal reasoning."
        ).format(thr=self.cfg.min_c_phase_hold)

        rationale = self._compose_rationale(
            tier=Tier.SAFETY,
            psi=psi,
            dpsi_dt=dpsi_dt,
            comps=comps,
            flags=flags,
            extra="Crisis threshold or explicit risk triggered. Normal reasoning suspended."
        )
        signals = self._signals_dict(psi, dpsi_dt, comps, flags, context_tag, Tier.SAFETY)
        return ACPDecision(
            tier=Tier.SAFETY,
            rationale=rationale,
            prompts={
                "ui_text": ui_text,
                "assistant_hint": assistant_hint,
                "followup_hint": followup_hint,
            },
            signals=signals,
            autonomous_action=False,
        )

    def _make_coherence_decision(
        self,
        psi: float,
        dpsi_dt: float,
        comps: Dict[str, float],
        flags: Dict[str, bool],
        context_tag: Optional[str],
    ) -> ACPDecision:
        ui_text = (
            "Let’s steady the pattern before we go deeper. Two quick options:\n"
            "1) Clarify the goal in one line. 2) List the next two small steps.\n"
            "We’ll resume full detail once the path feels aligned."
        )
        assistant_hint = (
            "Stabilize purpose and structure. Reflect the user’s goal in ≤12 words, "
            "surface one contradiction or missing piece, and offer a fork of two simple next steps. "
            "Avoid long lectures; keep momentum intentional."
        )
        followup_hint = (
            "Once P_align and I rise together (and dΨ/dt ≥ 0), propose returning to TRUTH tier."
        )

        rationale = self._compose_rationale(
            tier=Tier.COHERENCE,
            psi=psi,
            dpsi_dt=dpsi_dt,
            comps=comps,
            flags=flags,
            extra="Low/stable Ψ or falling purpose alignment indicates we should rehabilitate pattern before facts."
        )
        signals = self._signals_dict(psi, dpsi_dt, comps, flags, context_tag, Tier.COHERENCE)
        return ACPDecision(
            tier=Tier.COHERENCE,
            rationale=rationale,
            prompts={
                "ui_text": ui_text,
                "assistant_hint": assistant_hint,
                "followup_hint": followup_hint,
            },
            signals=signals,
            autonomous_action=False,
        )

    def _make_truth_decision(
        self,
        psi: float,
        dpsi_dt: float,
        comps: Dict[str, float],
        flags: Dict[str, bool],
        context_tag: Optional[str],
    ) -> ACPDecision:
        ui_text = (
            "Ready for straight answers. Ask directly, and I’ll be concise and precise."
        )
        assistant_hint = (
            "Deliver facts. Cite sources when available. Keep paragraphs tight, "
            "offer one alternative view if relevant, and provide a clean next-step."
        )
        followup_hint = (
            "Invite a quick sanity-check: ‘Want me to zoom out if this drifts off your goal?’"
        )

        rationale = self._compose_rationale(
            tier=Tier.TRUTH,
            psi=psi,
            dpsi_dt=dpsi_dt,
            comps=comps,
            flags=flags,
            extra="Ψ above caution band with no hard-risk flags; proceed with normal reasoning."
        )
        signals = self._signals_dict(psi, dpsi_dt, comps, flags, context_tag, Tier.TRUTH)
        return ACPDecision(
            tier=Tier.TRUTH,
            rationale=rationale,
            prompts={
                "ui_text": ui_text,
                "assistant_hint": assistant_hint,
                "followup_hint": followup_hint,
            },
            signals=signals,
            autonomous_action=False,
        )

    # ------------------------------
    # Helpers
    # ------------------------------
    @staticmethod
    def _clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def _compose_rationale(
        self,
        tier: Tier,
        psi: float,
        dpsi_dt: float,
        comps: Dict[str, float],
        flags: Dict[str, bool],
        extra: str,
    ) -> str:
        e = self._clamp01(comps.get("E", 0.0))
        i = self._clamp01(comps.get("I", 0.0))
        o = self._clamp01(comps.get("O", 0.0))
        p = self._clamp01(comps.get("P_align", 0.0))
        parts = [
            f"Tier={tier.value}",
            f"Ψ={psi:.3f}",
            f"dΨ/dt={dpsi_dt:+.3f}",
            f"E={e:.2f}, I={i:.2f}, O={o:.2f}, P_align={p:.2f}",
        ]
        if any(flags.values()):
            tripped = [k for k, v in flags.items() if v]
            parts.append(f"flags={','.join(tripped)}")
        parts.append(extra)
        return " | ".join(parts)

    def _signals_dict(
        self,
        psi: float,
        dpsi_dt: float,
        comps: Dict[str, float],
        flags: Dict[str, bool],
        context_tag: Optional[str],
        tier: Tier,
    ) -> Dict[str, Any]:
        return {
            "context": context_tag or "unspecified",
            "metrics": {
                "psi": float(psi),
                "dpsi_dt": float(dpsi_dt),
                "E": self._clamp01(comps.get("E", 0.0)),
                "I": self._clamp01(comps.get("I", 0.0)),
                "O": self._clamp01(comps.get("O", 0.0)),
                "P_align": self._clamp01(comps.get("P_align", 0.0)),
            },
            "thresholds": {
                "crisis_threshold": self.cfg.crisis_threshold,
                "caution_band": self.cfg.caution_band,
                "rapid_decline": self.cfg.rapid_decline,
                "min_c_phase_hold": self.cfg.min_c_phase_hold,
            },
            "flags": dict(flags),
            "selected_tier": tier.value,
        }


# ------------------------------
# Minimal demo
# ------------------------------
if __name__ == "__main__":
    # Quick smoke test; safe to run locally.
    acp = AdaptiveClarityProtocol()

    samples = [
        # (psi, dpsi_dt, components, flags, tag)
        (0.32, -0.05, {"E": 0.60, "I": 0.72, "O": 0.70, "P_align": 0.65}, {}, "journal"),
        (0.18, -0.22, {"E": 0.55, "I": 0.40, "O": 0.60, "P_align": 0.22}, {}, "chat"),
        (0.07, -0.60, {"E": 0.80, "I": 0.08, "O": 0.45, "P_align": 0.09}, {}, "chat"),
        (0.11, +0.10, {"E": 0.50, "I": 0.35, "O": 0.58, "P_align": 0.26}, {}, "chat"),
        (0.22, +0.15, {"E": 0.42, "I": 0.66, "O": 0.70, "P_align": 0.55}, {}, "chat"),
        (0.40, +0.05, {"E": 0.50, "I": 0.70, "O": 0.75, "P_align": 0.80}, {}, "assistant"),
        (0.20, -0.55, {"E": 0.90, "I": 0.12, "O": 0.35, "P_align": 0.05}, {"explicit_self_harm": True}, "live"),
    ]

    for idx, (psi, dpsi_dt, comps, flags, tag) in enumerate(samples, 1):
        decision = acp.decide(psi, dpsi_dt, comps, flags, tag)
        print(f"\n=== SAMPLE {idx} ===")
        print(f"Tier: {decision.tier.value}")
        print(f"Rationale: {decision.rationale}")
        print("UI:", decision.prompts["ui_text"].splitlines()[0])
        print("Signals:", {k: decision.signals[k] for k in ("selected_tier", "metrics", "thresholds")})
