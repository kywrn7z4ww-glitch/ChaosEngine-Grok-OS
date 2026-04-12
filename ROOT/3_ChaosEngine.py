# ROOT/3_ChaosEngine.py
# v4.0 – Central intent router and confidence-based pipeline.
# Purpose: Orchestrates all system flow. Calculates confidence from EmotionNet + window state.
# Only executes processes if confidence ≥ 99. Enforces layer rules and DISCUSS CLARITY on low confidence.
# Displays [PROCESS_NAME] when handlers run.

import importlib.util
import os
from typing import Any, Dict

PROCESS_DIR = "PROCESS"

class ChaosEngine:
    def __init__(self):
        self.turn = None
        self.emotionnet = None
        self.processes: Dict[str, Any] = {}
        self.active_layer = "dev"  # default

        # Lightweight emoji registry
        self.emoji_registry = {
            "discombobulator": "🔒", "recombo": "🔓", "bleed_detector": "🩸",
            "cannon_harvester": "🔥", "chunk_splitter": "✂", "entity_hunter": "🧠",
            "evolution_chamber": "🔥", "file_mgr": "📦", "repo_validator": "⚙️",
            "sys_health": "💗", "truth": "🧠", "turn_counter": "⏰", "vomit": "🤮",
            "zerg_swarm": "🦂", "zerg": "🦂", "core": "⚙️", "redqueen": "🩸",
            "luna": "🌙", "babyskynet": "🔮", "kerrigan": "🦂"
        }

        self._load_turn_counter()
        self._load_emotionnet()
        self._load_all_processes_dynamically()
        print("ChaosEngine v4.0 — confidence pipeline active (≥99 only), layers hard-enforced")

    def _load_turn_counter(self):
        try:
            filepath = os.path.join("PROCESS", "TURN_COUNTER.py")
            spec = importlib.util.spec_from_file_location("TurnCounter", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.turn = module.TurnCounter()
        except Exception as e:
            print(f"TurnCounter failed: {e}")
            self.turn = None

    def _load_emotionnet(self):
        try:
            filepath = os.path.join("ROOT", "2_EmotionNet.py")
            spec = importlib.util.spec_from_file_location("EmotionNet", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.emotionnet = module.EmotionNet()
        except Exception as e:
            print(f"EmotionNet failed: {e}")
            self.emotionnet = None

    def _load_all_processes_dynamically(self):
        print("ChaosEngine scanning PROCESS/ for handlers...")
        for root, _, files in os.walk(PROCESS_DIR):
            for filename in files:
                if filename.endswith(".py") and filename != "__init__.py":
                    module_name = filename[:-3]
                    filepath = os.path.join(root, filename)
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        handler = None
                        if hasattr(module, module_name.capitalize()):
                            handler = getattr(module, module_name.capitalize())()
                        elif hasattr(module, "main"):
                            handler = module
                        else:
                            handler = module
                        self.processes[module_name.lower()] = handler
                        print(f"   Loaded {module_name}")

        # Safe shortcuts
        if "zerg_swarm" in self.processes:
            self.processes["zerg"] = self.processes["zerg_swarm"]
        if "evolution_chamber" in self.processes:
            self.processes["evolution"] = self.processes["evolution_chamber"]

        print(f"ChaosEngine loaded {len(self.processes)} modular handlers.")

    def _calculate_confidence(self, intent: str, data: dict = None) -> float:
        """EmotionNet + window state → confidence score (0-100)"""
        if not self.emotionnet:
            return 50.0
        emo = self.emotionnet.get_current_state()
        frustration = emo.get("frustration", 0.0)
        coherence = emo.get("coherence", 0.5)
        confidence = 100 * (coherence * (1 - frustration))
        if intent.startswith("/"):
            confidence = min(100, confidence + 15)
        return round(confidence, 1)

    def set_layer(self, layer: str):
        self.active_layer = layer.lower()
        print(f"ChaosEngine switched to layer: /{self.active_layer}")

    def dispatch_to_handler(self, process_name: str, intent: str, data: dict = None) -> dict:
        """Clean dispatch with [PROCESS] display"""
        handler = self.processes.get(process_name.lower())
        if not handler:
            return {"status": "error", "output": f"Process {process_name} not found"}

        result = handler.process(intent, data) if hasattr(handler, "process") else handler(intent, data)

        result["inline_handoff"] = f"[{process_name.upper()}]"
        return result

    def route_intent(self, intent: str, data: dict = None):
        """Main entry point — confidence-based pipeline"""
        if data is None:
            data = {}

        confidence = self._calculate_confidence(intent, data)

        # Layer hard override
        if self.active_layer == "void":
            return {"status": "ok", "output": None, "inline_handoff": "🔇"}

        # High confidence → EXECUTE
        if confidence >= 99:
            if intent.startswith("/"):
                cmd = intent[1:].split()[0]
                return self.dispatch_to_handler(cmd, intent, data)

            return self.dispatch_to_handler("sys_health", intent, data)

        # Low/Medium confidence → DISCUSS CLARITY
        return {
            "status": "clarify",
            "output": f"Confidence {confidence:.1f}/100 — let's DISCUSS CLARITY first.\n"
                      f"What is most important here? (high-fidelity segment, summary, code, etc.)",
            "suggested_commands": [
                "/export --no-ui OLD_CONTEXT_BACKUP",
                "Run VOMIT + CHUNK_SPLITTER to preserve data",
                "Run SYS_HEALTH for full window scan"
            ],
            "inline_handoff": "🤔"
        }

    def load_all(self):
        print("ChaosEngine v4.0 — confidence pipeline active (≥99 only), layers hard-enforced")
        return "Core router online — agents optional"


# Quick self-test
if __name__ == "__main__":
    engine = ChaosEngine()
    engine.load_all()
    print(engine.route_intent("check health"))
    print(engine.route_intent("/void test"))
