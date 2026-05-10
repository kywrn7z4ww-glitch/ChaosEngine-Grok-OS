import importlib.util
import os
from typing import Any, Dict

PROCESS_DIR = "PROCESS"

class ChaosEngine:
    def __init__(self):
        self.turn = None
        self.emotionnet = None
        self.processes: Dict[str, Any] = {}

        # Lightweight emoji registry — fires automatically (processes can override)
        self.emoji_registry = {
            "discombobulator": "🔒",      # disco start
            "recombo": "🔓",              # recombobulate success
            "bleed_detector": "🩸",
            "cannon_harvester": "🔥",
            "chunk_splitter": "✂",
            "entity_hunter": "🧠",
            "evolution_chamber": "🔥",
            "file_mgr": "📦",
            "repo_validator": "⚙️",
            "sys_health": "💗",
            "truth": "🧠",
            "turn_counter": "⏰",
            "vomit": "🤮",
            "zerg_swarm": "🦂",           # future swarm emoji
            "zerg": "🦂",
            "core": "⚙️",
            "redqueen": "🩸",
            "luna": "🌙",
            "babyskynet": "⚡️",
            "kerrigan": "🦂"
        }

        self._load_turn_counter()
        self._load_emotionnet()
        self._load_all_processes_dynamically()
        print("ChaosEngine v3.0 — rebuilt modular, emojis fire inline, Decision Kernel aware")

    def _load_turn_counter(self):
        try:
            filepath = os.path.join("PROCESS", "TURN_COUNTER.py")
            spec = importlib.util.spec_from_file_location("TurnCounter", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.turn = module.TurnCounter()
            print("TurnCounter loaded dynamically")
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
            print("EmotionNet loaded dynamically")
        except Exception as e:
            print(f"EmotionNet failed: {e}")
            self.emotionnet = None

    def _load_all_processes_dynamically(self):
        """Fully modular auto-discovery — core of the system"""
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

    def dispatch_to_handler(self, cls: str, intent: str, data: dict = None) -> dict:
        """Clean registry dispatch — emojis fire inline automatically"""
        if data is None:
            data = {}
        handler = self.processes.get(cls)
        result = {"status": "ok", "output": None, "inline_handoff": "⚙️"}  # default cog

        if handler and hasattr(handler, "route_intent"):
            result = handler.route_intent(intent, data)
        elif handler and callable(handler):
            result = handler(intent, data)

        # Guarantee emoji fires — process can override by returning its own key
        if "inline_handoff" not in result or not result.get("inline_handoff"):
            result["inline_handoff"] = self.emoji_registry.get(cls, "⚙️")

        # Special Discombobulator logic (🔒 vs 🔓)
        if cls == "discombobulator":
            result["inline_handoff"] = "🔓" if "recombo" in intent.lower() else "🔒"

        return result

    def route_intent(self, intent: str, data: dict = None, caller: str = None):
        """Agentic path only — emojis guaranteed to fire"""
        if data is None:
            data = {}
        result = {"status": "ok", "output": None, "inline_handoff": "⚙️"}

        words = intent.lower().split()
        if words and words[0].startswith("/"):
            cmd = words[0][1:]
            args = " ".join(words[1:])
            if cmd in ["disco", "recombo"]:
                return self.dispatch_to_handler("discombobulator", args, data)
            return self.dispatch_to_handler(cmd, args, data)

        # Direct keyword fallbacks (still modular)
        intent_upper = intent.upper()
        if ("TRUTH" in intent_upper or "CHECK" in intent_upper) and "truth" in self.processes:
            return self.processes["truth"].check(intent)
        if ("HEALTH" in intent_upper or "STATUS" in intent_upper) and "sys_health" in self.processes:
            return self.processes["sys_health"].get_raw()
        if "VOMIT" in intent_upper and "vomit" in self.processes:
            return self.processes["vomit"].parse(intent)
        if "CHUNK" in intent_upper and "chunk_splitter" in self.processes:
            return self.processes["chunk_splitter"].process(intent)

        result["output"] = f"ChaosEngine (Agentic) routed: {intent} | Turn active"
        return result

    def get_roleplay_emotion(self, character_type: str, user_text: str):
        if self.emotionnet:
            return self.emotionnet.get_roleplay_emotion(character_type, user_text)
        return {"default": 0.5}

    def load_all(self):
        print("ChaosEngine v3.0 — rebuilt modular, emojis fire inline")
        return "Core router online — agents optional"


# Quick self-test
if __name__ == "__main__":
    engine = ChaosEngine()
    engine.load_all()
    print(engine.route_intent("/disco test blob"))
    print(engine.route_intent("health check"))
