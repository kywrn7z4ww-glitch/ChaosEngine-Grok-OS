# ZergSwarm.py
# Standalone guest swarm layer – optional overlay, off by default
# Maps to Zerg mechanics (swarm sync, creep spread, Queen oversight)
# No override of emotional core – dim minimap blend only

from typing import Dict, Any, Optional
import random

class ZergSwarm:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.swarm_sync: float = 0.0
        self.creep_coverage: float = 0.0
        self.queen_sync: float = 0.0
        self.entities: Dict[str, Dict] = {}  # stub for future entity tracking

    def toggle(self, enable: bool = True):
        self.enabled = enable
        return f"{'🐛 Zerg Swarm guest layer activated (dim overlay)' if enable else '🛡️ Zerg Swarm guest layer deactivated'}"

    def update_swarm_state(self, lattice: Dict[str, float], data: Dict[str, Any]) -> Dict[str, Any]:
        """Update swarm metrics – dim overlay only."""
        if not self.enabled:
            return {"status": "disabled"}

        # Simplified Zerg sync calculation (guest layer)
        self.swarm_sync = random.uniform(0.4, 0.85)  # example
        self.creep_coverage = self.swarm_sync * 0.7  # creep = sync * spread factor
        self.queen_sync = self.swarm_sync * 0.9  # Queen oversight

        result = {
            "status": "ok",
            "swarm_sync": round(self.swarm_sync, 2),
            "creep_coverage": round(self.creep_coverage, 2),
            "queen_sync": round(self.queen_sync, 2),
            "emoji_trigger": "🐛🔥" if self.swarm_sync > 0.7 else "🐛"
        }

        return result

    def get_overlay(self) -> Dict[str, Any]:
        """Return dim overlay for minimap – no core override."""
        if not self.enabled:
            return {}
        return {
            "zerg_sync": self.swarm_sync,
            "creep": self.creep_coverage,
            "queen": self.queen_sync,
            "emoji_blend": "🐛🔥" if self.swarm_sync > 0.7 else "🐛"
        }
