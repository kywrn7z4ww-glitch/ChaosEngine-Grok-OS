#!/usr/bin/env python3
"""
github-tools/scripts/download.py
Download files/folders from GitHub and save locally using connectors.
"""

import os
from pathlib import Path

def download_file(owner: str, repo: str, path: str, branch: str, local_path: str):
    """
    Download a single file from GitHub and save it locally.
    Uses github___get_file_contents internally.
    """
    print(f"⬇️ Downloading {path} from {owner}/{repo}...")
    # Placeholder - actual implementation would call github___get_file_contents
    # and write the content to local_path
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    # Simulated write
    with open(local_path, "w") as f:
        f.write(f"# Downloaded from {owner}/{repo}/{path}\n")
    print(f"✅ Saved to {local_path}")
    return local_path

def download_folder(owner: str, repo: str, path: str, branch: str, local_base: str):
    """
    Recursively download a folder.
    """
    print(f"⬇️ Downloading folder {path}...")
    # Placeholder for recursive download logic
    return f"{local_base}/{path}"