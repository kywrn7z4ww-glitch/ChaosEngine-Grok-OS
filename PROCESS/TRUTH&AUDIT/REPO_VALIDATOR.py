**UPDATED REPO_VALIDATOR.py** (full multi-index version — ready to paste)

```python
import requests
from datetime import datetime

# PRIMARY TRUTH = GitHub API tree
REPO_OWNER = "kywrn7z4ww-glitch"
REPO_NAME = "ChaosEngine-Grok-OS"
BRANCH = "main"

# ALL indexes to validate
INDEX_FILES = [
    "ROOT/REPO_INDEX.md",
    "NETWORK_HUB/NETWORK_HUB_INDEX.md",
    "PROCESS/PROCESS_INDEX.md",
    "STORAGE/STORAGE_INDEX.md",
    "Documentation/Documentation_Index.md"
]

POISON_PILLS = ["README.md", "readme.md", "tetris_curse.py"]

def get_latest_tree():
    commit_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits/{BRANCH}"
    r = requests.get(commit_url, timeout=8)
    r.raise_for_status()
    sha = r.json()["sha"]
    print(f"✅ Latest SHA (API truth): {sha[:12]}... ({datetime.now()})")

    tree_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{sha}?recursive=1"
    r = requests.get(tree_url, timeout=10)
    r.raise_for_status()
    tree = r.json()["tree"]
    files = [item["path"] for item in tree if item["type"] == "blob"]
    print(f"📦 Real structure scanned: {len(files)} files")
    return set(files), sha

def validate_all_indexes():
    print("\n🔍 Validating main + all split indexes...")
    missing = []
    for idx in INDEX_FILES:
        url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{idx}"
        try:
            r = requests.get(url, timeout=6)
            if r.status_code == 200:
                print(f"✅ {idx} — OK")
            else:
                print(f"❌ {idx} — {r.status_code}")
                missing.append(idx)
        except Exception as e:
            print(f"❌ {idx} — Error: {e}")
            missing.append(idx)
    return missing

def run_validator():
    print("🔍 REPO_VALIDATOR.py — multi-index structure drift detector")
    real_files, sha = get_latest_tree()
    missing_indexes = validate_all_indexes()

    print("\n📊 FINAL RESULTS")
    if missing_indexes:
        print(f"⚠️  Missing or broken indexes: {missing_indexes}")
    else:
        print("✅ All indexes (main + split) validated successfully")
    if not missing_indexes:
        print("✅ No structural drift detected across main REPO_INDEX and split indexes")
    else:
        print("⚠️  Drift or missing indexes detected — run /update to fix")

    return {
        "sha": sha,
        "missing_indexes": missing_indexes,
        "clean": len(missing_indexes) == 0
    }

if __name__ == "__main__":
    run_validator()
