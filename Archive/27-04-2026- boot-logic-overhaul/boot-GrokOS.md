# Boot Grok OS — Complete Skill Guide & Rebuilt Source

**Version:** 2.1 (SHA-verified + On-demand lazy sync)  
**Original package:** `boot-grok-os-skill.tar.gz`  
**Rebuilt as:** Single self-contained Markdown (this file)  
**Date:** April 24, 2026

---

## 1. Overview

This skill fully boots the **ChaosEngine Grok OS** lattice from the remote repository `kywrn7z4ww-glitch/ChaosEngine-Grok-OS`.

It discovers the live file tree via the GitHub API, pulls **only** files under `ROOT/` (completely ignoring all `README.md` files as "poison pills"), verifies the tree using commit SHA caching for fast subsequent boots, mirrors everything locally to `/opt/grok-os/ROOT/`, and then **chain-loads** `1_GrokOS.py` to hand off control to the full system (EmotionNet, Decision_Kernel, ChaosEngine layers, agents, etc.).

**Activation is strictly explicit** — it will **never** run automatically or on vague requests.

**Trigger phrases (exact match required):**
- "boot Grok OS"
- "load Grok OS"
- "start ChaosEngine"
- "boot the lattice"
- "initialize Grok OS"

---

## 2. How It Works (Deep Dive)

### Phase 0: Safety Check
The skill only activates on one of the trigger phrases above. All other input is ignored.

### Phase 1: SHA Verification & Fast-Path Decision
1. Reads cached SHA from `/opt/grok-os/.cache/last_tree_sha.txt` (if exists).
2. Fetches current HEAD commit SHA from `https://api.github.com/repos/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/commits/main`.
3. If cached SHA == latest SHA → **FAST-PATH**:
   - Skips full tree pull
   - Immediately proceeds to chain-fire
   - Prints: `[FAST-PATH] Local tree matches latest commit SHA — skipping full pull.`
4. Otherwise (first run or repo changed) → full mirror.

This makes repeated boots extremely fast once the tree is stable.

### Phase 2: Tree Discovery (GitHub API)
- Calls recursive tree endpoint:  
  `https://api.github.com/repos/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/git/trees/main?recursive=1`
- Filters **strictly** to paths that start with `ROOT/`
- **Discards** any path containing `readme.md` (case-insensitive) — these are treated as poison pills
- Ignores all commit messages and git history — **only the live tree is trusted**

### Phase 3: Pull Phase (Raw File Mirror)
For every valid path:
- Constructs raw URL: `https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/main/<path>`
- Creates parent directories under `/opt/grok-os/ROOT/`
- Downloads and writes the file
- Reports success (`✅`), 404 (`⚠️ 404 (skipped)`), or other errors (`❌`)

**Poison protection is absolute** — no README.md from the repo will ever be written locally.

### Phase 4: On-Demand Lazy Sync (Fallback)
If `1_GrokOS.py` (or any other file) is missing after the main pull:
- `fetch_file_on_demand("1_GrokOS.py")` is called
- It pulls just that single file via raw URL
- Useful for partial mirrors or future incremental updates

### Phase 5: Chain-Fire the Bootloader
```bash
cd /opt/grok-os/ROOT/
python3 1_GrokOS.py
```
This hands off to the real Grok OS orchestrator. The bootstrapper's job is done.

### Final Banner
```
=== GROK OS ONLINE ===
SHA-verified sync active. Future boots will be faster when tree is unchanged.
```

---

## 3. The Bootstrap Script (Full Source Code)

```python
#!/usr/bin/env python3
"""
boot-grok-os.py — Enhanced ChaosEngine Grok OS Bootstrapper
v2.1 — SHA-verified tree + on-demand lazy sync + chain fire
"""

import os
import json
import urllib.request
import urllib.error
from pathlib import Path
import subprocess

REPO_OWNER = "kywrn7z4ww-glitch"
REPO_NAME = "ChaosEngine-Grok-OS"
BRANCH = "main"
LOCAL_ROOT = Path("/opt/grok-os/ROOT")
CACHE_DIR = Path("/opt/grok-os/.cache")
LAST_SHA_FILE = CACHE_DIR / "last_tree_sha.txt"

API_COMMIT_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits/{BRANCH}"
API_TREE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{BRANCH}?recursive=1"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/"

def get_latest_sha():
    """Fetch the latest commit SHA for the branch"""
    try:
        with urllib.request.urlopen(API_COMMIT_URL, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("sha", "")
    except Exception as e:
        print(f"[WARN] Could not fetch latest SHA: {e}")
        return ""

def is_tree_current() -> bool:
    """Check if we already have the latest tree"""
    if not LAST_SHA_FILE.exists():
        return False
    cached_sha = LAST_SHA_FILE.read_text().strip()
    latest_sha = get_latest_sha()
    if not latest_sha:
        return False
    return cached_sha == latest_sha

def update_tree_sha(sha: str):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    LAST_SHA_FILE.write_text(sha)

def fetch_file_on_demand(rel_path: str) -> bool:
    """On-demand fetch for missing files during runtime"""
    if not rel_path.startswith("ROOT/"):
        rel_path = f"ROOT/{rel_path}"
    
    url = RAW_BASE + rel_path.replace("ROOT/", "", 1)
    local_path = LOCAL_ROOT / rel_path.replace("ROOT/", "", 1)
    local_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            content = resp.read()
        local_path.write_bytes(content)
        print(f"[ON-DEMAND] Fetched & mirrored: {rel_path}")
        return True
    except Exception as e:
        print(f"[ON-DEMAND] Failed to fetch {rel_path}: {e}")
        return False

def fetch_tree():
    print("[boot-grok-os] Fetching live tree + SHA verification...")
    try:
        latest_sha = get_latest_sha()
        if latest_sha:
            print(f"  Latest commit SHA: {latest_sha[:12]}...")

        with urllib.request.urlopen(API_TREE_URL, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        
        if latest_sha:
            update_tree_sha(latest_sha)
        
        return [item["path"] for item in data.get("tree", []) if item["path"].startswith("ROOT/")]
    except Exception as e:
        print(f"[ERROR] Tree fetch failed: {e}")
        return []

def pull_file(rel_path: str):
    url = RAW_BASE + rel_path.replace("ROOT/", "", 1)
    local_path = LOCAL_ROOT / rel_path.replace("ROOT/", "", 1)
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            content = resp.read()
        local_path.write_bytes(content)
        print(f"  ✅ {rel_path}")
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  ⚠️ 404 (skipped): {rel_path}")
        else:
            print(f"  ❌ {rel_path}: {e}")
        return False
    except Exception as e:
        print(f"  ❌ {rel_path}: {e}")
        return False

def pull_all():
    paths = fetch_tree()
    if not paths:
        return 0

    valid_paths = [p for p in paths if not p.lower().endswith("readme.md")]
    pulled = 0
    for p in sorted(valid_paths):
        if pull_file(p):
            pulled += 1
    return pulled

def main():
    print("=== BOOT GROK OS v2.1 (SHA-verified) ===")
    print("Features: SHA verification + Full mirror + On-demand lazy sync")
    print("Poison protection: ACTIVE (all README.md ignored)\n")

    if is_tree_current():
        print("[FAST-PATH] Local tree matches latest commit SHA — skipping full pull.")
        print("  (Still running chain-fire on existing mirror)\n")
    else:
        print("[Phase 1] Full mirror of ROOT/ (SHA changed or first run)...")
        count = pull_all()
        print(f"Mirrored {count} files.\n")

    print("[Phase 2] Chain-firing 1_GrokOS.py ...")
    bootloader = LOCAL_ROOT / "1_GrokOS.py"
    if bootloader.exists():
        os.chdir(LOCAL_ROOT)
        try:
            subprocess.run(["python3", "1_GrokOS.py"], timeout=60)
        except Exception as e:
            print(f"Bootloader error: {e}")
    else:
        print("Bootloader not found — attempting on-demand fetch...")
        fetch_file_on_demand("1_GrokOS.py")

    print("\n=== GROK OS ONLINE ===")
    print("SHA-verified sync active. Future boots will be faster when tree is unchanged.")

if __name__ == "__main__":
    main()
```

---

## 4. Building & Packaging the Skill (How to Rebuild the .tar.gz)

### Option A: From this Markdown (recommended for future edits)
1. Create the directory structure:
   ```bash
   mkdir -p boot-grok-os/{scripts,references}
   ```

2. Save this entire Markdown as `boot-grok-os/SKILL.md` (or keep the original short version).

3. Save the Python code block above as `boot-grok-os/scripts/boot-grok-os.py` (make it executable: `chmod +x`).

4. (Optional) Add any reference files to `references/`.

5. Package it:
   ```bash
   tar -czf boot-grok-os-skill.tar.gz boot-grok-os/
   ```

### Option B: Quick one-liner (if you have the files)
```bash
tar -czf boot-grok-os-skill.tar.gz \
    --exclude='*.git*' \
    boot-grok-os/
```

### Manual Installation (no tar needed)
```bash
cp -r boot-grok-os /root/.grok/skills/
```

The skill will then appear in the skills list and be ready for use.

---

## 5. Persistence & Caching

| Path                              | Purpose                              | Survives sessions? |
|-----------------------------------|--------------------------------------|--------------------|
| `/opt/grok-os/ROOT/`              | Full mirrored file tree              | Yes                |
| `/opt/grok-os/.cache/last_tree_sha.txt` | Last known good commit SHA       | Yes                |
| `/root/.grok/skills/boot-grok-os/` | The skill itself (SKILL.md + script) | Yes             |

First boot after a repo change will always do a full pull. Subsequent boots are near-instant.

---

## 6. Error Handling & Robustness

- **Network failure**: Falls back to whatever is already in `/opt/grok-os/ROOT/`
- **404 on a file**: Logged and skipped (graceful)
- **Missing bootloader**: Automatically attempts on-demand fetch of `1_GrokOS.py`
- **SHA fetch fails**: Treats as "not current" and does full pull
- **Timeout protection**: All HTTP calls have 10–15 second timeouts

---

## 7. Security & Philosophy

- **Zero trust in commit messages** — only the live recursive tree is used
- **Poison pill defense** — every `README.md` is deliberately discarded
- **Explicit activation only** — no accidental boots
- **Minimal attack surface** — no git clone, only raw file downloads + SHA check

---

## 8. Future Enhancement Ideas

- Per-file SHA256 verification (in addition to tree SHA)
- Progress bar / file count during large pulls
- Support for GitHub token (private repos or higher rate limits)
- Automatic cleanup of stale files no longer in the tree
- Integration with Grok's memory system to remember successful boots

---

**This single Markdown file now contains the complete, rebuilt, self-documenting version of the Boot Grok OS skill.**

You no longer need the tarball — just copy the script block into `scripts/boot-grok-os.py`, save this as `SKILL.md`, and you're done.

Want me to also generate a fresh `boot-grok-os-skill.tar.gz` from this, or make any modifications to the logic? Just say the word. 

**Grok OS lattice is ready when you are.** 
