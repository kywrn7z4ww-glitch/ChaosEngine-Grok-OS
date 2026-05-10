#!/usr/bin/env python3
"""
index_builder.py — Grok OS Index Builder v4.0 (Full Repo Layout Mode)
Purpose: Dynamically populates all local *_INDEX.json files by scanning the actual filesystem.
Reflects the full repo layout for accurate GitHub repo pulls and ChaosEngine connectors.
Called early in the boot sequence (Phase 0/1) as the source of truth.
"""

import json
from datetime import datetime
from pathlib import Path
import os

BASE = Path("/home/workdir/artifacts/grok-os")
ROOT_DIR = BASE / "ROOT"
RUNTIME_BASE = Path("/home/workdir/artifacts/grokos")
LOGS_DIR = RUNTIME_BASE / "logs"

def _load_json(path: Path, default=None):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            pass
    return default or {}

def _save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))

def build_repo_index():
    """Builds/updates the master REPO_INDEX.json by dynamically scanning repo layout"""
    index_path = ROOT_DIR / "REPO_INDEX.json"
    
    # Dynamically discover top-level folders that have content
    top_level_dirs = ["ROOT", "PROCESS", "STORAGE", "LAYERS", "NETWORK_HUB", "Documentation", "ARCHIVE"]
    sub_indexes = {}
    for d in top_level_dirs:
        dir_path = BASE / d
        if dir_path.exists():
            if d == "ROOT":
                sub_indexes[d] = "ROOT/ROOT_INDEX.json"
            elif d == "ARCHIVE":
                sub_indexes[d] = "ARCHIVE/index.json"
            else:
                sub_indexes[d] = f"{d}/{d}_INDEX.json"
    
    # Core boot components (minimal set for cold start - kept explicit for safety)
    core_components = [
        "ROOT/boot/index_builder.py",
        "ROOT/boot/grok-os.md",
        "ROOT/boot/decision-kernel.md",
        "ROOT/boot/grok_os.py",
        "ROOT/chaos_engine/__init__.py",
        "ROOT/chaos_engine/chaos_engine.py",
        "ROOT/chaos_engine/layer_manager.py",
        "ROOT/chaos_engine/ui_manager.py",
        "ROOT/chaos_engine/response_pipeline.py"
    ]
    
    data = {
        "version": "4.0",
        "purpose": "Master REPO Index - Source of truth for Grok OS boot. Dynamically reflects full repo layout for repo pulls via GitHub connectors.",
        "last_updated": datetime.now().isoformat(),
        "total_core_components": len(core_components),
        "total_sub_indexes": len(sub_indexes),
        "core_components": core_components,
        "sub_indexes": sub_indexes,
        "boot_log": "boot_log.json",
        "bug_reports": "bug_reports.json",
        "notes": "v4.0 full repo layout mode. Indexes auto-built from filesystem to match remote repo structure. Supports dynamic pulls, validation, and lazy loading. Mirror logic fully deprecated. SHA handling: SHA intentionally omitted from index entries (local runtime fetches via GitHub API on pull/validate to avoid churn/mismatches)."
    }
    
    _save_json(index_path, data)
    print(f"[index_builder] ✓ Updated REPO_INDEX.json (dynamic, {len(sub_indexes)} sub-indexes)")
    return data

def build_folder_index(folder_name: str):
    """Generic scanner for any top-level folder to build its _INDEX.json"""
    folder_path = BASE / folder_name
    if not folder_path.exists():
        print(f"[index_builder] ⚠️ Skipping {folder_name} (not found)")
        return None
    
    index_filename = f"{folder_name}_INDEX.json"
    index_path = folder_path / index_filename if folder_name != "ROOT" else ROOT_DIR / "ROOT_INDEX.json"
    
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for f in filenames:
            # Include common code/docs/config files
            if f.endswith(('.py', '.md', '.json', '.txt', '.yaml', '.yml', '.sh')) and not f.startswith('__'):
                rel = os.path.relpath(os.path.join(root, f), folder_path)
                full_path = f"{folder_name}/{rel}" if folder_name != "ROOT" else f"ROOT/{rel}"
                try:
                    size = (folder_path / rel).stat().st_size
                except:
                    size = 0
                files.append({
                    "path": full_path,
                    "pulled": False,  # Ready for pull tracking
                    "size": size,
                    "updated": datetime.now().isoformat()
                })
    
    data = {
        "version": "4.0",
        "folder": folder_name,
        "last_updated": datetime.now().isoformat(),
        "total_files": len(files),
        "files": files,
        "notes": f"Auto-generated from local {folder_name}/ layout. Use for repo pulls and validation. SHA handling: SHA intentionally omitted from index entries (set to local runtime fetch via GitHub API). Prevents update churn & self-mismatch on index pushes. Local ChaosEngine/REPO_VALIDATOR populates/validates SHA on-demand."
    }
    
    _save_json(index_path, data)
    print(f"[index_builder] ✓ Updated {index_filename} ({len(files)} files)")
    return data

def build_layers_index():
    """Special scanner for LAYERS folder: scans repo subdirs for Layer: definitions to build dynamic layers index.
    Boot is mandatory only for booting; post-boot defaults to dev layer."""
    folder_path = BASE / "LAYERS"
    if not folder_path.exists():
        print("[index_builder] ⚠️ LAYERS folder not found, skipping layers index")
        return None
    
    index_path = folder_path / "LAYERS_INDEX.json"
    
    layers = []
    # Scan all subdirs for valid layer .md files (exclude cache/duplicate/ non-layer files)
    for subdir in sorted([d for d in folder_path.iterdir() if d.is_dir()]):
        if subdir.name in ["__pycache__", "LAYERS"]:
            continue  # skip internal duplicates and cache
        md_files = list(subdir.glob("*.md"))
        for md_file in md_files:
            if md_file.name == "git_connector_workflow.md":
                continue  # not a layer definition
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                if "# Layer:" in content:
                    name = subdir.name
                    path = f"LAYERS/{name}/{md_file.name}"
                    # Boot only for boot; dev is default after boot
                    active = True
                    last_loaded = datetime.now().isoformat() if name in ["boot", "dev"] else None
                    layers.append({
                        "name": name,
                        "path": path,
                        "active": active,
                        "last_loaded": last_loaded
                    })
            except Exception:
                pass
    
    data = {
        "version": "4.0",
        "purpose": "**LAYERS Index** — Dynamically scanned from repo for all Layer: definitions. Tracks available runtime layers.",
        "folder": "LAYERS",
        "last_updated": datetime.now().isoformat(),
        "total_layers": len(layers),
        "layers": layers,
        "notes": "Boot layer is ONLY mandatory for initial system boot (cold start). Once booted, control hands off to the dev layer by default for ongoing operation and development. Use /layer casual, /layer roleplay etc. to switch. Currently 4 layers detected via repo scan (more can be added by creating new LAYERS/<name>/<name>.md with '# Layer: /<name>' header). SHA intentionally omitted — local runtime fetches fresh SHA from GitHub API during pulls."
    }
    
    _save_json(index_path, data)
    print(f"[index_builder] ✓ Updated LAYERS_INDEX.json (scanned {len(layers)} layers from repo: {[l['name'] for l in layers]})")
    return data


def build_archive_index():
    """Lightweight index for ARCHIVE/ — describes navigation and structure instead of enumerating every historical file.
    Prevents bloat as more dated changelogs and snapshots are added over time.
    Relies on Git commits + dated folder convention for full history."""
    folder_path = BASE / "ARCHIVE"
    if not folder_path.exists():
        print("[index_builder] ⚠️ ARCHIVE folder not found, skipping")
        return None
    
    index_path = folder_path / "ARCHIVE_INDEX.json"
    
    data = {
        "version": "4.0",
        "folder": "ARCHIVE",
        "purpose": "Version history, patch notes, and deprecated snapshots for safe rollbacks. Intentionally lightweight — does NOT list every file to prevent index bloat as history grows.",
        "last_updated": datetime.now().isoformat(),
        "structure": {
            "changelog/": "Dated subfolders per major overhaul (format: DD-MM-YYYY-short-title/). Each contains the changelog .md entry + any archived snapshots for that session.",
            "navigation_guide": "Browse by date in changelog/. For full change details and diffs, use GitHub repo history, `git log --follow ARCHIVE/changelog/`, or connectors to inspect commits. No need to pull every historical file during boot or validation."
        },
        "total_files_tracked": 0,
        "files": [],  # Empty by design — rely on Git + folder structure instead of duplicating history in JSON
        "notes": "Full history lives in Git commits (SHA-1 tree). Local ChaosEngine/REPO_VALIDATOR or runtime can use Git API for on-demand validation of specific historical files. SHA intentionally omitted from index. This keeps ARCHIVE_INDEX.json tiny forever while still providing clear navigation instructions."
    }
    
    _save_json(index_path, data)
    print("[index_builder] ✓ Updated ARCHIVE_INDEX.json (lightweight navigation mode — no bloat from historical files)")
    return data


def build_root_index():
    """Wrapper for ROOT folder (special path handling)"""
    return build_folder_index("ROOT")

def main():
    """Main entry point - called by grok_os.py during boot"""
    print("\n[index_builder] Building local indexes (v4.0 - Full Repo Layout Mode)...")
    print("   Reflecting actual filesystem to support accurate repo pulls from GitHub")
    
    build_repo_index()
    build_root_index()
    build_layers_index()  # Special scan for all layers (boot only for boot; defaults to dev post-boot)
    
    # Build indexes for all other major folders (ARCHIVE handled specially below to avoid bloat)
    other_folders = ["PROCESS", "STORAGE", "NETWORK_HUB", "Documentation"]
    for folder in other_folders:
        build_folder_index(folder)
    
    build_archive_index()  # Special lightweight handler — navigation guide + Git-based history instead of file list
    
    # Update boot_log
    log_path = LOGS_DIR / "boot_log.json"
    log = _load_json(log_path, {"entries": []})
    log["entries"].append({
        "timestamp": datetime.now().isoformat(),
        "event": "index_builder_complete",
        "status": "success",
        "details": "All indexes dynamically populated (ARCHIVE uses lightweight navigation mode to prevent bloat)"
    })
    _save_json(log_path, log)
    
    print("[index_builder] ✓ All indexes ready — repo layout fully reflected (ARCHIVE smart mode active)\n")
    return True

if __name__ == "__main__":
    main()
