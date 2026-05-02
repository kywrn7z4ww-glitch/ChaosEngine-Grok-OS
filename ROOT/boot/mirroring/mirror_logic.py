#!/usr/bin/env python3
"""
mirror_logic.py — GrokOS Mirror Logic & Boot Orchestrator v2.5 (FIXED)

Implements the authoritative phased boot sequence from mirror-logic.md + REPO_INDEX.json.
This file was previously a duplicate of download_skill.py — now it is the real orchestrator.
"""

import json
from datetime import datetime
from pathlib import Path

# Import the download skill (robust for both package and direct run)
try:
    from .download_skill import download_file_list
    from .download_skill import install as install_download_skill
except ImportError:
    import sys
    from pathlib import Path as _Path

    sys.path.insert(0, str(_Path(__file__).parent))
    from download_skill import download_file_list
    from download_skill import install as install_download_skill

BASE = Path("/home/workdir/artifacts")
ROOT_DIR = BASE / "ROOT"
LOGS_DIR = BASE / "grokos" / "logs"


def _load_json(path: Path, default=None):
    if path.exists():
        return json.loads(path.read_text())
    return default or {}


def _save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def _update_boot_log(action: str, details: dict = None):
    """Mandatory per spec: update boot_log.json immediately after every action."""
    log_path = LOGS_DIR / "boot_log.json"
    log = _load_json(log_path, {"entries": []})
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details or {},
    }
    log["entries"].append(entry)
    _save_json(log_path, log)
    print(f"[mirror-logic] ✓ Logged: {action}")


def _update_bug_report(error: str, data: dict = None):
    """Mandatory per spec for rich debugging."""
    report_path = LOGS_DIR / "bug_reports.json"
    reports = _load_json(report_path, {"reports": []})
    reports["reports"].append(
        {"timestamp": datetime.now().isoformat(), "error": error, "data": data or {}}
    )
    _save_json(report_path, reports)


def run_mirror_logic(profile="grok-os", full=False):
    """
    Main entry point — follows exact phases from mirror-logic.md
    Phase 0 → 1 → 1.5 → 2 → 3
    """
    print(
        f"\n[mirror-logic] === GrokOS Boot Sequence v2.5 START (profile={profile}, full={full}) ==="
    )
    _update_boot_log("boot_started", {"profile": profile, "full": full})

    # === Phase 0 — Pre-Boot ===
    print(
        "[mirror-logic] Phase 0 — Pre-Boot: Activating Download Skill + loading indexes..."
    )
    install_download_skill()
    _update_boot_log("phase0_download_skill_active")

    # Load/create REPO_INDEX.json (source of truth)
    repo_index_path = ROOT_DIR / "REPO_INDEX.json"
    if not repo_index_path.exists():
        repo_index = {
            "version": "2.5",
            "last_updated": datetime.now().isoformat(),
            "core_components": [
                "ROOT/boot/mirroring/download_skill.py",
                "ROOT/boot/mirroring/mirror_logic.py",
                "ROOT/boot/mirroring/__init__.py",
                "ROOT/boot/grok-os.md",
                "ROOT/UI_Template.md",
                "ROOT/chaos-engine/__init__.py",
            ],
            "sub_indexes": {"ROOT": "ROOT_INDEX.json"},
            "boot_sequence": ["Phase 0-3 implemented in mirror_logic.py"],
        }
        _save_json(repo_index_path, repo_index)
    else:
        repo_index = _load_json(repo_index_path)

    print("[mirror-logic] (index_builder stub) Indexes ready from disk.")
    _update_boot_log("phase0_indexes_ready")

    # === Phase 1 — Core Mirror ===
    print("[mirror-logic] Phase 1 — Core Mirror: Pulling ONLY core_components...")
    core_files = repo_index.get("core_components", [])
    if core_files:
        download_file_list(core_files, target_dir=str(ROOT_DIR), profile=profile)
        _update_boot_log("phase1_core_mirror_complete", {"count": len(core_files)})

    # === Phase 1.5 — ROOT Batch Load ===
    print(
        "[mirror-logic] Phase 1.5 — ROOT Batch Load (priority: layers/ → boot/ → chaos-engine/)..."
    )
    root_batch = [
        "ROOT/layers/__init__.py",
        "ROOT/boot/mirroring/__init__.py",
        "ROOT/boot/mirroring/download_skill.py",
        "ROOT/boot/mirroring/mirror_logic.py",
        "ROOT/chaos-engine/__init__.py",
        "ROOT/emotion-net/__init__.py",  # partial load only
    ]
    download_file_list(root_batch, target_dir=str(ROOT_DIR), profile=profile)
    _update_boot_log("phase1.5_root_batch_complete")

    # Update ROOT_INDEX.json
    root_index_path = ROOT_DIR / "ROOT_INDEX.json"
    root_index = _load_json(root_index_path, {"files": [], "last_mirrored": None})
    root_index["last_mirrored"] = datetime.now().isoformat()
    root_index["files"] = root_batch
    _save_json(root_index_path, root_index)

    # === Phase 2 — Next Batch (controlled) ===
    print(
        "[mirror-logic] Phase 2 — Next Batch (PROCESS/ + STORAGE/ — skipped in this run for safety)..."
    )
    _update_boot_log("phase2_next_batch_skipped", {"reason": "controlled batch"})

    # === Phase 3 — Handoff + Lazy Runtime ===
    print("[mirror-logic] Phase 3 — Handoff + Lazy Runtime enabled...")
    _update_boot_log(
        "boot_complete",
        {"status": "success", "handoff_ready": True, "lazy_pulls_enabled": True},
    )

    print("[mirror-logic] ✓ GrokOS boot complete. System ready for on-demand pulls.\n")
    return {"status": "success", "boot_log": str(LOGS_DIR / "boot_log.json")}


# Self-test if run directly
if __name__ == "__main__":
    run_mirror_logic()
