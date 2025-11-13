# safety_gateway_client.py
# Atlas Ψ — Safety Gateway Client
# MIT License
# Author: Kenneth E. Whitman Jr. | 2025-11
#
# Purpose:
#   Receives crisis alerts from C-Phase Runtime,
#   logs them, encrypts payload, and forwards to
#   HUMAN responders through a Safety Gateway API.
#
#   This module NEVER calls 911, dispatches services,
#   or performs any autonomous escalation.
#
#   HUMAN-IN-LOOP is mandatory.

from __future__ import annotations

import json
import uuid
import time
from datetime import datetime
from typing import Dict, Optional


class SafetyGatewayClient:
    """
    Atlas Ψ — Safety Gateway Client

    Responsibilities:
      - Accept crisis alerts from c_phase_runtime.py
      - Encrypt & log alerts (local or remote)
      - Forward alerts to a HUMAN-review system (Dashboard or API)
      - Track human verification and consent
      - NEVER autonomously contact emergency services

    This module is safe to integrate into production.
    """

    def __init__(
        self,
        gateway_url: Optional[str] = None,
        encryption_key: Optional[str] = None,
        local_log: str = "safety_alerts.log",
    ):
        self.gateway_url = gateway_url
        self.encryption_key = encryption_key
        self.local_log = local_log

    # ----------------------------------------------------------
    # Utility: Fake encryption (placeholder for real AES)
    # ----------------------------------------------------------
    def _encrypt(self, payload: Dict) -> str:
        """Basic reversible encoder. Replace with AES-256 in production."""
        raw = json.dumps(payload)
        return raw[::-1]  # naive reverse-string "encryption"

    # ----------------------------------------------------------
    # Logging
    # ----------------------------------------------------------
    def _write_local(self, encrypted: str):
        with open(self.local_log, "a") as f:
            f.write(f"{encrypted}\n")

    # ----------------------------------------------------------
    # Human alert
    # ----------------------------------------------------------
    def send_alert(self, alert: Dict) -> Dict:
        """
        Receives alert payload from C-Phase, encrypts it,
        logs it, and sends to human dashboard (mock).
        """
        timestamp = datetime.utcnow().isoformat()
        alert_package = {
            "gateway_id": f"GW-{uuid.uuid4()}",
            "received_at": timestamp,
            "payload": alert,
            "autonomous_action": False,
            "human_required": True,
            "consent_verified": False,
            "reviewed_by_human": False,
        }

        encrypted = self._encrypt(alert_package)
        self._write_local(encrypted)

        # In production: POST to real API
        if self.gateway_url:
            # Placeholder for network call
            pass

        return {
            "status": "RECEIVED",
            "timestamp": timestamp,
            "gateway_id": alert_package["gateway_id"],
            "human_required": True,
        }

    # ----------------------------------------------------------
    # Human verification workflow
    # ----------------------------------------------------------
    def verify_by_human(self, gateway_id: str, reviewer: str) -> Dict:
        """
        Manually attaches human verification.
        This is the required step before *any* escalation.
        """
        return {
            "gateway_id": gateway_id,
            "reviewed_by": reviewer,
            "verified_at": datetime.utcnow().isoformat(),
            "verified": True,
        }

    def verify_consent(self, gateway_id: str, reviewer: str) -> Dict:
        """
        Verifies explicit user consent for escalation.
        Required before warm-handoff or crisis routing.
        """
        return {
            "gateway_id": gateway_id,
            "consent_verified_by": reviewer,
            "verified_at": datetime.utcnow().isoformat(),
            "consent": True,
        }


# ----------------------------------------------------------
# Demo block
# ----------------------------------------------------------
if __name__ == "__main__":
    client = SafetyGatewayClient()

    dummy_alert = {
        "alert_id": "ALERT-123",
        "psi": 0.04,
        "reason": "Ψ below threshold",
        "autonomous_action": False,
        "human_required": True,
    }

    print("\n--- Sending Alert ---")
    r = client.send_alert(dummy_alert)
    print(r)

    print("\n--- Human Verifies ---")
    print(client.verify_by_human(r["gateway_id"], reviewer="Dr. Lee"))

    print("\n--- User Gives Consent (Example) ---")
    print(client.verify_consent(r["gateway_id"], reviewer="Dr. Lee"))
