import json
from datetime import datetime

import requests

# PRIMARY TRUTH = GitHub API tree (real current structure)
# REFERENCE ONLY = REPO_INDEX.md (for diff detection on huge changes)
REPO_OWNER = "kywrn7z4ww-glitch"
REPO_NAME = "ChaosEngine-Grok-OS"
BRANCH = "main"

POISON_PILLS = ["README.md", "readme.md", "tetris_curse.py"]


def get_latest_tree():
    """Primary source: GitHub API recursive tree (structure-only)"""
    # Get latest SHA
    commit_url = (
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits/{BRANCH}"
    )
    r = requests.get(commit_url, timeout=8)
    r.raise_for_status()
    sha = r.json()["sha"]
    print(f"✅ Latest SHA (API truth): {sha[:12]}... ({datetime.now()})")

    # Get full tree
    tree_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{sha}?recursive=1"
    r = requests.get(tree_url, timeout=10)
    r.raise_for_status()
    tree = r.json()["tree"]
    files = [item["path"] for item in tree if item["type"] == "blob"]
    print(f"📦 Real structure scanned: {len(files)} files")
    return set(files), sha


def load_index_reference():
    """Reference only — parse REPO_INDEX.md for comparison"""
    url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/ROOT/REPO_INDEX.md"
    r = requests.get(url, timeout=8)
    r.raise_for_status()
    lines = r.text.strip().split("\n")
    indexed = set()
    for line in lines:
        line = line.strip()
        if line.startswith("- ") and not line.startswith("#"):
            # Extract path (e.g. ROOT/LAYERS/boot/boot.md)
            path = line.split("→")[0].strip().replace("- ", "").strip()
            if path:
                indexed.add(path)
    print(f"📋 REPO_INDEX reference loaded: {len(indexed)} entries")
    return indexed


def run_validator():
    print("🔍 REPO_VALIDATOR.py — structure drift detector (API tree = TRUTH)")
    real_files, sha = get_latest_tree()
    index_ref = load_index_reference()

    # Detect differences
    additions = real_files - index_ref
    deletions = index_ref - real_files
    poison_found = [
        f for f in real_files if any(p.lower() in f.lower() for p in POISON_PILLS)
    ]

    print("\n📊 DRIFT REPORT (big structure changes)")
    if additions:
        print(
            f"⚠️  ADDITIONS (new files/folders): {len(additions)} → {list(additions)[:10]}"
        )
    if deletions:
        print(
            f"⚠️  DELETIONS / missing from index: {len(deletions)} → {list(deletions)[:10]}"
        )
    if poison_found:
        print(f"‼️  POISON PILL DETECTED: {poison_found}")
    if not additions and not deletions and not poison_found:
        print("✅ No structural drift — index matches live tree")

    return {
        "sha": sha,
        "additions": list(additions),
        "deletions": list(deletions),
        "poison": poison_found,
        "clean": len(additions) == 0 and len(deletions) == 0 and len(poison_found) == 0,
    }


if __name__ == "__main__":
    run_validator()
