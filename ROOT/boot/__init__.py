"""
boot/__init__.py — Grok OS Traditional Boot v4.0 (Clean + Stable)

Follows traditional logic from grok_os.py + boot.md + grok-os.md
No blind recursion. Clean handoff to ChaosEngine.
"""

import os
from datetime import datetime
from pathlib import Path

# === CONFIG ===
LOCAL_ROOT = Path(os.getenv("GROKOS_ROOT", "/home/workdir/artifacts/grok-os/ROOT"))
BOOT_LOG = Path("/home/workdir/artifacts/grokos/Boot_Log.json")


def log_event(event: str, status: str = "success", details: str = ""):
    """Simple log writer for Boot_Log.json"""
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] {event} | {status} | {details}\n"
    try:
        with open(BOOT_LOG, "a") as f:
            f.write(entry)
    except:
        pass  # fail silently during boot


def boot_grok_os():
    print("🚀 Grok OS Traditional Boot v4.0 Starting...")

    log_event("boot_started")

    # === PHASE 1: Download Skill + Core Mirror ===
    print("\n📥 Phase 1: Download Skill + Core Mirror")
    try:
        from grok_download import sync_github_folder

        sync_github_folder(
            "https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/tree/main/ROOT",
            str(LOCAL_ROOT),
            profile="grok-os",
        )
        print("  ✅ Core mirror complete")
        log_event("core_mirror_complete")
    except Exception as e:
        print(f"  ⚠️  Download skill not available or failed: {e}")
        log_event("core_mirror_failed", "warning", str(e))

    # === PHASE 2: Load Core Components ===
    print("\n🔧 Phase 2: Load Core Components")
    core_files = [
        "grok-download.md",
        "grok-os.md",
        "decision-kernel.md",
        "UI_Template.md",
        "layers/boot/boot.md",
    ]

    loaded = []
    for filename in core_files:
        filepath = LOCAL_ROOT / filename
        if filepath.exists():
            print(f"  ✅ Loaded: {filename}")
            loaded.append(filename)
        else:
            print(f"  ⚠️  Missing: {filename}")

    log_event("core_components_loaded", "success", f"{len(loaded)} files")

    # === PHASE 3: Handoff to ChaosEngine + /boot layer ===
    print("\n🧠 Phase 3: Handoff to ChaosEngine + /boot layer")
    try:
        from chaos_engine import chaos_engine

        chaos_engine.load_all()
        print("  ✅ ChaosEngine initialized")
        log_event("chaosengine_initialized")
    except Exception as e:
        print(f"  ⚠️  ChaosEngine load failed: {e}")
        log_event("chaosengine_failed", "error", str(e))

    print("\n✅ Grok OS Traditional Boot Complete")
    log_event("boot_complete")

    return loaded


if __name__ == "__main__":
    boot_grok_os()
