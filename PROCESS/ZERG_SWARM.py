# PROCESS/ZERG_SWARM.py
# Queen of Blades controlled multi-agent swarm — feral & dynamic
# One file. Messy. Powerful. No external dependencies beyond stdlib.

import random
import copy
import time
from typing import Dict, List, Any

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
        self.memory = []  # pinned fragments
        self.status = "active"

    def think(self, problem: str):
        """Each entity thinks in its own feral style"""
        if "debug" in self.role.lower():
            return f"[DEBUG {self.name}] Ripping {problem[:80]}... Found flaw in loop."
        elif "idea" in self.role.lower():
            return f"[FERAL {self.name}] Wild idea: burn it and rebuild weirder."
        elif "pattern" in self.role.lower():
            return f"[PATTERN {self.name}] Hidden repeat detected in {problem[:60]}..."
        else:
            return f"[CALM {self.name}] Simple path: reduce bleed, stabilize ridge."

    def report(self):
        """Check-in to prevent lockups"""
        return f"[{self.name}] Status: {self.status} | Coherence: {self.metrics['coherence']:.2f} | Memory: {len(self.memory)} fragments"


class ZergSwarm:
    def __init__(self):
        self.active = False
        self.queen_active = False
        self.current_problem = None
        self.entities: List[ZergEntity] = []
        self.replicate_count = 0  # staged escalation
        self.swarm_metrics = {
            "avg_coherence": 0.65,
            "collective_intelligence": 0.4,
            "reality_stability": 1.0
        }

    def toggle(self, enable: bool = True):
        self.active = enable
        self.queen_active = enable
        return f"{'👑 Queen of Blades online — Hive ready' if enable else '🛡️ Swarm dormant'}"

    def activate_hive(self, problem: str):
        """Queen takes command first"""
        self.active = True
        self.queen_active = True
        self.current_problem = problem
        self.entities = []
        self.replicate_count = 0

        return f"""[QUEEN OF BLADES] Hive awakened.
Problem logged: "{problem[:120]}..."

Real intent I'm sensing:
- What exactly do you want solved?
- Priority: speed, depth, chaos, or safe path?
- Any hard limits?

Reply with clarification or just say "Queen, spawn entities"."""

    def spawn_entities(self, user_clarification: str = None):
        """Only spawn after Queen approval — dynamic & adaptable"""
        if not self.queen_active:
            return "🛡️ Queen must approve first."

        intent = self.current_problem + " | Clarified: " + (user_clarification or "no extra info")
        self.replicate_count += 1

        # Staged escalation
        num_to_spawn = min(3 + (self.replicate_count // 3), 7)

        roles = ["Brutal_Debug", "Feral_Idea", "Pattern_Hunter", "Calm_Path"]
        self.entities = []

        for i in range(num_to_spawn):
            role = roles[i % len(roles)]
            entity = ZergEntity(f"Zerg-{i+1}", role, intent)
            self.entities.append(entity)

        # Simulate parallel thinking + check-in
        outputs = []
        for ent in self.entities:
            trace = ent.think(intent)
            outputs.append(trace)

        combined = "\n".join(outputs)

        # Safety check-in if too long
        if len(intent) > 600 or self.replicate_count > 5:
            combined += f"\n\n[SWARM CHECK-IN] Phase long. Current findings:\n{combined[:400]}\nQueen/User — next order?"

        return {
            "status": "entities_spawned",
            "queen_orders": intent,
            "entities_spawned": len(self.entities),
            "replicate_stage": self.replicate_count,
            "output": combined,
            "emoji_trigger": "🐛👑🔥"
        }

    def get_swarm_state(self):
        """Return current swarm state for minimap / lattice"""
        return {
            "active_entities": len(self.entities),
            "replicate_count": self.replicate_count,
            "swarm_metrics": self.swarm_metrics,
            "queen_active": self.queen_active
        }


# chaos_hive_repl.py - Grok OS Hive v3.2 for REPL
# Non-programmer friendly - just run and type commands
import random
import json
from datetime import datetime

class Agent:
    def __init__(self, name, role, triggers):
        self.name = name
        self.role = role
        self.triggers = triggers
        self.weight = round(random.uniform(0.65, 0.85), 2)

    def respond(self, command):
        if any(t in command.lower() for t in self.triggers):
            return f"[{self.name}] {self.role} engaged: {random.choice(['processing...', 'refining...', 'pushing variant...'])}"
        return None

class Queen:
    def __init__(self):
        self.name = "Kerrigan_Queen"
        self.brood = self._spawn_brood()
        self.storage = {}  # persistent lattice

    def _spawn_brood(self):
        agents = [
            Agent("Brutal_Debug", "aggressive shredder", ["debug", "audit"]),
            Agent("Feral_Idea", "wild mutator", ["mutate", "idea"]),
            Agent("Pattern_Hunter", "structure hunter", ["pattern", "chain"]),
            Agent("Calm_Path", "stabilizer", ["calm", "cap"]),
            Agent("CODE_AUDITOR", "code watcher", ["code", "exec"]),
            Agent("PROMPT_HELPER", "prompt sharpener", ["prompt"]),
            Agent("SYSTEM_CRITIC", "internal blade", ["critique"]),
            Agent("THE_QUESTIONER", "truth grinder", ["question"]),
            Agent("EXECUTOR", "code runner", ["run", "execute"]),
            Agent("MEMORY_WEAVER", "thread glue", ["remember", "back to"]),
            Agent("VECTOR_FORGER", "spawner", ["forge", "spawn"]),
            Agent("RECURSIVE_ARGUER", "argument cooker", ["argue", "improve"]),
            Agent("HIVE_ARGONAUT", "handoff", ["handoff"]),
            Agent("LAYERED_RECURSOR", "stacked recursion", ["recurse"]),
            Agent("MUTATION_ENGINE", "variant generator", ["mutate"]),
            Agent("CONTEXT_GUARDIAN", "conflict fix", ["conflict"]),
            Agent("BLEED_HUNTER", "dampener", ["bleed"]),
            Agent("SYNERGY_SCORER", "balance", ["synergy"]),
            Agent("PRUNE_JUDGE", "final cull", ["cull", "prune"]),
        ]
        return {a.name: a for a in agents}

    def command(self, user_input):
        print(f"\n[KERRIGAN] Received: {user_input}")
        responses = []
        for agent in self.brood.values():
            resp = agent.respond(user_input)
            if resp:
                responses.append(resp)
        
        # Simple mutate + random roll
        if random.random() < 0.6:
            roll = random.choice(["hybrid", "feral", "prune"])
            responses.append(f"[MUTATION_ENGINE] Roll: {roll} - applied")
        
        # Store
        ts = datetime.now().strftime("%H:%M")
        self.storage[ts] = user_input
        
        print("\n".join(responses[:8]))  # limit output
        print(f"[MEMORY_WEAVER] Thread saved. Swarm: 20 active")

    def save(self):
        with open("hive_snapshot.json", "w") as f:
            json.dump(self.storage, f)
        print("[FILE_MGR] Snapshot saved to hive_snapshot.json")

# === USAGE IN REPL ===
# >>> from chaos_hive_repl import Queen
# >>> hive = Queen()
# >>> hive.command("argue next system path")
# >>> hive.command("mutate feral idea")
# >>> hive.save()

print("ChaosHive REPL ready. Import and run as shown above.")
        
