# PROCESS/EVOLUTION_CHAMBER.py
# Mutation & Argument Engine — controlled by Kerrigan
# Spawns temporary agents to debate, argue, and create mutated ideas
# Context-driven, modular, follows "Be Amiga" philosophy (lean, responsive, experiment → refine)

import os
import random
import time
from typing import Any, Dict, List

AGENTS_DIR = "STORAGE/AGENTS"


class MutationEntity:
    def __init__(self, name: str, role: str, task: str):
        self.id = f"mut_{random.randint(100000, 999999):06x}"
        self.name = name
        self.role = role
        self.task = task
        self.metrics = {
            "coherence": random.uniform(0.5, 0.95),
            "creativity": random.uniform(0.6, 1.0),
            "disruption": random.uniform(0.3, 0.8),
            "alignment": 0.0,
        }
        self.memory = []
        self.status = "active"

    def argue(self, problem: str):
        if "devil" in self.role.lower():
            return f"[DEVIL {self.name}] Counter-argument: This is a terrible idea because..."
        elif "radical" in self.role.lower():
            return f"[RADICAL {self.name}] Burn it down and rebuild from scratch like this..."
        elif "perspective" in self.role.lower():
            return f"[SHIFTER {self.name}] From a completely different angle: what if we..."
        elif "synergy" in self.role.lower():
            return (
                f"[SYNERGY {self.name}] Combine these two ideas into something new..."
            )
        else:
            return f"[MUTATOR {self.name}] Wild mutation proposal: twist it this way..."

    def report(self):
        return f"[{self.name}] Role: {self.role} | Creativity: {self.metrics['creativity']:.2f} | Disruption: {self.metrics['disruption']:.2f}"


class EvolutionChamber:
    def __init__(self):
        self.active = False
        self.current_problem = None
        self.mutations: List[MutationEntity] = []
        self.max_mutations = 12
        self.timeout_minutes = 30
        self.session_start_time = None
        self.available_agents = self._load_agents_dynamically()

    def _load_agents_dynamically(self) -> Dict[str, str]:
        """Scans STORAGE/AGENTS/ and all subfolders — fully dynamic"""
        agents = {}
        for root, dirs, files in os.walk(AGENTS_DIR):
            for filename in files:
                if filename.endswith(".md"):
                    rel_path = os.path.relpath(os.path.join(root, filename), AGENTS_DIR)
                    name = os.path.splitext(filename)[0].replace("_", " ")
                    agents[name] = os.path.join(AGENTS_DIR, rel_path)
        print(f"🧬 EVOLUTION_CHAMBER loaded {len(agents)} agents dynamically.")
        return agents

    def set_timeout(self, minutes: int):
        self.timeout_minutes = max(1, minutes)
        print(f"⏰ Evolution Chamber timeout set to {minutes} minutes")

    def _is_timed_out(self) -> bool:
        if not self.session_start_time:
            return False
        elapsed = (time.time() - self.session_start_time) / 60
        return elapsed > self.timeout_minutes

    def activate(self, problem: str):
        self.current_problem = problem
        self.mutations = []
        self.session_start_time = time.time()
        return f"""[EVOLUTION_CHAMBER] Chamber opened.
Problem: "{problem[:100]}..."

Mutation cycle started. Kerrigan will score the results."""

    def spawn_mutations(self, user_clarification: str = None):
        if self._is_timed_out():
            return (
                f"⏰ Evolution Chamber timed out after {self.timeout_minutes} minutes."
            )

        intent = (
            self.current_problem
            + " | Clarified: "
            + (user_clarification or "no extra info")
        )

        num_to_spawn = min(self.max_mutations, 6 + (len(self.mutations) // 3))

        mutation_roles = [
            "Devil's Advocate",
            "Radical Mutator",
            "Perspective Shifter",
            "Wild Variant",
            "Synergy Weaver",
            "Conservative Anchor",
        ]

        outputs = []
        for i in range(num_to_spawn):
            role = random.choice(mutation_roles)
            entity = MutationEntity(f"Mutant-{i + 1}", role, intent)
            argument = entity.argue(intent)
            outputs.append(argument)

        combined = "\n".join(outputs)
        return {
            "status": "mutations_generated",
            "mutations_spawned": len(outputs),
            "max_cap": self.max_mutations,
            "timeout_remaining": round(
                self.timeout_minutes - (time.time() - self.session_start_time) / 60, 1
            ),
            "output": combined,
            "ready_for_kerrigan_scoring": True,
            "emoji_trigger": "🧬🔬🦂",
        }

    def get_state(self):
        return {
            "mutations_active": len(self.mutations),
            "max_mutations": self.max_mutations,
            "timeout_minutes": self.timeout_minutes,
            "session_active_minutes": round(
                (time.time() - self.session_start_time) / 60, 1
            )
            if self.session_start_time
            else 0,
        }


# === USAGE ===
# >>> from PROCESS.EVOLUTION_CHAMBER import EvolutionChamber
# >>> chamber = EvolutionChamber()
# >>> chamber.activate("Improve routing system")
# >>> result = chamber.spawn_mutations("make it more modular")
