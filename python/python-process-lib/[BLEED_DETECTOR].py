# python/python-process-lib/bleed_detector.py
# 🔄 v1.1 – Cross-node bleed detector & stabilizer (variables, dynamic growth)

from typing import Dict, List, Tuple

class BleedDetector:
    def __init__(self, opposites: Dict[str, str], threshold: float = 0.35):
        self.opposites = opposites  # starting pairs – expands dynamically
        self.threshold = threshold  # variable – tune on fly

    def detect_bleed(self, lattice: Dict[str, float]) -> List[Tuple[str, str, float]]:
        """Scan for bleed – variables only, no statics."""
        bleed_events = []

        # Opposite bleed (variable delta)
        for pos, neg in list(self.opposites.items()):  # list to allow dynamic modify
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

    def suggest_stabilization(self, bleed_events: List[Tuple[str, str, float]]) -> str:
        """Suggest fixes – single-line nudge."""
        if not bleed_events:
            return "🔄 No significant bleed – stable"

        strongest = bleed_events[0]
        n1, n2, score = strongest
        return f"🔄 Bleed detected ({n1} → {n2}, {score:.2f}) – /thread split? /vent? /clarity?"

    def check(self, lattice: Dict[str, float]) -> str:
        """Full check – call on demand or auto-nudge."""
        events = self.detect_bleed(lattice)
        return self.suggest_stabilization(events)

# Example usage:  
# opposites = {'ache': 'relief', 'frustr': 'satisf'}
# detector = BleedDetector(opposites, threshold=0.4)
# lattice = {'ache': 0.7, 'relief': 0.2, 'frustr': 0.3, 'project': 0.6}
# print(detector.check(lattice))
