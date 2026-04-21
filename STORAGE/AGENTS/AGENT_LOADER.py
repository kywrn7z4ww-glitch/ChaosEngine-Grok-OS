#!/usr/bin/env python3
"""
================================================================================
STORAGE/AGENTS/AGENT_LOADER.py — Dynamic Agent Discovery & Loading System
ChaosEngine Grok OS — v1.0
================================================================================

PURPOSE:
This module is the single source of truth for discovering and loading all agents
in the STORAGE/AGENTS/ folder (including all subfolders).

It is designed to be:
- Fully dynamic (no hard-coded agent lists)
- Easy to extend later (can load .py versions when ready)
- Clean and lightweight

USAGE:
    from STORAGE.AGENTS.AGENT_LOADER import load_agent, list_all_agents

    agent_content = load_agent("BabySkynet")
    all_agents = list_all_agents()

FUTURE UPGRADES:
- When you're ready, add support for loading .py versions instead of .md
- Example: if BabySkynet.py exists, load that instead of BabySkynet.md

================================================================================
"""

import os
from pathlib import Path
from typing import List, Optional

AGENTS_DIR = Path("STORAGE/AGENTS")


def _find_agent_file(name: str) -> Optional[Path]:
    """
    Search for an agent file (case-insensitive) in AGENTS_DIR and all subfolders.
    Returns the Path if found, otherwise None.
    """
    name_lower = name.lower()
    for root, dirs, files in os.walk(AGENTS_DIR):
        for file in files:
            if file.lower() == f"{name_lower}.md":
                return Path(root) / file
    return None


def load_agent(name: str) -> str:
    """
    Load an agent by name and return its markdown content.
    Returns a helpful error message if the agent is not found.
    """
    agent_path = _find_agent_file(name)

    if agent_path and agent_path.exists():
        return agent_path.read_text(encoding="utf-8")

    return f"❌ Agent '{name}' not found in STORAGE/AGENTS/ (including subfolders)."


def list_all_agents() -> List[str]:
    """
    Return a sorted list of all available agent names (without .md extension).
    """
    agents = set()
    for root, dirs, files in os.walk(AGENTS_DIR):
        for file in files:
            if file.endswith(".md"):
                agents.add(file[:-3])  # remove .md extension
    return sorted(agents)


def get_agent_path(name: str) -> Optional[str]:
    """
    Return the full relative path to an agent's .md file (if it exists).
    Useful for debugging or future .py upgrades.
    """
    agent_path = _find_agent_file(name)
    return str(agent_path) if agent_path else None


# =============================================================================
# FUTURE: Python Version Support (commented out for now)
# =============================================================================
#
# When you're ready to convert agents to Python, uncomment and extend this:
#
# def load_agent_python(name: str):
#     py_path = AGENTS_DIR / f"{name}.py"
#     if py_path.exists():
#         # Load and return the Python class
#         ...
#     else:
#         return load_agent(name)  # fallback to markdown
#


if __name__ == "__main__":
    print("=== AGENT_LOADER Test ===")
    print(f"Available agents: {list_all_agents()}")
    print("\n--- Loading BabySkynet ---")
    print(load_agent("BabySkynet")[:300] + "...")
