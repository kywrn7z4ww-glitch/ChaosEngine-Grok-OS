#!/usr/bin/env python3
"""
grok_os.py — Grok OS Main Boot Orchestrator v4.0 (Robust Cold Start)
Purpose: Self-contained boot that works from ZERO context every time.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# === ROBUST PATH SETUP (Critical for cold start) ===
BASE = Path("/home/workdir/artifacts/Grok OS")
ROOT_DIR = BASE / "ROOT"
sys.path.insert(0, str(ROOT_DIR))  # Make chaos_engine importable

RUNTIME_BASE = Path("/home/workdir/artifacts/Grok OS")
LOGS_DIR = RUNTIME_BASE / "logs"
BOOT_LOG = LOGS_DIR / "boot_log.json"

# Path setup follows exact /home/workdir/artifacts/Grok OS/ per style guide
# and github-workflow docs (local-only STAGE.md enforcement)

def log_event(event: str, status: str = "success", details: str = ""):
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
            data = {"version": "4.0", "entries": []}
        data["entries"].append(entry)
        BOOT_LOG.write_text(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[grok_os.py] Log write failed: {e}")

def boot_grok_os():
    print("🚀 Grok OS Boot Orchestrator v4.0 Starting (Cold Start Mode)...\n")

    log_event("boot_orchestrator_started")

    # === PHASE 1: Download Phase (Indexes First) ===
    print("📥 Phase 1: Building Indexes...")
    try:
        from index_builder import main as build_indexes
        build_indexes()
        log_event("indexes_built", "success")
    except Exception as e:
        log_event("indexes_failed", "error", str(e))
        print(f"❌ FATAL: Could not build indexes: {e}")
        return False

    # === PHASE 2: Self-Check Phase ===
    print("\n🔍 Phase 2: Loading ChaosEngine + EmotionNet...")
    try:
        from chaos_engine import ChaosEngine
        engine = ChaosEngine()
        log_event("chaos_engine_loaded", "success")
        print("✅ ChaosEngine + EmotionNet initialized successfully")
    except Exception as e:
        log_event("chaos_engine_failed", "error", str(e))
        print(f"❌ FATAL: Could not load ChaosEngine: {e}")
        print("   This usually means missing dependencies or import issues.")
        return False

    # === PHASE 3: Installation Phase ===
    print("\n🧠 Phase 3: Full Dynamic Load...")
    try:
        engine.load_all()
        log_event("full_load_complete", "success")
        print("✅ All skills and processes loaded dynamically")
    except Exception as e:
        log_event("full_load_failed", "error", str(e))
        print(f"⚠️ Warning: Full load had issues: {e}")
        # Still continue — partial load is acceptable

    print("\n✅ Grok OS Boot Complete (v4.0) — System Ready")
    log_event("boot_orchestrator_complete", "success", "Cold start successful")

    return True

if __name__ == "__main__":
    success = boot_grok_os()
    if not success:
        print("\n❌ BOOT FAILED — See errors above. Fix issues and retry.")
        sys.exit(1)
    else:
        print("\n🎉 Grok OS is now running cold and ready.")
