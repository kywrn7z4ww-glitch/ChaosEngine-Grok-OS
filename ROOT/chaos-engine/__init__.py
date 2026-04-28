"""
ChaosEngine v3.2 — Package Initializer (FIXED)
Matches actual exports from layer_manager.py, ui_manager.py, response_pipeline.py
"""

# ============================================================
# IMPORT INSTANCES (not classes)
# ============================================================
try:
    from .chaos_engine import ChaosEngine, chaos_engine
    from .layer_manager import get_current_layer, layer_manager, set_layer
    from .response_pipeline import process_input, response_pipeline
    from .ui_manager import format_output, ui_manager
except ImportError as e:
    print(f"[ChaosEngine] Warning: Could not import: {e}")
    chaos_engine = layer_manager = ui_manager = response_pipeline = None

# ============================================================
# STARTUP BANNER
# ============================================================
print("[ChaosEngine] v3.2 package initialized (chain-fire mode)")
if chaos_engine:
    print("  ✅ ChaosEngine       ready")
if layer_manager:
    print("  ✅ LayerManager      ready")
if ui_manager:
    print("  ✅ UIManager         ready")
if response_pipeline:
    print("  ✅ ResponsePipeline  ready")

# ============================================================
# PUBLIC API
# ============================================================
__all__ = [
    "ChaosEngine",
    "chaos_engine",
    "layer_manager",
    "get_current_layer",
    "set_layer",
    "ui_manager",
    "format_output",
    "response_pipeline",
    "process_input",
]
