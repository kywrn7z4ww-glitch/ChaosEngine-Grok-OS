#!/usr/bin/env python3
"""
Grok OS - Snapshot Manager
Lightweight, purge-friendly snapshot system.
Creates timestamped JSON snapshots + maintains snapshot-eval.json index.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "snapshots")
EVAL_FILE = os.path.join(SNAPSHOT_DIR, "snapshot-eval.json")

def ensure_dir():
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def create_snapshot(layer: str, data: Dict[str, Any], notes: str = "") -> str:
    """Create a new snapshot. Returns filename."""
    ensure_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{layer}.json"
    path = os.path.join(SNAPSHOT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Update eval index
    entry = {
        "timestamp": timestamp,
        "layer": layer,
        "filename": filename,
        "size_bytes": os.path.getsize(path),
        "notes": notes,
        "eval_score": 0.0,      # future: auto-eval or user score
        "created_at": datetime.now().isoformat()
    }

    if os.path.exists(EVAL_FILE):
        with open(EVAL_FILE, "r", encoding="utf-8") as f:
            eval_data: List[Dict] = json.load(f)
    else:
        eval_data = []

    eval_data.append(entry)
    with open(EVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(eval_data, f, indent=2)

    return filename

def list_snapshots() -> List[str]:
    ensure_dir()
    return sorted([
        f for f in os.listdir(SNAPSHOT_DIR)
        if f.endswith(".json") and f != "snapshot-eval.json"
    ], reverse=True)

def load_snapshot(filename: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(SNAPSHOT_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def delete_snapshot(filename: str) -> bool:
    path = os.path.join(SNAPSHOT_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
        # TODO: also remove from snapshot-eval.json (light cleanup)
        return True
    return False

def get_eval_summary() -> List[Dict[str, Any]]:
    if not os.path.exists(EVAL_FILE):
        return []
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    print("Snapshot Manager ready. Use from chaos_engine or boot.")
    print("Example: create_snapshot('casual', {'turns': 12, 'mood': 'chill'})"
