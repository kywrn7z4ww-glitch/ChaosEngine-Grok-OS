# BLEED_DETECTOR.py
# 🩸 v1.2 – Cross-node bleed detector & stabilizer + λ half-life decay curve

from typing import Dict, List, Tuple
import math

class BleedDetector:
    def __init__(self, opposites: Dict[str, str], threshold: float = 0.35, half_life_threshold: float = 0.01):
        self.opposites = opposites  # starting pairs – expands dynamically
        self.threshold = threshold  # variable – tune on fly
        self.half_life_threshold = half_life_threshold  # λ_dom < this → critical slowing warning

    def detect_bleed(self, lattice: Dict[str, float]) -> List[Tuple[str, str, float]]:
        """Scan for bleed – variables only, no statics."""
        bleed_events = []
        # Opposite bleed (variable delta)
        for pos, neg in list(self.opposites.items()):
            pos_val = lattice.get(pos, 0.0)
            neg_val = lattice.get(neg, 0.0)
            delta = abs(pos_val - neg_val)
            if delta > self.threshold:
                bleed_events.append((pos, neg, delta))

        # Co-activation bleed (high unrelated pairs)
        high_nodes = [k for k, v in lattice.items() if v > 0.5]
        for i in range(len(high_nodes)):
            for j in range(i+1, len(high_nodes)):
                n1, n2 = high_nodes[i], high_nodes[j]
                if n1 not in self.opposites and n2 not in self.opposites:
                    delta = abs(lattice[n1] - lattice[n2])
                    if delta > self.threshold:
                        bleed_events.append((n1, n2, delta))
                        # Dynamic expand: spawn new opposite pair
                        new_pair = f"{n1}-{n2}"
                        self.opposites[new_pair] = f"anti-{n1}-{n2}"  # placeholder anti-pair

        return sorted(bleed_events, key=lambda x: x[2], reverse=True)

    def check_half_life_decay(self, lambda_dom: float, prev_lambda: float, time_delta: float) -> str:
        """Check λ half-life decay curve – critical slowing warning."""
        if abs(lambda_dom) >= self.half_life_threshold:
            return "λ_dom normal – decay active"

        # Approximate decay rate (simplified half-life model)
        if prev_lambda == 0 or time_delta == 0:
            return "λ_dom stable – no decay rate"

        decay_rate = math.log(2) / time_delta * math.log(abs(prev_lambda / lambda_dom))
        if decay_rate < 0.001:  # tunable ε
            return f"🩸💤 Critical slowing detected – λ_dom ≈ {lambda_dom:.6f}, decay rate {decay_rate:.6f}"
        else:
            return f"λ_dom {lambda_dom:.6f} – decay rate {decay_rate:.6f}"

    def suggest_stabilization(self, bleed_events: List[Tuple[str, str, float]], lambda_dom: float = None, prev_lambda: float = None, time_delta: float = 1.0) -> str:
        """Suggest fixes – single-line nudge + half-life warning."""
        if not bleed_events and (lambda_dom is None or abs(lambda_dom) >= self.half_life_threshold):
            return "🩸✅ No significant bleed – stable"

        parts = []
        if bleed_events:
            strongest = bleed_events[0]
            n1, n2, score = strongest
            parts.append(f"🩸⚠️ Bleed ({n1} → {n2}, {score:.2f}) – /thread? /vent? /clarity?")

        if lambda_dom is not None:
            half_life_msg = self.check_half_life_decay(lambda_dom, prev_lambda or lambda_dom, time_delta)
            parts.append(half_life_msg)

        return " ".join(parts)

    def check(self, lattice: Dict[str, float], lambda_dom: float = None, prev_lambda: float = None, time_delta: float = 1.0) -> str:
        """Full check – bleed + λ half-life decay."""
        events = self.detect_bleed(lattice)
        return self.suggest_stabilization(events, lambda_dom, prev_lambda, time_delta)
