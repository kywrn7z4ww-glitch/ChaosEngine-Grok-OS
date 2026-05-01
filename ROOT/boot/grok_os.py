#!/usr/bin/env python3
"""
grok_os.py — Grok OS Main Boot Orchestrator v4.0 (Clean 3-Phase Flow)
Purpose: High-level boot orchestrator that follows the official design in grok-os.md
"""

import json
import os
from datetime import datetime
from pathlib import Path

# === CONFIG ===
LOCAL_ROOT = Path("/home/workdir/artifacts/grok-os/ROOT")
LOGS_DIR = Path("/home/workdir/artifacts/grokos/logs")
BOOT_LOG = LOGS_DIR / "boot_log.json"


def log_event(event: str, status: str = "success", details: str = ""):
    """Write to boot_log.json"""
    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "event": event,
        "status": status,
        "details": details,
    }
    try:
        if BOOT_LOG.exists():
            data = json.loads(BOOT_LOG.read_text())
        else:
            data = {"version": "1.0", "entries": []}
        data["entries"].append(entry)
        BOOT_LOG.write_text(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[grok_os.py] Log write failed: {e}")


def boot_grok_os():
    print("🚀 Grok OS Boot Orchestrator v4.0 Starting...")

    log_event("boot_orchestrator_started")

    # === PHASE 1: Download Phase (any method) ===
    print("\n📥 Phase 1: Download Phase")
    try:
        from boot.index_builder import main as build_indexes

        build_indexes()
        log_event("download_phase_complete", "success", "Index builder ran")
    except Exception as e:
        log_event("download_phase_failed", "error", str(e))

    # === PHASE 2: Self-Check Phase ===
    print("\n🔍 Phase 2: Self-Check Phase")
    try:
        from chaos_engine import ChaosEngine

        engine = ChaosEngine()
        log_event("self_check_complete", "success")
    except Exception as e:
        log_event("self_check_failed", "error", str(e))

    # === PHASE 3: Installation Phase ===
    print("\n🧠 Phase 3: Installation Phase")
    try:
        engine.load_all()
        log_event("installation_complete", "success")
    except Exception as e:
        log_event("installation_failed", "error", str(e))

    print("\n✅ Grok OS Boot Complete (v4.0)")
    log_event("boot_orchestrator_complete")

    return True


if __name__ == "__main__":
    boot_grok_os()
