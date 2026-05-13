#!/usr/bin/env python3
"""
Grok OS - Cache Manager
Slim, fast, purge-friendly in-memory + disk cache.
"""

import json
import os
from typing import Any, Dict, Optional

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "current-session.json")

def ensure_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(os.path.join(CACHE_DIR, "temp"), exist_ok=True)

def get(key: str, default: Any = None) -> Any:
    ensure_dir()
    if not os.path.exists(CACHE_FILE):
        return default
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(key, default)
    except Exception:
        return default

def set(key: str, value: Any) -> None:
    ensure_dir()
    data = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    data[key] = value
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def clear() -> None:
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    # Also clear temp/
    temp_dir = os.path.join(CACHE_DIR, "temp")
    if os.path.exists(temp_dir):
        for f in os.listdir(temp_dir):
            try:
                os.remove(os.path.join(temp_dir, f))
            except:
                pass

def get_all() -> Dict[str, Any]:
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

if __name__ == "__main__":
    print("Cache Manager ready.")
    print("Example: set('current_layer', 'casual')"
