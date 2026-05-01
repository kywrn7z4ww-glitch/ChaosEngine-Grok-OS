#!/usr/bin/env python3
"""
chaos-engine.py — Grok OS ChaosEngine v4.1 (Full Logging + Index Builder + Future Patch Support)
Purpose: Central brain with mandatory logging, index building, and support for future_patches.json + changelog.json
"""

import importlib.util
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Set

# === CONFIG ===
LOCAL_ROOT = Path("/home/workdir/artifacts/grok-os/ROOT")
LOGS_DIR = Path("/home/workdir/artifacts/grokos/logs")

BOOT_LOG = LOGS_DIR / "boot_log.json"
BUG_REPORTS = LOGS_DIR / "bug_reports.json"
CHANGELOG = LOGS_DIR / "changelog.json"
FUTURE_PATCHES = LOGS_DIR / "future_patches.json"

# Import index builder
try:
    from boot.index_builder import main as build_indexes
except:
    build_indexes = None


def log_event(event: str, status: str = "success", details: str = ""):
    """Write to boot_log.json"""
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
        print(f"[chaos_engine] Log write failed: {e}")


def log_bug(severity: str, message: str, data: dict = None):
    """Write to bug_reports.json"""
    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "severity": severity,
        "message": message,
        "data": data or {},
    }
    try:
        if BUG_REPORTS.exists():
            bugs = json.loads(BUG_REPORTS.read_text())
        else:
            bugs = {"version": "1.0", "entries": []}
        bugs["entries"].append(entry)
        BUG_REPORTS.write_text(json.dumps(bugs, indent=2))
    except Exception as e:
        print(f"[chaos_engine] Bug log failed: {e}")


def load_json_log(path: Path) -> dict:
    """Load a JSON log file (used for future_patches.json and changelog.json)"""
    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            return {"version": "1.0", "entries": []}
    return {"version": "1.0", "entries": []}


class ChaosEngine:
    def __init__(self):
        self.turn = None
        self.emotionnet = None
        self.processes: Dict[str, Any] = {}
        self.active_layer: str = "dev"
        self.live_index: Set[str] = set()

        log_event("chaosengine_init_started")
        self._load_emotionnet()
        self._build_live_index()
        self._load_all_processes_dynamically()
        log_event("chaosengine_init_complete")

        print(
            "⚙️  ChaosEngine v4.1 — Full Logging + Index Builder + Future Patch Support Online"
        )

    def _build_live_index(self):
        log_event("live_index_build_started")
        print("🔍 Building live index...")

        if build_indexes:
            try:
                build_indexes()
                log_event("index_builder_called", "success")
            except Exception as e:
                log_event("index_builder_failed", "error", str(e))
                log_bug("error", "Index builder failed", {"error": str(e)})

        self.live_index = set()
        for base_dir in ["PROCESS", "layers", "chaos-engine", "emotion-net"]:
            base_path = LOCAL_ROOT / base_dir
            if base_path.exists():
                for root, dirs, files in os.walk(base_path):
                    for file in files:
                        if file.endswith(".py") and not file.startswith("__"):
                            rel_path = os.path.relpath(
                                os.path.join(root, file), LOCAL_ROOT
                            )
                            self.live_index.add(rel_path)

        log_event("live_index_built", "success", f"{len(self.live_index)} files")
        print(f"  ✅ Live index built ({len(self.live_index)} files)")

    def _load_emotionnet(self):
        try:
            filepath = LOCAL_ROOT / "emotion-net/emotion-net.py"
            if not filepath.exists():
                log_event("emotionnet_missing", "warning")
                return
            spec = importlib.util.spec_from_file_location("EmotionNet", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.emotionnet = module.EmotionNet()
            log_event("emotionnet_loaded")
            print("🧠 EmotionNet loaded")
        except Exception as e:
            log_event("emotionnet_failed", "error", str(e))
            log_bug("error", "Failed to load EmotionNet", {"error": str(e)})

    def _load_all_processes_dynamically(self):
        log_event("dynamic_load_started")
        print("🔄 Loading all discovered processes...")
        loaded = 0
        for rel_path in sorted(self.live_index):
            if not rel_path.endswith(".py"):
                continue
            try:
                full_path = LOCAL_ROOT / rel_path
                module_name = Path(rel_path).stem
                spec = importlib.util.spec_from_file_location(module_name, full_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                handler = None
                if hasattr(module, module_name):
                    handler = getattr(module, module_name)()
                elif hasattr(module, "main"):
                    handler = module
                else:
                    handler = module

                self.processes[module_name.lower()] = handler
                loaded += 1
            except Exception as e:
                log_event("process_load_failed", "error", f"{rel_path}: {e}")
                log_bug("warning", f"Failed to load {rel_path}", {"error": str(e)})

        log_event("dynamic_load_complete", "success", f"{loaded} processes loaded")
        print(f"✅ Loaded {loaded} processes/skills dynamically")

    def load_all(self):
        print("🔄 ChaosEngine fully initialized with full logging")
        log_event("load_all_called")
        return "Ready — all skills and processes loaded"


# Quick self-test
if __name__ == "__main__":
    engine = ChaosEngine()
    engine.load_all()
