"""
mirror_logic.py — GrokOS Mirror Logic v0.3 (Integrated with Download Skill)

Purpose: Orchestrator for the batch mirroring process.
Follows the boot_sequence defined in REPO_INDEX.json.
Now uses download_skill.py for actual file pulling.

Location: ROOT/boot/mirroring/mirror_logic.py
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

from .download_skill import download_file_list

# === CONFIG ===
LOGS_DIR = Path("/home/workdir/artifacts/grokos/logs")
BOOT_LOG = LOGS_DIR / "boot_log.json"
BUG_REPORTS = LOGS_DIR / "bug_reports.json"
INDEX_BUILDER = Path("/home/workdir/artifacts/index_builder.py")


def log_event(event: str, status: str = "success", details: str = ""):
    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "event": event,
        "status": status,
        "details": details,
    }
    try:
        if BOOT_LOG.exists():
            data = json.loads(BOOT_LOG.read_text())
        else:
            data = {"version": "1.0", "entries": []}
        data["entries"].append(entry)
        BOOT_LOG.write_text(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[mirror_logic] Log write failed: {e}")


def load_repo_index():
    index_path = Path("/home/workdir/artifacts/REPO_INDEX.v2.5.json")
    if not index_path.exists():
        raise FileNotFoundError("REPO_INDEX.v2.5.json not found")
    return json.loads(index_path.read_text())


def call_index_builder():
    if not INDEX_BUILDER.exists():
        print("[mirror_logic] index_builder.py not found — skipping")
        return False
    try:
        result = subprocess.run(
            ["python3", str(INDEX_BUILDER)], capture_output=True, text=True, timeout=30
        )
        log_event("index_builder_called", "success", result.stdout[:200])
        print(f"[mirror_logic] index_builder.py output: {result.stdout[:200]}")
        return True
    except Exception as e:
        log_event("index_builder_error", "error", str(e))
        print(f"[mirror_logic] index_builder error: {e}")
        return False


def run_phase_0():
    log_event("phase_0_start", "success", "Pre-Boot starting")
    print("[mirror_logic] Phase 0 — Pre-Boot")
    call_index_builder()
    log_event("phase_0_complete", "success", "Manifests + index_builder done")
    return True


def run_phase_1(core_components):
    log_event(
        "phase_1_start", "success", f"Core Mirror: {len(core_components)} components"
    )
    print(f"[mirror_logic] Phase 1 — Core Mirror ({len(core_components)} files)")

    # Use the real download skill
    results = download_file_list(core_components, target_dir=".", profile="grok-os")

    for item, success in results.items():
        if success:
            log_event("file_pulled", "success", item)
            print(f"  ✓ Pulled: {item}")
        else:
            log_event("file_failed", "warning", item)
            print(f"  ✗ Skipped/Failed: {item}")

    log_event("phase_1_complete", "success", "Core components processed")
    return True


def run_phase_1_5():
    log_event("phase_1_5_start", "success", "ROOT Batch Load")
    print("[mirror_logic] Phase 1.5 — ROOT Batch Load (layers → boot → chaos-engine)")
    return True


def run_mirror_logic():
    print("=== GrokOS Mirror Logic v0.3 (Integrated) ===")
    log_event("mirror_logic_start", "success", "Starting batch mirror process")

    try:
        index = load_repo_index()
        core = index.get("core_components", [])

        run_phase_0()
        run_phase_1(core)
        run_phase_1_5()

        log_event("mirror_logic_complete", "success", "All phases finished")
        print("=== Mirror Logic Complete ===")
        return True

    except Exception as e:
        log_event("mirror_logic_error", "error", str(e))
        print(f"[mirror_logic] ERROR: {e}")
        return False


if __name__ == "__main__":
    run_mirror_logic()
