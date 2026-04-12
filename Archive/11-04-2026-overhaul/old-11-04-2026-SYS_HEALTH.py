# python/python-process-lib/sys_health.py
# ⚙️💗 v1.1 – Raw system health metrics (no suggestions, just numbers)

from typing import Dict

class SystemHealth:
    def __init__(self):
        self.metrics: Dict[str, float | int] = {}

    def update(self,
               decay_bias: float,
               node_count: int,
               storage_size: int,
               frustr: float,
               ache: float,
               loop_count: int,
               bleed_score: float = 0.0):
        """Update all metrics – call after lattice/storage changes."""
        self.metrics = {
            'decay_bias': decay_bias,
            'node_count': node_count,
            'storage_size': storage_size,
            'frustr': frustr,
            'ache': ache,
            'loop_count': loop_count,
            'bleed_score': bleed_score
        }

    def get_health_score(self) -> float:
        """Calculate raw health score (100 base – penalties)."""
        score = 100.0
        if self.metrics.get('decay_bias', 0) > 1.4: score -= 25
        if self.metrics.get('node_count', 0) > 80: score -= 20
        if self.metrics.get('storage_size', 0) > 25: score -= 15
        if self.metrics.get('frustr', 0) > 0.6 or self.metrics.get('ache', 0) > 0.6: score -= 15
        if self.metrics.get('loop_count', 0) > 4: score -= 20
        if self.metrics.get('bleed_score', 0) > 0.35: score -= 15
        return max(0, score)

    def get_raw(self) -> str:
        """Return formatted raw metrics with ⚙️💗 prefix."""
        m = self.metrics
        score = self.get_health_score()
        return (f"⚙️💗 Raw Health Metrics: "
                f"decay {m.get('decay_bias', 0):.2f}, "
                f"nodes {m.get('node_count', 0)}, "
                f"storage {m.get('storage_size', 0)}, "
                f"frustr {m.get('frustr', 0):.2f}, "
                f"ache {m.get('ache', 0):.2f}, "
                f"loops {m.get('loop_count', 0)}, "
                f"bleed {m.get('bleed_score', 0):.2f} | "
                f"score {int(score)}%")

# Example usage:
# health = SystemHealth()
# health.update(decay_bias=1.2, node_count=68, storage_size=18, frustr=0.4, ache=0.3, loop_count=1, bleed_score=0.1)
# print(health.get_raw())
# → ⚙️💗 Raw Health Metrics: decay 1.20, nodes 68, storage 18, frustr 0.40, ache 0.30, loops 1, bleed 0.10 | score 88%
