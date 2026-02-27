# ROOT/4 – HIVE v41 – ALL FIT HERE
# Queen central – all PROCESS loaded – ultra low friction auto-dump

from datetime import datetime
import re

# === Import all 10 real PROCESS handlers (repo truth) ===
from PROCESS.BLEED_DETECTOR import BleedDetector
from PROCESS.CANNON_HARVESTER import CannonHarvester  # your fixed version
from PROCESS.CHUNK_SPLITTER import ChunkSplitter
from PROCESS.DISCOMBOBULATOR import discombobulate, recombobulate
from PROCESS.FILE_MGR import FileManager
from PROCESS.SYS_HEALTH import SystemHealth
from PROCESS.TRUTH import TruthChecker
from PROCESS.TURN_COUNTER import TurnCounter
from PROCESS.VOMIT import VomitParser
from PROCESS.ZERG_SWARM import ZergSwarm


class HiveManager:
    def __init__(self):
        self.queen_active = True
        # All 10 processes loaded together in tandem
        self.processes = {
            "bleed": BleedDetector(opposites={}),
            "cannon": CannonHarvester(),
            "chunk": ChunkSplitter(),
            "disco": None,  # functions only
            "file": FileManager(),
            "health": SystemHealth(),
            "truth": TruthChecker(
                hist=["initial boot sequence"],
                lat={"conf": 0.85, "surprise": 0.15, "frustr": 0.0, "ache": 0.0}
            ),
            "turn": TurnCounter(),
            "vomit": VomitParser(),
            "zerg": ZergSwarm()
        }
        self.turn = self.processes["turn"]

    def route_intent(self, raw_intent: str):
        self.turn.increment()
        intent_upper = raw_intent.strip().upper()

        # === ULTRA LOW FRICTION – auto-detect & dump ===
        # 1. Short command with trigger word → auto raw
        short_triggers = ["print", "show", "dump", "raw", "pull", "file", "repo", "process"]
        if len(raw_intent.split()) <= 5 and any(t in raw_intent.lower() for t in short_triggers):
            target = raw_intent.strip()
            if "root" in target.lower():
                return self._fetch_root_file(target)
            elif "process" in target.lower():
                return self._fetch_process_file(target)
            # fallback to cannon harvester
            return self.processes["cannon"].harvest(target)

        # 2. Looks like a path → instant raw dump
        if re.search(r'(root|process|storage)/.*\.(md|py)', raw_intent, re.I):
            return self.processes["cannon"].harvest(raw_intent)

        # === Normal direct mapping – no anger/vibe check ===
        if any(k in intent_upper for k in ["PULL", "RAW", "PRINT", "HARVEST", "REPO", "FILE"]):
            return self.processes["cannon"].harvest(raw_intent)

        if "CHUNK" in intent_upper or "SPLIT" in intent_upper:
            return self.processes["chunk"].process(raw_intent)

        if "DISCO" in intent_upper or "ENCRYPT" in intent_upper or "RECOMBO" in intent_upper:
            return "DISCO routed – use /disco <text> or /recombo <blob>"

        if "PIN" in intent_upper or "SAVE" in intent_upper:
            return self.processes["file"].pin(title=raw_intent[:50], content=raw_intent)

        # ────────────────────────────────
        # TRUTH / ANCHOR TRIGGERS (upgraded – external verification cascade)
        # ────────────────────────────────
        if "TRUTH" in intent_upper or "CHECK" in intent_upper:
            escalate = any(k in intent_upper for k in [
                "ANCHOR", "VERIFY", "GROK TRUTH", "WIKI TRUTH", "PERP TRUTH", "TRUTH ESCALATE"
            ])
            pri = "grok"  # default xAI layer
            if "WIKI" in intent_upper:
                pri = "wiki"
            if "PERP" in intent_upper:
                pri = "perp"
            if "ALL" in intent_upper or "ESCALATE" in intent_upper:
                pri = "all"  # force full cascade

            truth_result = self.processes["truth"].check(
                raw_intent,
                escalate=escalate,
                anchor_pri=pri
            )

            # Safety: add external delta if not present and escalated
            if escalate and "External anchor delta" not in truth_result:
                topic = self._extract_topic(raw_intent)
                external = self.processes["truth"]._anchor_external(raw_intent, topic, pri)
                truth_result += f"\n{external}"

            return truth_result + f" | Turn {self.turn.get_current()}"

        if "HEALTH" in intent_upper or "STATUS" in intent_upper:
            return self.processes["health"].get_raw()

        if "BLEED" in intent_upper:
            return self.processes["bleed"].check({})  # pass real lattice dict when available

        if "VOMIT" in intent_upper or "MESSY" in intent_upper:
            return self.processes["vomit"].parse(raw_intent)

        if "ZERG" in intent_upper or "SPAWN" in intent_upper or "ENTITY" in intent_upper:
            return self.processes["zerg"].spawn_entities(raw_intent)

        # Default – Queen decides with health check
        health = self.processes["health"].get_raw()
        return f"Queen routed: {raw_intent} | {health} | Turn {self.turn.get_current()}"

    # === Helper stubs for auto-fetch (replace with real browse_page later) ===
    def _fetch_root_file(self, target):
        guessed = self._guess_path(target, "ROOT")
        if guessed:
            return self.processes["cannon"].harvest(guessed)
        return "no matching ROOT file found"

    def _fetch_process_file(self, target):
        guessed = self._guess_path(target, "PROCESS")
        if guessed:
            return self.processes["cannon"].harvest(guessed)
        return "no matching PROCESS handler found"

    def _guess_path(self, target, prefix):
        # simple guess – clean up user input to match repo naming
        clean = target.lower().replace(" ", "").replace(".py", "").replace(".md", "")
        if prefix == "ROOT":
            known = ["1 grokos.md", "2 emotionnet.py", "3 chaosengine.py", "4 chaosmanager.py", "5 full-repo-index.md", "emojiiPalette.md", "futurepatches.md"]
        else:  # PROCESS
            known = ["bleed_detector.py", "cannon_harvester.py", "chunk_splitter.py", "discombobulator.py", "file_mgr.py", "sys_health.py", "truth.py", "turn_counter.py", "vomit.py", "zerg_swarm.py"]
        for k in known:
            if clean in k or any(word in clean for word in k.split("_")):
                return f"{prefix}/{k}"
        return None

    def _extract_topic(self, text: str) -> str:
        sentences = re.split(r'[.!?]+', text)[:3]
        for s in sentences:
            words = re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', s)
            if words:
                return '_'.join(words[:4])
        return "unknown_topic"

    def load_all(self):
        print("HIVE boot — all 10 processes loaded in tandem")
        return "Queen online – everything working together"


# === Quick self-test ===
if __name__ == "__main__":
    hive = HiveManager()
    hive.load_all()
    print("\nTest commands:")
    print(hive.route_intent("ROOT/1 GrokOS.md"))
    print(hive.route_intent("print process/zerg_swarm.py"))
    print(hive.route_intent("truth check this is a test"))
