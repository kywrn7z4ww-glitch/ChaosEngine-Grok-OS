"""
index_builder.py — Grok OS Index Builder v1.0
Purpose: Scans folders and builds/updates the corresponding _INDEX.json files.
Adds short purpose tags and logs everything.

Location: /ROOT/boot/index_builder.py
"""

import json
import os
from datetime import datetime
from pathlib import Path

# === CONFIG ===
LOCAL_ROOT = Path(os.getenv("GROKOS_ROOT", "/home/workdir/artifacts/grok-os/ROOT"))
LOGS_DIR = Path("/home/workdir/artifacts/grokos/logs")
BOOT_LOG = LOGS_DIR / "boot_log.json"
BUG_REPORTS = LOGS_DIR / "bug_reports.json"


def log_event(event: str, status: str = "success", details: str = ""):
    """Write to Boot_Log.json"""
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
        print(f"[index_builder] Log write failed: {e}")


def build_index(folder_name: str, index_path: Path):
    """Build or update a single _INDEX.json"""
    folder = LOCAL_ROOT / folder_name
    if not folder.exists():
        log_event("index_build_skipped", "warning", f"Folder not found: {folder_name}")
        return

    files = []
    for root, dirs, filenames in os.walk(folder):
        for f in filenames:
            if f.endswith((".py", ".md")) and not f.startswith("__"):
                rel_path = os.path.relpath(os.path.join(root, f), LOCAL_ROOT)
                files.append(
                    {
                        "path": rel_path,
                        "purpose": "Auto-generated stub — needs manual description",
                        "size": os.path.getsize(os.path.join(root, f)),
                        "last_modified": datetime.fromtimestamp(
                            os.path.getmtime(os.path.join(root, f))
                        ).isoformat(),
                    }
                )

    index_data = {
        "version": "1.0",
        "folder": folder_name,
        "last_updated": datetime.now().isoformat(),
        "total_files": len(files),
        "files": files,
    }

    index_path.write_text(json.dumps(index_data, indent=2))
    log_event("index_built", "success", f"{folder_name} → {len(files)} files")


def main():
    print("🔧 Grok OS Index Builder v1.0")

    # Build core indexes
    build_index("PROCESS", LOGS_DIR / "PROCESS_INDEX.json")
    build_index("layers", LOGS_DIR / "LAYERS_INDEX.json")
    build_index("chaos-engine", LOGS_DIR / "CHAOS_ENGINE_INDEX.json")
    build_index("emotion-net", LOGS_DIR / "EMOTION_NET_INDEX.json")

    log_event("index_builder_complete", "success", "All core indexes updated")
    print("✅ Index build complete")


if __name__ == "__main__":
    main()
