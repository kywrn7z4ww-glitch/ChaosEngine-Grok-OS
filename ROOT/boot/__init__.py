"""
boot/__init__.py — Grok OS Master Boot v3.2 (Recursive + Two-Phase)
Phase 1: Mass Download → Phase 2: Recursive Scan + Chain
Only scans under ROOT/ (core systems)
"""

import importlib.util
import os
from pathlib import Path

LOCAL_ROOT = Path("/opt/grok-os/ROOT")


def boot_grok_os():
    print("🚀 [boot] Grok OS Recursive Boot v3.2 Starting...")

    # === PHASE 1: MASS DOWNLOAD (optional) ===
    print("\n📥 Phase 1: Mass Download")
    try:
        from grok_download import sync_github_folder

        sync_github_folder(
            "https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/tree/main/ROOT",
            str(LOCAL_ROOT),
            profile="grok-os",
        )
        print("  ✅ Core systems downloaded")
    except:
        print("  ⚠️  Download skill not available — using local files")

    # === PHASE 2: RECURSIVE SCAN + CHAIN ===
    print("\n🔗 Phase 2: Recursive Scan & Chain")
    loaded = []

    for root, dirs, files in os.walk(LOCAL_ROOT):
        if "__init__.py" in files:
            try:
                rel_path = Path(root).relative_to(LOCAL_ROOT)
                module_name = str(rel_path).replace("/", ".").replace("\\", ".")

                if module_name:
                    spec = importlib.util.spec_from_file_location(
                        module_name, Path(root) / "__init__.py"
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    print(f"  ✅ {module_name}")
                    loaded.append(module_name)
            except Exception as e:
                print(f"  ⚠️  {root} failed: {e}")

    print(f"\n✅ Grok OS booted — {len(loaded)} systems loaded (full recursive)")
    return loaded


if __name__ == "__main__":
    boot_grok_os()
