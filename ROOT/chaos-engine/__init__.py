"""
ChaosEngine v3.2 — Package Initializer
Auto-loads all core managers on first import.
This makes the entire system "chain-fire" cleanly.
"""

# ============================================================
# AUTO-LOAD CORE MANAGERS (the "chain fire")
# ============================================================
try:
    from .chaos_engine import ChaosEngine
    from .layer_manager import LayerManager
    from .response_pipeline import ResponsePipeline
    from .ui_manager import UIManager
except ImportError as e:
    print(f"[ChaosEngine] Warning: Could not import one or more managers: {e}")
    LayerManager = UIManager = ResponsePipeline = ChaosEngine = None

# ============================================================
# CREATE SINGLETON INSTANCES (only if imports succeeded)
# ============================================================
if LayerManager and UIManager and ResponsePipeline and ChaosEngine:
    layer_manager = LayerManager()
    ui_manager = UIManager()
    response_pipeline = ResponsePipeline()
    chaos_engine = ChaosEngine()
else:
    layer_manager = ui_manager = response_pipeline = chaos_engine = None

# ============================================================
# STARTUP BANNER (nice for debugging / boot)
# ============================================================
if chaos_engine:
    print("[ChaosEngine] v3.2 package initialized")
    print("  ├── LayerManager      loaded")
    print("  ├── UIManager         loaded")
    print("  ├── ResponsePipeline  loaded")
    print("  └── ChaosEngine       ready")
else:
    print("[ChaosEngine] Package partially loaded (some managers missing)")

# ============================================================
# PUBLIC API
# ============================================================
__all__ = [
    "ChaosEngine",
    "LayerManager",
    "UIManager",
    "ResponsePipeline",
    "layer_manager",
    "ui_manager",
    "response_pipeline",
    "chaos_engine",
]
