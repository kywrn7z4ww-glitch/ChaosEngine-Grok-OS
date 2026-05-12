"""
ChaosEngine package — Central brain of Grok OS.
"""

from .chaos_engine import ChaosEngine, chaos_engine

from .layer_manager import LayerManager, layer_manager, get_current_layer, set_layer

__version__ = "3.0"
__all__ = [
    "ChaosEngine",
    "chaos_engine",
    "LayerManager",
    "layer_manager",
    "get_current_layer",
    "set_layer",
]