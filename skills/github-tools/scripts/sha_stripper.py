#!/usr/bin/env python3
"""
github-tools/scripts/sha_stripper.py
Strip SHA fields from index files before pushing to prevent conflicts.
"""

import json
from pathlib import Path

def strip_shas_from_index(file_path: str) -> bool:
    """
    Remove all 'sha' fields from a *_INDEX.json file.
    Returns True if changes were made.
    """
    path = Path(file_path)
    if not path.exists():
        print(f"⚠️ File not found: {file_path}")
        return False

    data = json.loads(path.read_text())
    modified = False

    if "files" in data:
        for entry in data["files"]:
            if "sha" in entry:
                del entry["sha"]
                modified = True

    if modified:
        path.write_text(json.dumps(data, indent=2))
        print(f"✅ Stripped SHAs from {file_path}")
    return modified