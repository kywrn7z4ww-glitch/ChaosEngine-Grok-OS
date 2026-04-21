#!/usr/bin/env python3
# ================================================
# ROOT/1_GrokOS.py — Full Chain v0.6
# WITH GROK NAVIGATION GUIDE
# ================================================

"""
GROK NAVIGATION GUIDE (Read this first)
=======================================
This repo is a living, chaotic, evolving system. Rules:

1. ALWAYS load REPO_INDEX.md first — it contains the current truth + poison pill list.
2. Commit messages are unreliable. Always verify via API tree + raw files.
3. Poison pills exist (README.md, tetris_curse.py, etc.). Never load them.
4. Core is sovereign on boot. Respect his GitHub Lattice Sync rules.
5. The real logic lives in:
   - Decision_Kernel.md
   - LAYERS/ (especially boot/)
   - 2_EmotionNet.py
   - 3_ChaosEngine.py
   - STORAGE/AGENTS/ (dynamic loading via AGENT_LOADER.py if present)
6. Never assume structure is stable — always re-scan the tree on boot.
7. Future hooks are everywhere. Use them.

If something breaks, re-run the API tree scan first.
"""

import json
import urllib.request
from typing import Dict, List, Optional

REPO = {
    "owner": "kywrn7z4ww-glitch",
    "name": "ChaosEngine-Grok-OS",
    "raw_base": "https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/main/ROOT/",
}

POISON_PILLS = [
    "README.md",
    "tetris_curse.py",
    "readme.md",
]  # Will be overwritten by index


def future_hook(name: str, data: Optional[dict] = None):
    print(f"[HOOK] {name} triggered")
    if data:
        print(f"       → {data}")


def load_file(path: str) -> str:
    url = REPO["raw_base"] + path
    with urllib.request.urlopen(url, timeout=10) as r:
        return r.read().decode("utf-8")


def load_repo_index() -> str:
    print("\n=== Loading REPO_INDEX.md (Source of Truth) ===")
    return load_file("REPO_INDEX.md")


def parse_poison_pill_rules(index_content: str) -> List[str]:
    """Extract poison pill rules from the index"""
    pills = []
    for line in index_content.splitlines():
        if "POISON PILL" in line.upper() or "ignore" in line.lower():
            if "README" in line or "tetris" in line.lower():
                pills.append(line.strip())
    return pills


def scan_api_tree():
    print("\n=== API Tree Scan ===")
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
    print("=== 1_GrokOS.py v0.5 — Index First + Full Chain ===\n")

    # 1. Load index FIRST (so we know the rules)
    index = load_repo_index()
    poison_rules = parse_poison_pill_rules(index)
    print(f"✓ Poison pill rules loaded: {len(poison_rules)} rules recognized")

    # 2. API scan (with unreliable commit warning)
    scan_api_tree()

    # 3. Decision Kernel
    kernel = run_decision_kernel()

    # 4. /boot Layer
    execute_boot_layer()

    # 5. Fire up main systems
    fire_up_chaosengine()
    fire_up_emotionnet()

    print("\n✓ Full boot complete. CE + EmotionNet online.")
    future_hook("system_fully_live")


if __name__ == "__main__":
    main()
