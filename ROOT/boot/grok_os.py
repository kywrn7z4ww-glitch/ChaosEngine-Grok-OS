#!/usr/bin/env python3
"""
grok-os.py — Grok OS Boot Logic v2.3 (Configurable + Offline-First)
Purpose: Dynamically discovers files with smart 3-tier fallback:
1. Local first (fastest, offline)
2. Connector (GitHub API + raw) — only if network available
3. Download skill (web browse fallback)

This version is designed for no-internet environments + future network module.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

# === CONFIG (now configurable) ===
REPO_OWNER = "kywrn7z4ww-glitch"
REPO_NAME = "ChaosEngine-Grok-OS"
BRANCH = "main"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/ROOT/"

# Use environment variable or default to artifacts path for this environment
LOCAL_ROOT = Path(os.getenv("GROKOS_ROOT", "/home/workdir/artifacts/grok-os/ROOT"))
LOCAL_ROOT.mkdir(parents=True, exist_ok=True)

CACHE_DIR = LOCAL_ROOT.parent / ".cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
INDEX_CACHE = CACHE_DIR / "live_index.json"

POISON_PILLS = ["readme.md", "tetris_curse.py"]


def is_poison(path: str) -> bool:
    return any(p in path.lower() for p in POISON_PILLS)


def should_refresh(local_path: Path, max_age_days: int = 7) -> bool:
    if not local_path.exists():
        return True
    age = datetime.now() - datetime.fromtimestamp(local_path.stat().st_mtime)
    return age.days > max_age_days


def kernel_panic(missing: List[str]):
    """Fun kernel panic with emoji (kept for personality)"""
    print("\n🚨 KERNEL PANIC — Critical Files Missing")
    for f in missing:
        print(f"  - {f}")
    print("\nPlease repair and restart. Type 'retry' to try again.")
    if input("> ").strip().lower() == "retry":
        return True
    exit(1)


def fetch_file_3tier(rel_path: str) -> bool:
    """
    3-Tier Fallback System:
    Tier 1: Local (fastest, offline)
    Tier 2: Connector (GitHub raw) — only attempted if network might be available
    Tier 3: Download skill (web browse fallback)
    """
    local_path = LOCAL_ROOT / rel_path

    # === TIER 1: LOCAL FIRST (always preferred) ===
    if local_path.exists() and not should_refresh(local_path):
        print(f"  ♻️  Using local: {rel_path}")
        return True

    # === TIER 2: CONNECTOR (only if we think network might work) ===
    # In this environment we skip direct urllib to avoid long timeouts
    # The download skill (Tier 3) is the reliable path
    print(f"  ⚠️  Skipping direct connector for {rel_path} (offline mode)")

    # === TIER 3: DOWNLOAD SKILL (web browse fallback) ===
    print(f"  📥 Tier 3: Download skill recommended for {rel_path}")
    return False


def discover_tree() -> Set[str]:
    """Dynamically scan the entire ROOT/ tree via GitHub API (skipped in offline)"""
    print("\n=== Dynamic Discovery (Building Live Index) ===")
    print(
        "  ⚠️  Network discovery skipped (offline mode) — using cached index if available"
    )
    return set()


def build_and_save_index(files: Set[str]):
    index_data = {
        "timestamp": datetime.now().isoformat(),
        "file_count": len(files),
        "files": sorted(list(files)),
    }
    INDEX_CACHE.write_text(json.dumps(index_data, indent=2))
    print(f"  ✅ Live index saved ({len(files)} files)")


def load_cached_index() -> Set[str]:
    if INDEX_CACHE.exists():
        try:
            data = json.loads(INDEX_CACHE.read_text())
            return set(data.get("files", []))
        except:
            pass
    return set()


def main():
    print("=== Grok OS Boot Logic v2.3 (Configurable + Offline-First) ===")
    print(f"Using LOCAL_ROOT: {LOCAL_ROOT}")

    # Step 1: Try cached index first
    cached = load_cached_index()
    if cached:
        print(f"Using cached index ({len(cached)} files)")
        files = cached
    else:
        files = discover_tree()
        if files:
            build_and_save_index(files)

    if not files:
        print("❌ No files discovered. Cannot continue.")
        return

    # Step 2: Load all files using 3-tier system
    print("\n=== Loading Files (3-Tier System) ===")
    loaded = 0
    for f in sorted(files):
        if fetch_file_3tier(f):
            loaded += 1

    print(f"\n✅ {loaded}/{len(files)} files processed")
    print("=== Boot Complete ===")


if __name__ == "__main__":
    main()
