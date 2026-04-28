"""
boot/__init__.py — Grok OS Master Boot v3.2 (Two-Phase)
Phase 1: Mass Download → Phase 2: Install & Chain
"""

import importlib
import pkgutil
from pathlib import Path

LOCAL_ROOT = Path("/opt/grok-os/ROOT")


def boot_grok_os():
    print("🚀 [boot] Grok OS Two-Phase Boot Starting...")

    # === PHASE 1: MASS DOWNLOAD ===
    print("\n📥 Phase 1: Mass Download")
    try:
        from grok_download import sync_github_folder

        sync_github_folder(
            "https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/tree/main/ROOT",
            str(LOCAL_ROOT),
            profile="grok-os",
        )
        print("  ✅ All core files downloaded")
    except Exception as e:
        print(f"  ⚠️  Download failed or not available: {e}")
        print("  → Continuing with local files only...")

    # === PHASE 2: INSTALL & CHAIN ===
    print("\n🔗 Phase 2: Install & Chain Systems")
    loaded = []

    for importer, modname, ispkg in pkgutil.iter_modules([str(LOCAL_ROOT)]):
        if ispkg:
            try:
                importlib.import_module(f".{modname}", package="ROOT")
                print(f"  ✅ {modname}")
                loaded.append(modname)
            except Exception as e:
                print(f"  ⚠️  {modname} failed: {e}")

    print(f"\n✅ Grok OS booted — {len(loaded)} systems loaded")
    return loaded


if __name__ == "__main__":
    boot_grok_os()
