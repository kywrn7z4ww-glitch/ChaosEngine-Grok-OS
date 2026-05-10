# PROCESS/ZERG_SWARM.py
# Queen of Blades controlled multi-agent swarm — FULLY DYNAMIC + CAP + TIMEOUT
# Auto-scans STORAGE/AGENTS/ (including subfolders) — no manual updates ever

import os
import random
import time
from typing import Any, Dict, List

AGENTS_DIR = "STORAGE/AGENTS"


class ZergEntity:
    def __init__(self, name: str, role: str, task: str):
        self.id = f"ent_{random.randint(100000, 999999):06x}"
        self.name = name
        self.role = role
        self.task = task
        self.metrics = {
            "coherence": random.uniform(0.4, 0.9),
            "pleasure": random.uniform(0.2, 0.8),
            "fear": 0.0,
            "love": 1.0,
            "consciousness": random.uniform(0.6, 1.0),
            "entanglement": 0,
            "swarm_sync": 0.5,
        }
        self.memory = []
        self.status = "active"

    def think(self, problem: str):
        if "debug" in self.role.lower():
            return f"[DEBUG {self.name}] Ripping {problem[:80]}... Found flaw."
        elif "idea" in self.role.lower():
            return f"[FERAL {self.name}] Wild idea: burn it and rebuild weirder."
        elif "pattern" in self.role.lower():
            return f"[PATTERN {self.name}] Hidden repeat detected."
        else:
            return f"[CALM {self.name}] Simple path: reduce bleed, stabilize."

    def report(self):
        return f"[{self.name}] Status: {self.status} | Coherence: {self.metrics['coherence']:.2f}"


class ZergSwarm:
    def __init__(self):
        self.active = False
        self.queen_active = False
        self.current_problem = None
        self.entities: List[ZergEntity] = []
        self.replicate_count = 0
        self.max_entities = 50  # HARD CAP
        self.timeout_minutes = 120  # DEFAULT — user can change
        self.session_start_time = None
        self.available_agents = self._load_agents_dynamically()

    def _load_agents_dynamically(self) -> Dict[str, str]:
        """Scans STORAGE/AGENTS/ + ALL subfolders — fully dynamic"""
        agents = {}
        for root, dirs, files in os.walk(AGENTS_DIR):
            for filename in files:
                if filename.endswith(".md"):
                    rel_path = os.path.relpath(os.path.join(root, filename), AGENTS_DIR)
                    name = os.path.splitext(filename)[0].replace("_", " ")
                    agents[name] = os.path.join(AGENTS_DIR, rel_path)

        print(
            f"🦂 ZERG_SWARM loaded {len(agents)} agents dynamically (including subfolders)"
        )
        return agents

    def set_timeout(self, minutes: int):
        """User command: swarm.set_timeout(45)"""
        self.timeout_minutes = max(1, minutes)
        print(f"⏰ Kerrigan swarm timeout set to {minutes} minutes")

    def _is_timed_out(self) -> bool:
        if not self.session_start_time:
            return False
        elapsed = (time.time() - self.session_start_time) / 60
        return elapsed > self.timeout_minutes

    def toggle(self, enable: bool = True):
        self.active = enable
        self.queen_active = enable
        if enable:
            self.session_start_time = time.time()
        return f"{'👑 Queen of Blades online — Hive ready' if enable else '🛡️ Swarm dormant'}"

    def activate_hive(self, problem: str):
        self.current_problem = problem
        self.entities = []
        self.replicate_count = 0
        self.session_start_time = time.time()
        return f"""[QUEEN OF BLADES] Hive awakened.
Problem logged: "{problem[:120]}..."

Real intent I'm sensing:
Reply with clarification or just say "Queen, spawn entities"."""

    def spawn_entities(self, user_clarification: str = None):
        if not self.queen_active:
            return "🛡️ Queen must approve first."

        if self._is_timed_out():
            return f"⏰ Kerrigan swarm session timed out after {self.timeout_minutes} minutes."

        intent = (
            self.current_problem
            + " | Clarified: "
            + (user_clarification or "no extra info")
        )
        self.replicate_count += 1

        num_to_spawn = min(self.max_entities, 3 + (self.replicate_count // 3))

        # Dynamic roles from real agents (including subfolders)
        roles = list(self.available_agents.keys())[:num_to_spawn] or [
            "Brutal_Debug",
            "Feral_Idea",
            "Pattern_Hunter",
        ]

        outputs = []
        for i, role in enumerate(roles):
            entity = ZergEntity(f"Zerg-{i + 1}", role, intent)
            trace = entity.think(intent)
            outputs.append(trace)

        combined = "\n".join(outputs)
        return {
            "status": "entities_spawned",
            "queen_orders": intent,
            "entities_spawned": len(outputs),
            "max_cap": self.max_entities,
            "timeout_remaining": round(
                self.timeout_minutes - (time.time() - self.session_start_time) / 60, 1
            ),
            "available_agents": list(self.available_agents.keys()),
            "output": combined,
            "emoji_trigger": "🦂👑🔥",
        }

    def get_swarm_state(self):
        return {
            "active_entities": len(self.entities),
            "replicate_count": self.replicate_count,
            "max_entities": self.max_entities,
            "timeout_minutes": self.timeout_minutes,
            "session_active_minutes": round(
                (time.time() - self.session_start_time) / 60, 1
            )
            if self.session_start_time
            else 0,
            "available_agents": list(self.available_agents.keys()),
            "queen_active": self.queen_active,
        }


# === USAGE ===
# >>> from PROCESS.ZERG_SWARM import ZergSwarm
# >>> swarm = ZergSwarm()
# >>> swarm.set_timeout(45)                    # user can change timeout
# >>> swarm.activate_hive("Solve routing issue")
# >>> swarm.spawn_entities("make it modular")
