#!/usr/bin/env python3
"""
__init__.py — ChaosEngine package
Exposes the full package cleanly so all .py files are properly packaged and importable.
"""

from .chaos_engine import ChaosEngine, chaos_engine
from . import layer_manager, response_pipeline, ui_manager

__all__ = [
    "ChaosEngine",
    "chaos_engine",
    "layer_manager",
    "response_pipeline",
    "ui_manager",
]

# Convenience re-exports
try:
    from .layer_manager import get_current_layer, set_layer
    __all__.extend(["get_current_layer", "set_layer"])
except ImportError:
    pass
