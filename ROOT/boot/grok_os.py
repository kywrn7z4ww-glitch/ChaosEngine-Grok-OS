#!/usr/bin/env python3
"""
grok-os.py — Grok OS Boot Logic v2.1 (Local-First + Dynamic)
Purpose: Dynamically discovers files, builds its own live index,
loads core components, and prepares the OS environment.
Local-first + simple freshness check.
"""

import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

# === CONFIG ===
REPO_OWNER = "kywrn7z4ww-glitch"
REPO_NAME = "ChaosEngine-Grok-OS"
BRANCH = "main"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/ROOT/"

LOCAL_ROOT = Path("/opt/grok-os/ROOT")
LOCAL_ROOT.mkdir(parents=True, exist_ok=True)

CACHE_DIR = Path("/opt/grok-os/.cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
INDEX_CACHE = CACHE_DIR / "live_index.json"

POISON_PILLS = ["readme.md", "tetris_curse.py"]


def is_poison(path: str) -> bool:
    return any(p in path.lower() for p in POISON_PILLS)


def fetch_file(rel_path: str) -> bool:
    if is_poison(rel_path):
        print(f"  ⚠️  Skipping poison: {rel_path}")
        return False

    url = RAW_BASE + rel_path
    local_path = LOCAL_ROOT / rel_path
    local_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            content = resp.read()
        local_path.write_bytes(content)
        print(f"  ✅ {rel_path}")
        return True
    except Exception as e:
        print(f"  ❌ {rel_path}: {e}")
        return False


def discover_tree() -> Set[str]:
    """Dynamically scan the entire ROOT/ tree via GitHub API"""
    print("\n=== Dynamic Discovery (Building Live Index) ===")
    try:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{BRANCH}?recursive=1"
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        files = set()
        for item in data.get("tree", []):
            if item["type"] == "blob" and item["path"].startswith("ROOT/"):
                rel = item["path"].replace("ROOT/", "", 1)
                if not is_poison(rel):
                    files.add(rel)

        print(f"  Discovered {len(files)} files")
        return files
    except Exception as e:
        print(f"  Discovery failed: {e}")
        return set()


def build_and_save_index(files: Set[str]):
    """Save discovered index for future boots"""
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


def should_refresh(local_path: Path, max_age_days: int = 7) -> bool:
    """Simple freshness check"""
    if not local_path.exists():
        return True
    age = datetime.now() - datetime.fromtimestamp(local_path.stat().st_mtime)
    return age.days > max_age_days


def kernel_panic(missing: List[str]):
    print("\n🚨 KERNEL PANIC — Critical Files Missing")
    for f in missing:
        print(f"  - {f}")
    print("\nPlease repair and restart. Type 'retry' to try again.")
    if input("> ").strip().lower() == "retry":
        return True
    exit(1)


def main():
    print("=== Grok OS Boot Logic v2.1 (Local-First + Dynamic) ===")

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
        exit(1)

    # Step 2: Load critical core files (local first, then remote if needed)
    critical = ["grok-os.md", "decision-kernel.md", "REPO_INDEX.md"]
    print("\n=== Loading Critical Core Files (Local-First) ===")
    for f in critical:
        local_path = LOCAL_ROOT / f
        if local_path.exists() and not should_refresh(local_path):
            print(f"  ♻️  Using local: {f}")
        elif f in files:
            fetch_file(f)
        else:
            print(f"  ⚠️  Critical file not found: {f}")

    # Step 3: Load remaining files (local first, refresh if old)
    print("\n=== Loading Remaining Files ===")
    loaded = 0
    refreshed = 0
    for f in sorted(files):
        if f not in critical:
            local_path = LOCAL_ROOT / f
            if local_path.exists() and not should_refresh(local_path):
                print(f"  ♻️  Using local: {f}")
            else:
                if fetch_file(f):
                    refreshed += 1
            loaded += 1
    print(f"  {loaded} files processed ({refreshed} refreshed from remote)")

    print("\n✅ Grok OS environment ready.")
    print("Next stage (ChaosEngine + EmotionNet) prepared for following turn.")
    print("=== Boot Complete ===")


if __name__ == "__main__":
    main()
