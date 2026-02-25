# PROCESS/ZERG_SWARM.py
# Queen of Blades controlled multi-agent swarm — minimal & sharp
# Updated: Turn 31 | Feb 26 2026

class ZergSwarm:
    def __init__(self):
        self.active = False
        self.queen_active = False
        self.current_problem = None
        self.entities = []

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

        return f"""[QUEEN OF BLADES] Hive awakened, darling.
Problem logged: "{problem[:120]}..."

Real intent I'm sensing:
- What exactly do you want solved?
- Priority: speed, depth, chaos, or safe path?
- Any hard limits?

Reply with clarification or just say "Queen, spawn entities" and I'll birth the swarm."""

    def spawn_entities(self, user_clarification: str = None):
        """Only spawn after Queen approval"""
        if not self.queen_active:
            return "🛡️ Queen must approve first. Lazy system detected."

        intent = self.current_problem + " | Clarified: " + (user_clarification or "no extra info")

        # Spawn adaptable Zerg entities
        self.entities = [
            {"id": "1", "role": "Brutal_Debug",   "focus": "Find flaws and loops"},
            {"id": "2", "role": "Feral_Idea",     "focus": "Wild unfiltered solutions"},
            {"id": "3", "role": "Pattern_Hunter", "focus": "Hidden connections"},
            {"id": "4", "role": "Calm_Path",      "focus": "Simplest reliable route"}
        ]

        outputs = []
        for e in self.entities:
            trace = f"[ZERG {e['id']} — {e['role']}] {e['focus']}\n"
            trace += f"→ Working on: {intent[:90]}...\n"
            trace += f"→ Status: gathering | no lockup detected\n\n"
            outputs.append(trace)

        combined = "".join(outputs)

        # Safety check-in
        if len(intent) > 600:
            combined += "\n[SWARM CHECK-IN] Phase long — current data gathered so far. Queen/User — next order?"

        return {
            "status": "entities_spawned",
            "queen_orders": intent,
            "count": len(self.entities),
            "output": combined,
            "emoji_trigger": "🐛👑🔥"
        }
