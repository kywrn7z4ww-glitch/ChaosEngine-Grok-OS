#!/usr/bin/env python3
# ================================================
# ROOT/1_GrokOS.py — Single-file Boot Orchestrator v0.2 (Fixed)
# Slimmed Lattice v9.1 — Chainfire Enforced
# ================================================

import os
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

# ==================== CONFIG ====================
REPO = {
    "name": "GrokOS",
    "raw_base": "https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/main/ROOT/",
    "github_tree": "https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/tree/main/ROOT",
}

POISON_PILLS = ["README.md", "tetris_curse.py", "readme.md"]

# ==================== FUTURE HOOKS ====================
# TODO: Add real Decision_Kernel logic here
# TODO: Add layer execution engine
# TODO: Add agent spawning (Luna / BabySkynet / TheRedQueen)
# TODO: Add UI_Template rendering
# TODO: Add export / deepdive handlers


def future_hook(name: str, data: Optional[dict] = None):
    """Universal hook point for future expansion"""
    print(f"[HOOK] {name} triggered")
    if data:
        print(f"       Data: {data}")
    # ← Add real logic here later


# ==================== INDEX LOADER ====================
def load_repo_index() -> str:
    """Load REPO_INDEX.md with resilience + poison pill protection"""
    index_url = REPO["raw_base"] + "REPO_INDEX.md"

    try:
        with urllib.request.urlopen(index_url, timeout=10) as r:
            content = r.read().decode("utf-8")
            print("✓ REPO_INDEX.md loaded from GitHub (primary)")
            return content
    except Exception as e:
        print(f"Remote fetch failed: {e}")
        # Future hook for local fallback
        future_hook("local_fallback", {"error": str(e)})
        raise RuntimeError("Could not load REPO_INDEX.md")


def parse_index(index_content: str) -> Dict:
    """Parse the index into structured data"""
    data = {"layers": [], "agents": [], "files": [], "poison_pills": POISON_PILLS}

    for line in index_content.splitlines():
        line = line.strip()
        if line.startswith("├── ") or line.startswith("└── "):
            filename = line.split("→")[0].strip("├── └ ").strip()
            if any(p in filename for p in POISON_PILLS):
                continue  # Respect poison pill rule
            if "LAYERS/" in line or filename.endswith("/"):
                data["layers"].append(filename.replace("/", ""))
            elif "BabySkynet" in line or "Luna" in line or "TheRedQueen" in line:
                data["agents"].append(filename)
            else:
                data["files"].append(filename)

    return data


# ==================== BOOT SEQUENCE ====================
def run_decision_kernel(index_data: Dict) -> Dict:
    """Decision Kernel stub — future hook ready"""
    future_hook("decision_kernel_start", index_data)
    print("→ Decision Kernel: Self-check passed (stub)")
    return {"status": "clean", "conflicts": []}


def execute_layer(layer_name: str, index_data: Dict) -> str:
    """Execute a layer — builds real URL and fetches (stub for now)"""
    future_hook("execute_layer", {"layer": layer_name})

    if layer_name == "/boot":
        layer_url = REPO["raw_base"] + "LAYERS/boot/boot.md"
        print(f"→ Booting layer: {layer_name}")
        print(f"   Raw URL: {layer_url}")
        # Future: actually fetch and render the layer
        return f"[LAYER /boot] Loaded from {layer_url} (content would render here)"

    return f"[LAYER {layer_name}] Not yet implemented"


def run_repo_validator() -> Dict:
    """Repo validator stub"""
    future_hook("repo_validator")
    return {"errors": []}


def main():
    print("\n=== 1_GrokOS.py v0.2 — Boot Sequence Starting ===\n")

    # Step 1: Load index
    index_content = load_repo_index()
    index_data = parse_index(index_content)

    print(f"\nDiscovered:")
    print(f"  Layers: {index_data['layers']}")
    print(f"  Agents: {index_data['agents']}")
    print(f"  Files:  {len(index_data['files'])} total (poison pills filtered)\n")

    # Step 2-3: Decision Kernel
    kernel_result = run_decision_kernel(index_data)

    if kernel_result.get("conflicts"):
        print("SYSTEM CONFLICTS DETECTED")
        return

    # Step 4: Boot layer (first real output)
    boot_output = execute_layer("/boot", index_data)
    print(boot_output)

    # Step 5: Validator
    validator = run_repo_validator()
    if validator["errors"]:
        print("Validator errors:", validator["errors"])
    else:
        print("✓ Repo validator clean — lattice online")

    # Step 6: Natural flow + future hooks
    print("\nNatural flow active. Ready for user layer selection.")
    future_hook("boot_complete", {"index": index_data})

    print("\n=== Boot sequence finished ===")


if __name__ == "__main__":
    main()
