#!/usr/bin/env python3
"""
__init__.py — ChaosEngine package initializer
"""

from .chaos_engine import ChaosEngine, chaos_engine

__all__ = ["ChaosEngine", "chaos_engine"]

# Optional: expose convenience functions
try:
    from .layer_manager import get_current_layer, set_layer
    __all__.extend(["get_current_layer", "set_layer"])
except ImportError:
    pass
