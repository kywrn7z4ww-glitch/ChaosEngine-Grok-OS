#!/usr/bin/env python3
"""
================================================================================
ROOT/3_ChaosEngine.py — Central Intent Router & Dynamic Bridge (v5.0)
ChaosEngine Grok OS — The Real Functional Bridge
================================================================================

PURPOSE:
This is the **actual brain** of the system. It:
- Loads EmotionNet (emotional state)
- Dynamically discovers and loads all PROCESS/ modules
- Routes user intent to the correct handler based on current layer
- Calculates confidence before executing anything
- Acts as the bridge between the poetic `1_GrokOS.py` and real tools

This file should remain relatively clean and focused on routing + loading.
Heavy logic belongs in the individual PROCESS/ files.

================================================================================
"""

import os
import importlib.util
from typing import Any, Dict, Optional
from pathlib import Path

# Agent loader (optional - gracefully degrades if not present)
try:
    from STORAGE.AGENTS.AGENT_LOADER import load_agent, list_all_agents
    AGENT_LOADER_AVAILABLE = True
except ImportError:
    AGENT_LOADER_AVAILABLE = False

# =============================================================================
# CONFIG
# =============================================================================
PROCESS_DIR = Path("PROCESS")
ROOT_DIR = Path("ROOT")


class ChaosEngine:
    def __init__(self):
        self.turn = None
        self.emotionnet = None
        self.processes: Dict[str, Any] = {}
        self.active_layer: str = "dev"

        self._load_emotionnet()
        self._load_all_processes_dynamically()

        print("⚙️  ChaosEngine v5.0 — Intent Router Online (≥99% confidence gate)")

    # -------------------------------------------------------------------------
    # LOADING
    # -------------------------------------------------------------------------
    def _load_emotionnet(self):
        """Load EmotionNet from ROOT/2_EmotionNet.py"""
        try:
            filepath = ROOT_DIR / "2_EmotionNet.py"
            if not filepath.exists():
                print("⚠️  2_EmotionNet.py not found — emotional state disabled")
                return

            spec = importlib.util.spec_from_file_location("EmotionNet", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.emotionnet = module.EmotionNet()
            print("🧠 EmotionNet loaded")
        except Exception as e:
            print(f"⚠️  Could not load EmotionNet: {e}")

    def _load_all_processes_dynamically(self):
        """Auto-discover and load every .py file in PROCESS/ as a module"""
        print("🔍 Scanning PROCESS/ for handlers...")
        if not PROCESS_DIR.exists():
            print("⚠️  PROCESS/ folder not found")
            return

        loaded = 0
        for file in PROCESS_DIR.glob("*.py"):
            if file.name.startswith("__"):
                continue

            module_name = file.stem
            try:
                spec = importlib.util.spec_from_file_location(module_name, file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Try to get the main class (e.g. TruthValidator, Stitcher, etc.)
                handler = None
                if hasattr(module, module_name):
                    handler = getattr(module, module_name)()
                elif hasattr(module, "main"):
                    handler = module
                else:
                    handler = module  # fallback to module itself

                self.processes[module_name.lower()] = handler
                loaded += 1
            except Exception as e:
                print(f"  ❌ Failed to load {module_name}: {e}")

        print(f"✅ Loaded {loaded} process handlers dynamically")

    # -------------------------------------------------------------------------
    # ROUTING
    # -------------------------------------------------------------------------
    def _calculate_confidence(self, intent: str) -> float:
        """Simple confidence scoring (expand later with real EmotionNet)"""
        base = 75.0
        if intent.startswith("/"):
            base += 15
        if self.emotionnet:
            # Future: use real emotional state
            pass
        return min(100.0, base)

    def route_intent(self, intent: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Main entry point — routes user intent to the correct process"""
        if data is None:
            data = {}

        confidence = self._calculate_confidence(intent)

        # Hard layer override
        if self.active_layer == "void":
            return {"status": "ok", "output": None, "inline_handoff": "🔇"}

        # High confidence → execute
        if confidence >= 99:
            cmd = intent[1:].split()[0] if intent.startswith("/") else "sys_health"
            handler = self.processes.get(cmd.lower())
            if handler:
                result = handler.process(data) if hasattr(handler, "process") else handler
                return {"status": "executed", "process": cmd, "result": result}
            else:
                return {"status": "unknown_command", "command": cmd}

        # Low confidence → force clarification
        return {
            "status": "clarify",
            "message": f"Confidence {confidence:.1f}% — DISCUSS CLARITY required",
            "suggestions": ["Run /help", "Try /dev for debugging", "Use /casual for general chat"]
        }

    def set_layer(self, layer: str):
        self.active_layer = layer.lower()
        print(f"📍 Layer switched to: /{self.active_layer}")

    def load_agent(self, name: str) -> str:
        """Load an agent using the dynamic AGENT_LOADER (if available)"""
        if AGENT_LOADER_AVAILABLE:
            return load_agent(name)
        else:
            return f"⚠️ Agent loader not available. Cannot load '{name}'."

    def list_agents(self) -> list:
        """Return list of all available agents"""
        if AGENT_LOADER_AVAILABLE:
            return list_all_agents()
        else:
            return []

    def load_all(self):
        """Explicitly load everything (called by 1_GrokOS.py)"""
        print("🔄 ChaosEngine fully initialized")
        return "Bridge active — ready to route intent"


# Quick self-test
if __name__ == "__main__":
    engine = ChaosEngine()
    engine.load_all()
    print(engine.route_intent("/boot"))
    print(engine.route_intent("check system health"))
