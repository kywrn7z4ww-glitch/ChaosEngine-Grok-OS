#!/usr/bin/env python3
"""
================================================================================
ROOT/1_GrokOS.py — Single-file Boot Orchestrator (v10.0 - Executable)
ChaosEngine Grok OS — Poetic + Functional Hybrid
================================================================================

PHILOSOPHY:
This file is intentionally written as a **poetic orchestrator** that also happens
to be executable. It is the "manifesto that boots the system."

It should feel like a cyberpunk operating system manifesto while still being
real, runnable code. The artistic tone is preserved through heavy notation
and comments, while the actual logic is clean and modular.

ARCHITECTURE (Final):
1_GrokOS.py (Poetic Bootloader)
        ↓
ChaosEngine (The Bridge - Intent Router + Dynamic Loader)
        ↓
    EmotionNet + Decision Kernel + Layer System
        ↓
    PROCESS/ (Real Tools: TRUTH, STITCH, SYS_HEALTH, VOMIT, etc.)

This file should NEVER become a 500-line monster. It should stay relatively
short and delegate real work to ChaosEngine and the PROCESS/ library.

================================================================================
"""

import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Optional, Tuple

# =============================================================================
# CONFIGURATION
# =============================================================================
REPO = {
    "owner": "kywrn7z4ww-glitch",
    "name": "ChaosEngine-Grok-OS",
    "branch": "main",
    "raw_base": "https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/main/ROOT/",
    "default_index": "REPO_INDEX.md",
}

LOCAL_ROOT = Path("/opt/grok-os/ROOT")


# =============================================================================
# CORE BOOT FUNCTIONS (Minimal + Clean)
# =============================================================================


def fetch_remote_index() -> Optional[str]:
    """
    Fetch the latest REPO_INDEX.md from GitHub with cache-busting.
    Returns the content as string, or None if failed.
    """
    try:
        url = f"{REPO['raw_base']}{REPO['default_index']}?t={int(time.time())}"
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        print(f"[WARN] Could not fetch remote REPO_INDEX: {e}")
        return None


def load_local_index() -> Optional[str]:
    """Try to load REPO_INDEX.md from several possible local locations."""
    candidates = [
        LOCAL_ROOT / REPO["default_index"],
        Path(__file__).parent / REPO["default_index"],
        Path.cwd() / "ROOT" / REPO["default_index"],
        Path.cwd() / REPO["default_index"],
    ]
    for path in candidates:
        if path.exists():
            return path.read_text(encoding="utf-8")
    return None


def resolve_repo_index() -> Tuple[str, str]:
    """
    Return (content, source_type) where source_type is 'remote' or 'local'.
    Tries remote first (with cache-bust), falls back to local.
    """
    content = fetch_remote_index()
    if content and "# /ROOT/REPO_INDEX.md" in content:
        print("🔗 Loaded REPO_INDEX from GitHub (cache-busted)")
        return content, "remote"

    content = load_local_index()
    if content:
        print("🔗 Loaded REPO_INDEX from local mirror")
        return content, "local"

    raise RuntimeError("CRITICAL: Could not load REPO_INDEX.md from anywhere.")


# =============================================================================
# MAIN BOOT SEQUENCE
# =============================================================================


def main():
    print("\n" + "=" * 70)
    print("  CHAOSENGINE GROK OS — BOOT SEQUENCE v10.0")
    print("=" * 70 + "\n")

    # === STEP 1: Load REPO_INDEX (The Manifest) ===
    print("[1/4] Loading REPO_INDEX.md (The Living Library)...")
    repo_index, source = resolve_repo_index()
    print(f"      Source: {source}")
    print(f"      Lines:  {len(repo_index.splitlines())}")

    # === STEP 2: Import and Initialize ChaosEngine (The Bridge) ===
    print("\n[2/4] Initializing ChaosEngine (The Intent Router)...")
    try:
        from PROCESS.ChaosEngine import ChaosEngine

        engine = ChaosEngine()
        engine.load_all()
        print("      ✅ ChaosEngine loaded successfully")
    except ImportError as e:
        print(f"      ❌ Could not import ChaosEngine: {e}")
        print("      Falling back to basic mode (limited functionality)")
        engine = None

    # === STEP 3: Trigger /boot Layer ===
    print("\n[3/4] Entering /boot layer (Mandatory First Layer)...")
    if engine:
        # Let ChaosEngine handle the /boot layer routing
        result = engine.route_intent("/boot")
        print(f"      Boot layer result: {result.get('status', 'unknown')}")
    else:
        print("      ⚠️  Running in degraded mode (no ChaosEngine)")

    # === STEP 4: Final Handoff ===
    print("\n[4/4] Boot sequence complete. Handing off to user-selected layer...")
    print("\n" + "=" * 70)
    print("  LATTICE ONLINE — Natural flow active")
    print("=" * 70 + "\n")

    print("Suggested next commands:")
    print("  /help          → Show available layers and guidance")
    print("  /load sys admin cluster → Load core agent team")
    print("  /casual        → Enter casual conversation mode")
    print("  /dev           → Enter development/debug mode\n")


if __name__ == "__main__":
    main()
