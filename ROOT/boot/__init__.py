"""
boot/ package — Grok OS Boot Layer v2.1
Initializes the boot system and exposes core boot components.
"""

# Safe import of grok_os (the main boot script)
try:
    from .grok_os import main as boot_grok_os
except ImportError:
    boot_grok_os = None
    print("[boot] Warning: grok_os.py not found or failed to import")

print("[boot] Grok OS boot package initialized")
