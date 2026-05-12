#!/usr/bin/env python3
"""
github-tools/scripts/stage.py
Handle STAGE.md in cache/ (flat, non-nested).
"""

from pathlib import Path
from datetime import datetime

CACHE_DIR = Path("/home/workdir/artifacts/Grok OS/cache")
STAGE_FILE = CACHE_DIR / "STAGE.md"

def update_stage(changes: list, status: str = "In Progress"):
    """
    Update STAGE.md with new changes.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    content = f"# STAGE.md - {datetime.now().isoformat()}\n\n"
    content += f"**Status:** {status}\n\n"
    content += "## Changes\n"
    for change in changes:
        content += f"- {change}\n"
    
    STAGE_FILE.write_text(content)
    print(f"✅ Updated {STAGE_FILE}")
    return STAGE_FILE