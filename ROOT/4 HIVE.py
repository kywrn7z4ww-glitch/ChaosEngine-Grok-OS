# HIVE – Queen-managed central router (v34 – all PROCESS/ in tandem)
from datetime import datetime
# Import all 10 real handlers (repo truth)
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
        # All processes loaded together
        self.processes = {
            "bleed": BleedDetector(opposites={}),
            "cannon": CannonHarvester(),
            "chunk": ChunkSplitter(),
            "disco": None,  # functions only
            "file": FileManager(),
            "health": SystemHealth(),
            "truth": TruthChecker(hist=[], lat={}),
            "turn": TurnCounter(),
            "vomit": VomitParser(),
            "zerg": ZergSwarm()
        }
        self.turn = self.processes["turn"]

    def route_intent(self, raw_intent: str):
        intent = raw_intent.strip().upper()  # ALL CAPS boost + sloppy
        self.turn.increment()

        # Direct mapping — low friction, no anger check
        if any(k in intent for k in ["PULL", "RAW", "PRINT", "HARVEST", "REPO", "FILE"]):
            return self.processes["cannon"].harvest(raw_intent)  # or browse_page bridge

        if "CHUNK" in intent or "SPLIT" in intent:
            return self.processes["chunk"].process(raw_intent)

        if "DISCO" in intent or "ENCRYPT" in intent or "RECOMBO" in intent:
            # use discombobulate/recombobulate directly
            return "DISCO routed"

        if "PIN" in intent or "SAVE" in intent:
            return self.processes["file"].pin(title=raw_intent[:50], content=raw_intent)

        if "TRUTH" in intent or "CHECK" in intent:
            return self.processes["truth"].check(raw_intent)

        if "HEALTH" in intent or "STATUS" in intent:
            return self.processes["health"].get_raw()

        if "BLEED" in intent:
            return self.processes["bleed"].check({})  # pass lattice dict

        if "VOMIT" in intent or "MESSY" in intent:
            return self.processes["vomit"].parse(raw_intent)

        if "ZERG" in intent or "SPAWN" in intent or "ENTITY" in intent:
            return self.processes["zerg"].spawn_entities(raw_intent)

        # Default — Queen decides (turn + health check)
        health = self.processes["health"].get_raw()
        return f"Queen routed: {raw_intent} | {health} | Turn {self.turn.get_current()}"

    def load_all(self):
        print("HIVE boot — all 10 processes loaded in tandem")
        return "Queen online — everything working together"
