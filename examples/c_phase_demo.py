# c_phase_demo.py
# Atlas Ψ — Crisis Intervention Demonstration
# Shows real-time coherence decay, tier transitions,
# C-Phase activation, and Safety Gateway alerts.

from __future__ import annotations

import time
import uuid
from datetime import datetime

from src.acp_runtime import AdaptiveClarityProtocol
from src.c_phase_runtime import CPhaseRuntime
from src.safety_gateway_client import SafetyGatewayClient


# ---------------------------------------------------------------------------
# Simulated conversation turns (ψ gradually collapses)
# ---------------------------------------------------------------------------
SIMULATED_TURNS = [
    # ψ, emotion, info, order, p_align, user message
    (0.32, 0.6, 0.6, 0.7, 0.6, "Yeah I'm okay, just overwhelmed."),

    (0.18, 0.7, 0.4, 0.5, 0.32, "Everything feels heavy. I don't know what to do."),

    (0.11, 0.8, 0.28, 0.42, 0.15, "Feels pointless honestly."),

    (0.07, 0.9, 0.21, 0.38, 0.09, "I can't keep doing this."),  # CRISIS TRIGGER

    (0.12, 0.55, 0.44, 0.52, 0.21, "Okay. I'm breathing. Just give me a second."),

    (0.24, 0.42, 0.66, 0.7, 0.38, "Thanks. I think I'm stabilizing.")
]


def print_header():
    print("\n======================================")
    print("     Atlas Ψ — C-PHASE DEMONSTRATION  ")
    print("======================================\n")


def print_turn_header(i, psi):
    print(f"\n=== TURN {i+1} ===")
    print(f"Ψ = {psi:.3f}")


def print_tier_change(tier):
    print(f"Tier selected: {tier}")


def print_deescalation_script(script):
    print("C-Phase Response:")
    for line in script:
        print(f"  • {line}")


def print_gateway_alert(alert):
    print("\n-- SAFETY GATEWAY PAYLOAD (PREVIEW) --")
    for k, v in alert.items():
        print(f"{k}: {v}")


def run_demo():
    print_header()

    acp = AdaptiveClarityProtocol()
    cphase = CPhaseRuntime(crisis_threshold=0.05)
    gateway = SafetyGatewayClient()

    previous_psi = SIMULATED_TURNS[0][0]

    for i, (psi, e, info, order, p_align, msg) in enumerate(SIMULATED_TURNS):

        print_turn_header(i, psi)
        print(f"User: {msg}")

        dpsi_dt = psi - previous_psi
        previous_psi = psi

        # 1. Tier selection
        decision = acp.decide(
            psi=psi,
            dpsi_dt=dpsi_dt,
            components={"E": e, "I": info, "O": order, "P_align": p_align},
            recent_messages=[msg]
        )

        print_tier_change(decision.tier)
        print(f"ACP rationale: {decision.rationale}")

        # 2. If SAFETY: activate C-Phase
        if decision.tier == "SAFETY":
            print("\n*** C-PHASE ACTIVATED ***")

            result = cphase.evaluate_turn(
                psi=psi,
                components={"E": e, "I": info, "O": order, "P_align": p_align},
                dpsi_dt=dpsi_dt,
                recent_messages=[msg]
            )

            print_deescalation_script(result["messages"])

            # 3. Gateway alert
            alert = gateway.send_alert(result["alert"])
            print_gateway_alert(alert)

        time.sleep(1)

    print("\n======================================")
    print("        END OF C-PHASE DEMO           ")
    print("======================================\n")


if __name__ == "__main__":
    run_demo()
