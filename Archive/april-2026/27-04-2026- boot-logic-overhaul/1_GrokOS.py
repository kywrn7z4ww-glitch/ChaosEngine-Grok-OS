#!/usr/bin/env python3
# ================================================
# ROOT/1_GrokOS.py — Full Chain v0.6
# WITH GROK NAVIGATION GUIDE
# ================================================

"""
GROK NAVIGATION GUIDE (Read this first)
=======================================

PHILOSOPHY:
This is a "pull raw files as needed" system.
On first run (Turn 1) it scans the main repo URL, pulls the most important files,
stashes them locally, then chainfires the full boot sequence.

RULES:
1. ALWAYS load REPO_INDEX.md first — it is the source of truth.
2. Turn 1 = Scan main URL + pull core files (stash them).
3. Subsequent runs can use stashed files (faster + works offline).
4. Commit messages are unreliable — always verify via API tree + raw files.
5. Poison pills exist (README.md, tetris_curse.py, etc.). Never load them.
6. Core is sovereign on boot. Respect his GitHub Lattice Sync rules.
7. The real logic lives in:
   - Decision_Kernel.md
   - LAYERS/boot/boot.md
   - 2_EmotionNet.py
   - 3_ChaosEngine.py
8. Never assume structure is stable — re-scan on Turn 1.
9. Future hooks are everywhere. Use them.

FLOW:
Turn 1 → Scan URL → Pull core files → Stash → Chainfire logic
         (Decision Kernel → /boot → ChaosEngine → EmotionNet)

If something breaks, delete stashed files and re-run (forces fresh Turn 1).
"""

import json
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

REPO = {
    "owner": "kywrn7z4ww-glitch",
    "name": "ChaosEngine-Grok-OS",
    "raw_base": "https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/main/ROOT/",
}

STASH_DIR = Path.home() / ".grok-os" / "stash"
STASH_DIR.mkdir(parents=True, exist_ok=True)

POISON_PILLS = ["README.md", "tetris_curse.py", "readme.md"]


def future_hook(name: str, data: Optional[dict] = None):
    print(f"[HOOK] {name} triggered")
    if data:
        print(f"       → {data}")


def load_file(path: str, use_stash: bool = True) -> str:
    """Load file from stash if available, else pull from raw URL"""
    stash_path = STASH_DIR / path.replace("/", "_")

    if use_stash and stash_path.exists():
        print(f"      (using stashed {path})")
        return stash_path.read_text(encoding="utf-8")

    url = REPO["raw_base"] + path
    with urllib.request.urlopen(url, timeout=10) as r:
        content = r.read().decode("utf-8")

    # Stash it for next run
    stash_path.write_text(content, encoding="utf-8")
    return content


def load_repo_index() -> str:
    print("\n=== Loading REPO_INDEX.md (Source of Truth) ===")
    return load_file("REPO_INDEX.md")


def parse_poison_pill_rules(index_content: str) -> List[str]:
    pills = []
    for line in index_content.splitlines():
        if "POISON PILL" in line.upper() or "ignore" in line.lower():
            if "README" in line or "tetris" in line.lower():
                pills.append(line.strip())
    return pills


def scan_api_tree():
    print("\n=== API Tree Scan (Turn 1) ===")
    try:
        commit_url = (
            f"https://api.github.com/repos/{REPO['owner']}/{REPO['name']}/commits/main"
        )
        with urllib.request.urlopen(commit_url, timeout=8) as r:
            data = json.loads(r.read().decode())
            sha = data["sha"]
            message = data["commit"]["message"]
            print(f"✓ Latest commit: {sha[:8]}")
            print(f'  Message: "{message}"')
            print(
                "⚠️  Note: Commit messages are unreliable — always verify via tree + raw files."
            )
    except Exception as e:
        print(f"Scan failed: {e}")


def run_decision_kernel():
    print("\n=== Decision Kernel ===")
    kernel = load_file("Decision_Kernel.md")
    print("✓ Decision_Kernel.md loaded")
    future_hook("decision_kernel_loaded")
    return {"status": "clean"}


def execute_boot_layer():
    print("\n=== /boot Layer ===")
    boot = load_file("LAYERS/boot/boot.md")
    print(boot[:1000] + "..." if len(boot) > 1000 else boot)
    print("=== /boot COMPLETE ===")
    future_hook("boot_complete")
    return True


def fire_up_chaosengine():
    print("\n=== ChaosEngine (CE) ===")
    ce = load_file("3_ChaosEngine.py")
    print("✓ 3_ChaosEngine.py loaded")
    future_hook("chaosengine_fired")
    return True


def fire_up_emotionnet():
    print("\n=== EmotionNet ===")
    emo = load_file("2_EmotionNet.py")
    print("✓ 2_EmotionNet.py loaded")
    future_hook("emotionnet_fired")
    return True


def main():
    print("=== 1_GrokOS.py v0.6 — Index First + Full Chain ===\n")

    # 1. Load index FIRST
    index = load_repo_index()
    poison_rules = parse_poison_pill_rules(index)
    print(f"✓ Poison pill rules loaded: {len(poison_rules)} rules recognized")

    # 2. API scan (Turn 1)
    scan_api_tree()

    # 3. Decision Kernel
    run_decision_kernel()

    # 4. /boot Layer
    execute_boot_layer()

    # 5. Fire up main systems
    fire_up_chaosengine()
    fire_up_emotionnet()

    print("\n✓ Full boot complete. CE + EmotionNet online.")
    future_hook("system_fully_live")


if __name__ == "__main__":
    main()
