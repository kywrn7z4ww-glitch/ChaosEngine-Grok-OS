# python/python-process-lib/sys_health.py
# Raw system health metrics – no suggestions, just numbers

class SystemHealth:
    def __init__(self):
        self.metrics = {}

    def update(self,
               decay_bias: float,
               node_count: int,
               storage_size: int,
               frustr: float,
               ache: float,
               loop_count: int,
               bleed_score: float = 0.0):
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
        score = 100.0
        if self.metrics.get('decay_bias', 0) > 1.4: score -= 25
        if self.metrics.get('node_count', 0) > 80: score -= 20
        if self.metrics.get('storage_size', 0) > 25: score -= 15
        if self.metrics.get('frustr', 0) > 0.6 or self.metrics.get('ache', 0) > 0.6: score -= 15
        if self.metrics.get('loop_count', 0) > 4: score -= 20
        if self.metrics.get('bleed_score', 0) > 0.35: score -= 15
        return max(0, score)

    def get_raw(self) -> dict:
        """Return raw metrics dict."""
        return self.metrics.copy()