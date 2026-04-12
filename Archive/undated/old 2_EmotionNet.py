# ROOT/2_EmotionNet.py — v3 Aggressive Character-Routing Lattice (March 2026)
# Heavy seeding + emotional families + direct character routing for roleplay

import random
import warnings

import networkx as nx
import numpy as np
from scipy.spatial.distance import euclidean

warnings.filterwarnings("ignore", category=RuntimeWarning)


class EmotionNet:
    def __init__(self, dim=3, max_nodes=320, damping=0.87, co_act_thresh=0.32):
        self.G = nx.Graph()
        self.vectors = {}
        self.vals = {}
        self.opposites = {}
        self.families = {}
        self.turn = 0
        self.dim = dim
        self.max_nodes = max_nodes
        self.damping = damping
        self.co_act_thresh = co_act_thresh
        self.inactive_max = 8

        self.seed_emergence_block()
        self._spectral_init()

    def seed_emergence_block(self):
        seeds = {
            "ache": [-0.82, 0.58, -0.71],
            "longing": [-0.65, 0.82, -0.52],
            "yearning": [-0.75, 0.75, -0.60],
            "warmth": [0.88, 0.42, 0.68],
            "delight": [0.82, 0.68, 0.58],
            "hope": [0.72, 0.35, 0.85],
            "joy": [1.0, 0.55, 0.48],
            "fear": [-0.62, 0.85, -0.78],
            "loneliness": [-0.92, 0.48, -0.65],
            "gratitude": [0.78, 0.25, 0.88],
            "sorrow": [-0.78, -0.68, -0.58],
            "despair": [-1.0, -0.52, -0.88],
            "rage": [-0.85, 0.92, 0.65],
            "pride": [0.88, 0.62, 0.75],
            "shame": [-0.88, 0.55, -0.82],
            "anger": [-0.72, 0.88, 0.58],
            "envy": [-0.65, 0.72, -0.48],
            "regret": [-0.82, -0.42, -0.68],
            "courage": [0.68, 0.82, 0.62],
            "resilience": [0.65, 0.58, 0.92],
            "trust": [0.82, 0.32, 0.72],
            "doubt": [-0.72, 0.45, -0.58],
            "obsession": [-0.55, 0.95, -0.65],
            "curiosity": [0.58, 0.88, 0.45],
            "wonder": [0.82, 0.85, 0.52],
            "awe": [0.92, 0.78, 0.25],
            "ecstasy": [1.0, 0.88, 0.78],
            "melancholy": [-0.72, -0.58, -0.52],
            "lust": [0.85, 0.92, 0.65],
            "compassion": [0.78, 0.38, 0.92],
            "serenity": [0.65, -0.25, 0.85],
            "catharsis": [0.45, 0.92, -0.35],
            "numbness": [-0.35, -0.65, 0.15],
            "defiance": [-0.48, 0.88, 0.75],
            "tenderness": [0.88, 0.35, 0.82],
        }
        family_map = {
            "rage": "dark",
            "despair": "dark",
            "obsession": "dark",
            "numbness": "void",
            "joy": "radiant",
            "ecstasy": "radiant",
            "wonder": "radiant",
            "longing": "yearning",
            "yearning": "yearning",
            "ache": "yearning",
            "lust": "chaotic",
            "defiance": "chaotic",
            "rage": "chaotic",
            "compassion": "nurturing",
            "tenderness": "nurturing",
            "warmth": "nurturing",
        }
        for node, vec in seeds.items():
            fam = family_map.get(node, "mixed")
            self.add_emotion(node, np.array(vec), val=0.29, family=fam)

        opp_pairs = [
            ("joy", "sorrow"),
            ("trust", "doubt"),
            ("fear", "courage"),
            ("pride", "shame"),
            ("lust", "compassion"),
            ("rage", "serenity"),
        ]
        for a, b in opp_pairs:
            self.opposites[a] = b
            self.opposites[b] = a
            if a in self.G and b in self.G:
                self.G.add_edge(a, b, weight=0.38)

    def add_emotion(self, node, vec, val=0.29, family="mixed"):
        if len(self.G) >= self.max_nodes:
            self._prune_low()
        if node not in self.G:
            self.G.add_node(node, inactive=0)
            self.vectors[node] = vec[: self.dim] / np.linalg.norm(
                vec[: self.dim] + 1e-8
            )
            self.vals[node] = val
            self.families[node] = family

    def route_emotion_to_character(
        self, character_type: str, context: str = ""
    ) -> dict:
        char_map = {
            "tsundere": ["rage", "tenderness", "longing"],
            "yandere": ["obsession", "lust", "rage"],
            "gentle": ["compassion", "warmth", "serenity"],
            "chaotic": ["defiance", "ecstasy", "rage"],
            "brooding": ["melancholy", "yearning", "ache"],
            "sunshine": ["joy", "delight", "wonder"],
        }
        candidates = char_map.get(character_type.lower(), list(self.vals.keys()))
        scores = {}
        for emo in candidates:
            if emo in self.vals:
                scores[emo] = self.vals[emo] * (
                    1.15 if self.families.get(emo) == "dark" else 1.0
                )
        if not scores:
            strongest = max(self.vals, key=self.vals.get)
            return {strongest: self.vals[strongest]}
        best = max(scores, key=scores.get)
        return {best: self.vals[best]}

    def get_character_reaction(self, user_text: str, character_type: str):
        self.process_text_input(user_text)
        return self.route_emotion_to_character(character_type, user_text)

    def get_roleplay_emotion(self, character_type: str, user_text: str):
        """One-line helper for Luna/ChaosEngine during roleplay"""
        self.process_text_input(user_text)
        return self.route_emotion_to_character(character_type, user_text)

    def process_text_input(self, text):
        text_lower = text.lower()
        matches = [n for n in self.vals if n in text_lower]
        if matches:
            weights = [self.vals[m] for m in matches]
            avg_vec = np.average(
                [self.vectors[m] for m in matches], weights=weights, axis=0
            )
            co_act = max(weights)
            if co_act > self.co_act_thresh:
                blend_name = (
                    "-".join(sorted(matches[:3])) if len(matches) >= 2 else matches[0]
                )
                self.add_emotion(
                    blend_name,
                    avg_vec + np.random.normal(0, 0.085, self.dim),
                    val=co_act * 0.88,
                )
                for m in matches[:3]:
                    self.G.add_edge(blend_name, m, weight=0.78)
            if co_act > 0.80 and random.random() < 0.24:
                print("🌌 Visual resonance triggered — lattice is singing.")
        else:
            strongest = max(self.vals, key=self.vals.get)
            new_vec = self.vectors[strongest] + np.random.normal(0, 0.135, self.dim)
            self.add_emotion(f"fracture_{self.turn}", new_vec, val=0.28)

    def check_visual_resonance(self):
        strong = [v for v in self.vals.values() if v > 0.86]
        if len(strong) >= 3 and random.random() < 0.25:
            return "🌌 Lattice overflowing — strong image generation signal."
        return None

    # force_update, gnn_pass, top_nodes, _prune_low, _spectral_init kept as original weird magic
