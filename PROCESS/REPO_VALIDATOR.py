import json
import os
from datetime import datetime

import requests

# Primary: REPO_INDEX.md + raw pulls
REPO_OWNER = "kywrn7z4ww-glitch"
REPO_NAME = "ChaosEngine-Grok-OS"
BRANCH = "main"
INDEX_PATH = "ROOT/REPO_INDEX.md"  # relative to repo root

POISON_PILLS = ["README.md", "readme.md", "tetris_curse.py"]


def get_latest_sha():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits/{BRANCH}"
    r = requests.get(url, timeout=8)
    r.raise_for_status()
    sha = r.json()["sha"]
    print(f"✅ Latest SHA (API): {sha[:12]}... ({datetime.now()})")
    return sha


def get_tree_files(sha):
    """GitHub API tree scan — fallback only"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{sha}?recursive=1"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    tree = r.json()["tree"]
    return [item["path"] for item in tree if item["type"] == "blob"]


def load_current_index():
    """Primary source — raw pull of REPO_INDEX.md"""
    url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{INDEX_PATH}"
    r = requests.get(url, timeout=8)
    r.raise_for_status()
    lines = r.text.strip().split("\n")
    indexed = [
        line.strip() for line in lines if line.strip() and not line.startswith("#")
    ]
    return set(indexed)


def run_validator():
    print("🔍 REPO_VALIDATOR.py — starting structural cross-check...")
    sha = get_latest_sha()
    current_index = load_current_index()

    # Primary check: compare vs REPO_INDEX.md
    try:
        tree_files = get_tree_files(sha)  # API fallback only if needed
    except:
        tree_files = []  # graceful fallback

    indexed_set = current_index
    actual_set = set(
        f
        for f in tree_files
        if f.startswith("ROOT/") or f.startswith("LAYERS/") or f.startswith("PROCESS/")
    )

    additions = actual_set - indexed_set
    deletions = indexed_set - actual_set
    poison_found = [f for f in actual_set if any(p in f for p in POISON_PILLS)]

    print("\n📊 VALIDATOR RESULTS")
    if additions:
        print(f"⚠️  Additions detected ({len(additions)}): {list(additions)[:5]}")
    if deletions:
        print(
            f"⚠️  Deletions / missing from index ({len(deletions)}): {list(deletions)[:5]}"
        )
    if poison_found:
        print(f"‼️  POISON PILL DETECTED: {poison_found}")
    if not additions and not deletions and not poison_found:
        print("✅ Structure matches REPO_INDEX.md — no drift")

    return {
        "sha": sha,
        "additions": list(additions),
        "deletions": list(deletions),
        "poison": poison_found,
        "clean": len(additions) == 0 and len(deletions) == 0 and len(poison_found) == 0,
    }


if __name__ == "__main__":
    run_validator()
