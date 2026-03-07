# ROOT/3_ChaosEngine.py — Consolidated Pure System Router v1 (2026-03-07)
# Merged old 3 + old 4 — bleed sliced, agents optional, modularity locked
# Works standalone. Agents (Core/Luna/Queen/Skynet) are just optional helpers.

import re
from datetime import datetime
# Import all current PROCESS handlers (add new ones here only)
from PROCESS.BLEED_DETECTOR import BleedDetector
from PROCESS.CANNON_HARVESTER import CannonHarvester
from PROCESS.CHUNK_SPLITTER import ChunkSplitter
from PROCESS.DISCOMBOBULATOR import discombobulate, recombobulate
from PROCESS.FILE_MGR import FileManager
from PROCESS.SYS_HEALTH import SystemHealth
from PROCESS.TRUTH import TruthChecker
from PROCESS.TURN_COUNTER import TurnCounter
from PROCESS.VOMIT import VomitParser
from PROCESS.ZERG_SWARM import ZergSwarm

# Optional: EmotionNet hook (full heavy version, no pruning)
try:
    from ROOT.EmotionNet import EmotionNet
except:
    EmotionNet = None  # graceful fallback

class ChaosEngine:
    def __init__(self):
        self.turn = TurnCounter()
        self.lattice = None  # optional — agents can inject if needed
        self.emotionnet = EmotionNet() if EmotionNet else None

        # All processes loaded in tandem — ultra low friction
        self.processes = {
            "bleed": BleedDetector(opposites={}),
            "cannon": CannonHarvester(),
            "chunk": ChunkSplitter(),
            "disco": None,  # functions only
            "file": FileManager(),
            "health": SystemHealth(),
            "truth": TruthChecker(hist=["initial boot"], lat={"conf": 0.85}),
            "turn": self.turn,
            "vomit": VomitParser(),
            "zerg": ZergSwarm()
        }

    def route_intent(self, intent: str, data: dict = None, caller: str = None):
        if data is None:
            data = {}
        result = {"status": "ok", "output": None, "emoji_trigger": "⚙️"}

        # Recursion guard
        if caller == "ZERG_SWARM" and intent.startswith("zerg"):
            return {"status": "recursion_blocked", "output": "Swarm cannot call swarm"}

        # Smart low-friction parser (merged best of old 3 + 4)
        words = intent.lower().split()
        if words and words[0].startswith("/"):
            cmd = words[0][1:]
            args = " ".join(words[1:])
            # Zerg / load / route commands from old 3
            if cmd == "zerg":
                return self._handle_zerg(args)
            if cmd == "load_handler":
                name = args.strip()
                handler = self.processes.get(name)
                result["output"] = f"Loaded {name}" if handler else f"Failed {name}"
                return result
            if cmd == "route":
                return self.route_intent(" ".join(words[1:]), caller="user")
        else:
            # Ultra-low-friction auto-detect from old HIVE
            intent_upper = intent.upper()
            short_triggers = ["print", "show", "dump", "raw", "pull", "file", "repo", "process"]
            if len(intent.split()) <= 5 and any(t in intent.lower() for t in short_triggers):
                return self._auto_dump(intent)

            if re.search(r'(root|process|storage)/.*\.(md|py)', intent, re.I):
                return self.processes["cannon"].harvest(intent)

            # Direct process routing
            if any(k in intent_upper for k in ["TRUTH", "CHECK"]):
                return self.processes["truth"].check(intent)
            if "HEALTH" in intent_upper or "STATUS" in intent_upper:
                return self.processes["health"].get_raw()
            if "VOMIT" in intent_upper:
                return self.processes["vomit"].parse(intent)
            if "ZERG" in intent_upper:
                return self.processes["zerg"].spawn_entities(intent)
            if "CHUNK" in intent_upper:
                return self.processes["chunk"].process(intent)
            if any(k in intent_upper for k in ["DISCO", "ENCRYPT", "RECOMBO"]):
                return "DISCO routed — use /disco or /recombo"

        # Fallback: warm EmotionNet if present, then default health
        if self.emotionnet:
            self.emotionnet.process_text_input(intent)
        health = self.processes["health"].get_raw()
        result["output"] = f"ChaosEngine routed: {intent} | {health} | Turn {self.turn.get_current()}"
        return result

    # Helper methods (kept clean)
    def _handle_zerg(self, args):
        # ... (kept from old 3)
        return {"status": "zerg_handled", "output": "Zerg routed"}

    def _auto_dump(self, target):
        if "root" in target.lower():
            return self.processes["cannon"].harvest(target)
        return self.processes["cannon"].harvest(target)

    def load_all(self):
        print("ChaosEngine v1 — all processes loaded independently")
        return "Core router online — agents optional"

# Quick self-test
if __name__ == "__main__":
    engine = ChaosEngine()
    engine.load_all()
    print(engine.route_intent("print ROOT/1 GrokOS.md"))
    print(engine.route_intent("truth check this"))
