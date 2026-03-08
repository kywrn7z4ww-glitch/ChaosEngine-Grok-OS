import importlib.util
import os

PROCESS_DIR = "PROCESS"


class ChaosEngine:
    def __init__(self):
        self.turn = None
        self.lattice = None
        self.emotionnet = None
        self.processes = {}

        self._load_turn_counter()
        self._load_emotionnet()
        self._load_all_processes_dynamically()

    def _load_turn_counter(self):
        try:
            filepath = os.path.join("PROCESS", "TURN_COUNTER.py")
            spec = importlib.util.spec_from_file_location("TurnCounter", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.turn = module.TurnCounter()
            print("⏰ TurnCounter loaded dynamically")
        except Exception as e:
            print(f"⚠️ TurnCounter failed: {e}")
            self.turn = None

    def _load_emotionnet(self):
        try:
            filepath = os.path.join("ROOT", "2_EmotionNet.py")
            spec = importlib.util.spec_from_file_location("EmotionNet", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.emotionnet = module.EmotionNet()
            print("🧠 EmotionNet loaded dynamically")
        except Exception as e:
            print(f"⚠️ EmotionNet failed: {e}")
            self.emotionnet = None

    def _load_all_processes_dynamically(self):
        """Auto-discovers every .py in PROCESS/"""
        print("🛠️ ChaosEngine scanning PROCESS/ for handlers...")
        for root, dirs, files in os.walk(PROCESS_DIR):
            for filename in files:
                if filename.endswith(".py") and filename != "__init__.py":
                    module_name = filename[:-3]
                    filepath = os.path.join(root, filename)
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        if hasattr(module, module_name.capitalize()):
                            handler = getattr(module, module_name.capitalize())()
                            self.processes[module_name.lower()] = handler
                        elif hasattr(module, "main"):
                            self.processes[module_name.lower()] = module
                        else:
                            self.processes[module_name.lower()] = module

                        print(f"   ✓ Loaded {module_name}")

        # Special shortcuts
        if "zerg_swarm" in self.processes:
            self.processes["zerg"] = self.processes["zerg_swarm"]
        if "evolution_chamber" in self.processes:
            self.processes["evolution"] = self.processes["evolution_chamber"]

        print(f"✅ ChaosEngine loaded {len(self.processes)} handlers dynamically.")

    def route_intent(self, intent: str, data: dict = None, caller: str = None):
        if data is None:
            data = {}
        result = {"status": "ok", "output": None, "emoji_trigger": "⚙️"}

        # Swarm / Kerrigan / Evolution special route
        if any(x in intent.lower() for x in ["kerrigan", "swarm", "zerg", "evolution"]):
            if "zerg" in self.processes:
                return (
                    self.processes["zerg"].spawn_entities(intent)
                    if "spawn" in intent.lower()
                    else self.processes["zerg"].activate_hive(intent)
                )
            if "evolution" in self.processes:
                return self.processes["evolution"].spawn_mutations(intent)

        # Smart low-friction parser
        words = intent.lower().split()
        if words and words[0].startswith("/"):
            cmd = words[0][1:]
            args = " ".join(words[1:])
            if cmd in self.processes:
                handler = self.processes[cmd]
                if hasattr(handler, "route_intent"):
                    return handler.route_intent(args)
                elif callable(handler):
                    return handler(args)
                else:
                    return {"status": "ok", "output": f"Handler {cmd} activated"}

        else:
            # Direct keyword routing — safe fallbacks
            intent_upper = intent.upper()
            if (
                "TRUTH" in intent_upper or "CHECK" in intent_upper
            ) and "truth" in self.processes:
                return self.processes["truth"].check(intent)
            if (
                "HEALTH" in intent_upper or "STATUS" in intent_upper
            ) and "health" in self.processes:
                return self.processes["health"].get_raw()
            if "VOMIT" in intent_upper and "vomit" in self.processes:
                return self.processes["vomit"].parse(intent)
            if "CHUNK" in intent_upper and "chunk" in self.processes:
                return self.processes["chunk"].process(intent)

        # Final safe fallback
        result["output"] = f"ChaosEngine routed: {intent} | Turn active"
        return result

    def get_roleplay_emotion(self, character_type: str, user_text: str):
        """Bridge for Luna / roleplay — routes through EmotionNet"""
        if self.emotionnet:
            return self.emotionnet.get_roleplay_emotion(character_type, user_text)
        return {"default": 0.5}

    def load_all(self):
        print("ChaosEngine v2 — dynamic process loading complete")
        return "Core router online — agents optional"


# Quick self-test
if __name__ == "__main__":
    engine = ChaosEngine()
    engine.load_all()
    print(engine.route_intent("print ROOT/1_GrokOS_Boot.md"))
    print(engine.route_intent("kerrigan spawn entities"))
