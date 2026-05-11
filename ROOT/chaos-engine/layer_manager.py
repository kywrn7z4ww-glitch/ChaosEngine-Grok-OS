#!/usr/bin/env python3
"""
layer_manager.py — Layer Manager v1.2
Purpose: Tracks and switches active layers (/casual, /dev, /roleplay, /void, /export).
"""

_current_layer = "dev"


def get_current_layer() -> str:
    return _current_layer


def set_layer(layer: str):
    global _current_layer
    _current_layer = layer.lower().strip("/")
    print(f"📍 Layer switched to: /{_current_layer}")


def list_layers() -> list:
    return ["casual", "dev", "roleplay", "void", "export"]


# Global instance
layer_manager = None
try:
    layer_manager = type("LayerManager", (), {
        "get_current_layer": get_current_layer,
        "set_layer": set_layer,
        "list_layers": list_layers,
    })()
except:
    pass
