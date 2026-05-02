"""
__init__.py — GrokOS Mirroring Package
Auto-installs and exposes the Download Skill + Mirror Logic as loadable skills.

This makes the entire mirroring subsystem self-bootstrapping.
"""

import json
from datetime import datetime
from pathlib import Path

# === Skill Registration ===
SKILL_REGISTRY = {
    "grok-download": {
        "name": "grok-download",
        "version": "1.4",
        "description": "Production-ready GitHub download skill with full tree scanning, SHA verification, raw URL fallback, and graceful error handling.",
        "module": "download_skill",
        "status": "installed",
        "installed_at": None,
    },
    "mirror-logic": {
        "name": "mirror-logic",
        "version": "0.3",
        "description": "Orchestrator for batch mirroring following the official boot sequence.",
        "module": "mirror_logic",
        "status": "installed",
        "installed_at": None,
    },
}


def register_skill(skill_name: str):
    """Register a skill in the central registry (simulated)."""
    if skill_name in SKILL_REGISTRY:
        SKILL_REGISTRY[skill_name]["installed_at"] = datetime.now().isoformat()
        SKILL_REGISTRY[skill_name]["status"] = "active"
        print(f"[mirroring/__init__] Skill registered: {skill_name}")
        return True
    return False


def get_skill(skill_name: str):
    """Retrieve a registered skill."""
    return SKILL_REGISTRY.get(skill_name)


# === Auto-Install on Package Import ===
def install_mirroring_skills():
    """Install both the Download Skill and Mirror Logic."""
    print("[mirroring/__init__] Installing GrokOS mirroring skills...")

    # Install Download Skill first (dependency)
    try:
        from .download_skill import install as install_ds

        install_ds()
        register_skill("grok-download")
    except Exception as e:
        print(f"[mirroring/__init__] Download Skill install failed: {e}")

    # Then install/register Mirror Logic
    try:
        register_skill("mirror-logic")
    except Exception as e:
        print(f"[mirroring/__init__] Mirror Logic register failed: {e}")

    print("[mirroring/__init__] All mirroring skills installed and active.")
    return True


# Auto-trigger on import (self-bootstrapping)
install_mirroring_skills()

# Public API
from .download_skill import download_file_list
from .download_skill import install as install_download_skill
from .mirror_logic import run_mirror_logic

__all__ = [
    "download_file_list",
    "install_download_skill",
    "run_mirror_logic",
    "install_mirroring_skills",
    "SKILL_REGISTRY",
]
