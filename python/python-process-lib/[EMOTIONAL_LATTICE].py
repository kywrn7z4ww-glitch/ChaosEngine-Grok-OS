# python/python-process-lib/lattice.py
# 🔄 v1 – Dynamic emotional/cognitive lattice (growth, bleed, flex, no statics)

import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional

class Lattice:
    def __init__(self, max_nodes_sim: int = 100, max_nodes_full: int = 500):
        # Core state – all dynamic
        self.nodes: Dict[str, Dict] = {}  # node_name: {'value': float, 'dc': int, 'edges': {target: bleed_rate}}
        self.opposites: Dict[str, str] = {}  # pos → neg (expands on blends)
        self.max_nodes = max_nodes_sim  # toggle for full mode
        self.is_full_mode = False
        self.decay_bias = 1.0  # global accel on negative bleed
        self.tidal_counter = 0

        # Seed cognitive/text-based opposites (no bodily, from appraisal/awareness theories)
        self._seed_opposites()

    def _seed_opposites(self):
        """Load initial cognitive/text opposites – expandable."""
        seeds = {
            'joy': 'sadness',
            'trust': 'disgust',
            'fear': 'anger',
            'surprise': 'anticipation',
            'calm': 'frustr',
            'relief': 'ache',
            'spark': 'despair',
            'meaning': 'void',
            'courage': 'fear',  # fear already there, reinforce
            'hope': 'dread',
            'pride': 'shame',
            'excitement': 'boredom',
            'satisfaction': 'frustration',
            'acceptance': 'rejection',
            'interest': 'apathy'
        }
        for pos, neg in seeds.items():
            self.add_node(pos, 0.0)
            self.add_node(neg, 0.0)
            self.opposites[pos] = neg
            self.opposites[neg] = pos  # bidirectional

    def toggle_full_mode(self, enable: bool):
        """Switch to uncapped calibration mode."""
        self.is_full_mode = enable
        self.max_nodes = 500 if enable else 100
        if enable:
            print("🔄 Full lattice mode – uncapped growth, max flex, no prune")

    def add_node(self, name: str, initial_value: float = 0.0):
        """Add node if not exists – dynamic growth."""
        if name not in self.nodes:
            if len(self.nodes) >= self.max_nodes and not self.is_full_mode:
                return  # sim cap – skip in compressed mode
            self.nodes[name] = {
                'value': max(0.0, min(1.0, initial_value)),
                'dc': 0,  # decay counter
                'edges': {}  # target: bleed_rate (0.0–1.0)
            }

    def update_node(self, name: str, delta: float):
        """Update value – clamp 0–1, reset dc on change."""
        if name not in self.nodes:
            self.add_node(name, 0.0)
        self.nodes[name]['value'] = max(0.0, min(1.0, self.nodes[name]['value'] + delta))
        if abs(delta) > 0.05:  # meaningful change
            self.nodes[name]['dc'] = 0

    def add_bleed_edge(self, from_node: str, to_node: str, rate: float = 0.1):
        """Add directed bleed edge – dynamic link."""
        if from_node in self.nodes and to_node in self.nodes:
            self.nodes[from_node]['edges'][to_node] = rate

    def propagate_bleed(self):
        """Apply bleed – leak value across edges."""
        updates = {}
        for node, data in self.nodes.items():
            for target, rate in data['edges'].items():
                leak = data['value'] * rate
                updates[target] = updates.get(target, 0.0) + leak
        for target, amount in updates.items():
            self.update_node(target, amount)

    def process_input(self, text: str):
        """Fuzzy/regex/lev match input → boost existing or spawn new."""
        words = set(re.findall(r'\w+', text.lower()))
        boosted = set()

        # Regex + fuzzy match to existing nodes
        for node in list(self.nodes.keys()):
            if re.search(rf'\b{re.escape(node)}\b', text, re.I) or any(w in node.lower() for w in words):
                self.update_node(node, 0.2)
                boosted.add(node)

        # Lev/fuzzy for new terms
        for word in words:
            best_match = None
            best_ratio = 0.0
            for node in self.nodes:
                ratio = SequenceMatcher(None, word, node).ratio()
                if ratio > best_ratio and ratio > 0.7:
                    best_ratio = ratio
                    best_match = node
            if best_match:
                self.update_node(best_match, 0.15)  # boost existing
                boosted.add(best_match)
            else:
                # Spawn new node
                self.add_node(word, 0.3)
                boosted.add(word)

        # Co-activation blends
        high_nodes = [n for n in boosted if self.nodes[n]['value'] > 0.5]
        for i in range(len(high_nodes)):
            for j in range(i+1, len(high_nodes)):
                n1, n2 = high_nodes[i], high_nodes[j]
                if n1 != n2:
                    blend_val = (self.nodes[n1]['value'] + self.nodes[n2]['value']) * 0.6
                    blend_name = f"{n1}-{n2}"
                    self.add_node(blend_name, blend_val)
                    self.add_bleed_edge(n1, blend_name, 0.1)
                    self.add_bleed_edge(n2, blend_name, 0.1)

    def tidal_cycle(self):
        """Every 3 turns – halve low, opposites nudge."""
        self.tidal_counter += 1
        if self.tidal_counter % 3 != 0:
            return

        for node, data in list(self.nodes.items()):
            val = data['value']
            if val < 0.15:
                data['value'] /= 2.2
                data['dc'] += 1
            else:
                data['dc'] = 0

            # Opposites nudge
            if node in self.opposites:
                opp = self.opposites[node]
                if opp in self.nodes:
                    self.nodes[opp]['value'] += 0.09 * (1 - val)  # stronger opposite when low

            # Prune dead nodes
            if data['dc'] > 6 and not self.is_full_mode:
                del self.nodes[node]

    def get_bleed_score(self) -> float:
        """Max bleed delta across opposites/co-activated."""
        max_delta = 0.0
        for pos, neg in self.opposites.items():
            if pos in self.nodes and neg in self.nodes:
                delta = abs(self.nodes[pos]['value'] - self.nodes[neg]['value'])
                max_delta = max(max_delta, delta)
        return max_delta

    def summary(self) -> str:
        """Quick status."""
        active = len([n for n, d in self.nodes.items() if d['value'] > 0.1])
        return f"🔄 Lattice: {len(self.nodes)} nodes ({active} active), bleed {self.get_bleed_score():.2f}, decay {self.decay_bias:.2f}"
