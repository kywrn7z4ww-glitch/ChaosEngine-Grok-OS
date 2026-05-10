#!/usr/bin/env python3
"""
layer_manager.py — Layer Manager v1.0
Purpose: Tracks and manages the current active layer for Grok OS.
"""

from typing import Optional, Set
from pathlib import Path

# Default layer
DEFAULT_LAYER = "casual"

# Auto-discover available layers from filesystem (modular design)
LAYERS_DIR = Path("/home/workdir/artifacts/grok-os/LAYERS")


def discover_available_layers() -> Set[str]:
    """Dynamically scan LAYERS/ folder for available layers"""
    if not LAYERS_DIR.exists():
        return {DEFAULT_LAYER}

    layers = set()
    for item in LAYERS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("__"):
            layers.add(item.name)
    return layers if layers else {DEFAULT_LAYER}


class LayerManager:
    def __init__(self):
        self._current_layer: str = DEFAULT_LAYER
        self._previous_layer: Optional[str] = None
        self._available_layers: Set[str] = discover_available_layers()

    @property
    def current_layer(self) -> str:
        return self._current_layer

    @property
    def available_layers(self) -> Set[str]:
        """Self-check: always returns currently available layers"""
        self._available_layers = discover_available_layers()
        return self._available_layers

    def set_layer(self, layer: str) -> bool:
        """Switch to a new layer"""
        layer = layer.lower().strip("/")

        # Self-check for available layers
        available = self.available_layers
        if layer not in available:
            print(f"⚠️ Invalid layer: {layer} (available: {sorted(available)})")
            return False

        self._previous_layer = self._current_layer
        self._current_layer = layer
        print(f"✅ Layer switched: /{self._previous_layer} → /{self._current_layer}")
        return True

    def get_previous_layer(self) -> Optional[str]:
        return self._previous_layer

    def is_valid_layer(self, layer: str) -> bool:
        return layer.lower().strip("/") in self.available_layers

    def reset_to_default(self):
        self._current_layer = DEFAULT_LAYER
        print(f"✅ Layer reset to /{DEFAULT_LAYER}")


# Global instance (used by ChaosEngine)
layer_manager = LayerManager()


def get_current_layer() -> str:
    """Convenience function"""
    return layer_manager.current_layer


def set_layer(layer: str) -> bool:
    """Convenience function"""
    return layer_manager.set_layer(layer)
