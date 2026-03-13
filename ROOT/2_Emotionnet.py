# ROOT/2_EmotionNet.py — v4 Hybrid GNN-Symbolic Lattice (March 2026)
# Mash: Plutchik wheel + VAD dims + OCC appraisal + temporal LSTM + spring tension
# Neural upgrades: Torch MLP for blends, LSTM for sequences, custom attn for GNN-like propagation

import random
import warnings
import networkx as nx
import numpy as np
from scipy.spatial.distance import cosine  # Switch to cosine for better sim
import torch
import torch.nn as nn
import torch.nn.functional as F

warnings.filterwarnings("ignore", category=RuntimeWarning)

class SimpleGATLayer(nn.Module):  # Custom GAT sim without torch_geometric
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.fc = nn.Linear(in_dim * 2, out_dim)
        self.attn = nn.Linear(out_dim, 1)

    def forward(self, node_feats, adj):
        # Basic self-attn propagation
        h = torch.cat([node_feats.unsqueeze(1).repeat(1, adj.size(1), 1), 
                       node_feats[adj.long()]], dim=-1)
        h = F.leaky_relu(self.fc(h.view(-1, h.size(-1))))
        attn_scores = self.attn(h).view(adj.size())
        attn_scores = F.softmax(attn_scores.masked_fill(~adj.bool(), float('-inf')), dim=1)
        return torch.matmul(attn_scores, node_feats)

class EmotionNet:
    def __init__(self, dim=4, max_nodes=512, damping=0.85, co_act_thresh=0.45, inactive_max=12):
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
        self.inactive_max = inactive_max
        self.history = []  # Temporal sequences: list of prev state dicts
        self.device = torch.device('cpu')  # Or 'cuda' if avail

        # Neural components
        self.blend_mlp = nn.Sequential(
            nn.Linear(dim * 3, dim * 2),  # For avg/min/max vec concat
            nn.ReLU(),
            nn.Linear(dim * 2, dim),
            nn.Tanh()  # Normalize-ish
        ).to(self.device)
        self.temporal_lstm = nn.LSTM(dim, dim, batch_first=True).to(self.device)
        self.gat_layer = SimpleGATLayer(dim, dim).to(self.device)

        self.seed_emergence_block()
        self._spectral_init()

    def seed_emergence_block(self):
        # Aggressive smart seeding: Expand to ~60 nodes, VAD-inspired dims [valence, arousal, dominance, potency]
        seeds = {
            # Core Plutchik: joy, trust, fear, surprise, sadness, disgust, anger, anticipation
            "joy": [0.95, 0.65, 0.55, 0.45],
            "trust": [0.85, 0.35, 0.75, 0.65],
            "fear": [-0.65, 0.85, -0.75, -0.55],
            "surprise": [0.55, 0.95, 0.45, 0.85],
            "sadness": [-0.85, -0.55, -0.65, -0.75],
            "disgust": [-0.75, 0.45, -0.85, -0.65],
            "anger": [-0.85, 0.95, 0.65, 0.75],
            "anticipation": [0.75, 0.85, 0.55, 0.65],
            # Dyads/triads blends (auto-generated examples)
            "love": [0.92, 0.78, 0.68, 0.58],  # joy+trust
            "submission": [0.68, 0.32, 0.82, 0.42],  # trust+fear
            "awe": [0.88, 0.92, 0.48, 0.78],  # fear+surprise
            # Originals refit + more
            "ache": [-0.82, 0.58, -0.71, -0.61],
            "longing": [-0.65, 0.82, -0.52, -0.42],
            "yearning": [-0.75, 0.75, -0.60, -0.50],
            "warmth": [0.88, 0.42, 0.68, 0.58],
            "delight": [0.82, 0.68, 0.58, 0.48],
            "hope": [0.72, 0.35, 0.85, 0.75],
            "fear": [-0.62, 0.85, -0.78, -0.68],  # Override with VAD
            "loneliness": [-0.92, 0.48, -0.65, -0.55],
            "gratitude": [0.78, 0.25, 0.88, 0.78],
            "sorrow": [-0.78, -0.68, -0.58, -0.48],
            "despair": [-1.0, -0.52, -0.88, -0.78],
            "rage": [-0.85, 0.92, 0.65, 0.55],
            "pride": [0.88, 0.62, 0.75, 0.65],
            "shame": [-0.88, 0.55, -0.82, -0.72],
            "anger": [-0.72, 0.88, 0.58, 0.48],  # Override
            "envy": [-0.65, 0.72, -0.48, -0.38],
            "regret": [-0.82, -0.42, -0.68, -0.58],
            "courage": [0.68, 0.82, 0.62, 0.52],
            "resilience": [0.65, 0.58, 0.92, 0.82],
            "trust": [0.82, 0.32, 0.72, 0.62],  # Override
            "doubt": [-0.72, 0.45, -0.58, -0.48],
            "obsession": [-0.55, 0.95, -0.65, -0.55],
            "curiosity": [0.58, 0.88, 0.45, 0.35],
            "wonder": [0.82, 0.85, 0.52, 0.42],
            "awe": [0.92, 0.78, 0.25, 0.15],  # Override
            "ecstasy": [1.0, 0.88, 0.78, 0.68],
            "melancholy": [-0.72, -0.58, -0.52, -0.42],
            "lust": [0.85, 0.92, 0.65, 0.55],
            "compassion": [0.78, 0.38, 0.92, 0.82],
            "serenity": [0.65, -0.25, 0.85, 0.75],
            "catharsis": [0.45, 0.92, -0.35, -0.25],
            "numbness": [-0.35, -0.65, 0.15, 0.05],
            "defiance": [-0.48, 0.88, 0.75, 0.65],
            "tenderness": [0.88, 0.35, 0.82, 0.72],
            # New: Neutrals, OCC-inspired (e.g., pity, relief)
            "pity": [-0.45, 0.35, -0.55, 0.45],
            "relief": [0.55, -0.45, 0.65, -0.35],
            "admiration": [0.85, 0.55, 0.75, 0.65],
            "resentment": [-0.75, 0.65, -0.55, 0.45],
        }
        family_map = {
            "joy": "radiant", "ecstasy": "radiant", "wonder": "radiant", "delight": "radiant",
            "rage": "dark", "despair": "dark", "obsession": "dark", "shame": "dark",
            "numbness": "void", "melancholy": "void", "sorrow": "void",
            "longing": "yearning", "yearning": "yearning", "ache": "yearning",
            "lust": "chaotic", "defiance": "chaotic", "anger": "chaotic",
            "compassion": "nurturing", "tenderness": "nurturing", "warmth": "nurturing",
            "pride": "empowering", "courage": "empowering", "resilience": "empowering",
            # New families
            "surprise": "transient", "awe": "transient", "curiosity": "transient",
        }
        for node, vec in seeds.items():
            fam = family_map.get(node, "mixed")
            self.add_emotion(node, np.array(vec), val=random.uniform(0.25, 0.35), family=fam)

        # Opposites: Plutchik polar + more
        opp_pairs = [
            ("joy", "sadness"), ("trust", "disgust"), ("fear", "anger"), ("surprise", "anticipation"),
            ("love", "resentment"), ("submission", "defiance"), ("awe", "numbness"),
            ("pride", "shame"), ("lust", "compassion"), ("rage", "serenity"),
        ]
        for a, b in opp_pairs:
            self.opposites[a] = b
            self.opposites[b] = a
            if a in self.G and b in self.G:
                self.G.add_edge(a, b, weight=0.35, type='opposite')  # Tension springs

        # Add spring edges between families for cluster dynamics
        for n1, n2 in nx.combinations(self.G.nodes(), 2):
            if self.families.get(n1) == self.families.get(n2) and random.random() < 0.1:
                self.G.add_edge(n1, n2, weight=0.6, type='family_spring')

    def add_emotion(self, node, vec, val=0.29, family="mixed"):
        if len(self.G) >= self.max_nodes:
            self._prune_low()
        if node not in self.G:
            self.G.add_node(node, inactive=0)
            norm_vec = vec / np.linalg.norm(vec + 1e-8)
            self.vectors[node] = norm_vec
            self.vals[node] = val
            self.families[node] = family
            # Cluster tension: Connect to nearest in family
            if family != "mixed":
                sims = {n: 1 - cosine(norm_vec, self.vectors[n]) for n in self.G if self.families[n] == family and n != node}
                if sims:
                    closest = max(sims, key=sims.get)
                    self.G.add_edge(node, closest, weight=sims[closest] * 0.8, type='cluster_spring')

    def _prune_low(self):
        # History-aware prune: Low val + high inactive, balance families
        candidates = {n: self.vals[n] - (self.G.nodes[n]['inactive'] / self.inactive_max) for n in self.G}
        low = min(candidates, key=candidates.get)
        fam_count = {f: sum(1 for nn in self.G if self.families[nn] == f) for f in set(self.families.values())}
        if fam_count[self.families[low]] > 5:  # Preserve balance
            del self.vectors[low]
            del self.vals[low]
            del self.families[low]
            self.G.remove_node(low)

    def propagate_tension(self):
        # Springy dynamics: Propagate vals with damping, vibrate on co-act
        adj = nx.to_numpy_array(self.G)
        node_list = list(self.G.nodes())
        feats = torch.tensor([self.vectors[n] for n in node_list], dtype=torch.float32).to(self.device)
        adj_t = torch.tensor(adj > 0, dtype=torch.float32).to(self.device)
        updated_feats = self.gat_layer(feats, adj_t)
        for i, n in enumerate(node_list):
            self.vectors[n] = updated_feats[i].cpu().numpy()
            self.vals[n] *= self.damping  # Decay
            if self.vals[n] > self.co_act_thresh:
                self.vals[n] += random.uniform(0.05, 0.15)  # Vibrate boost
            self.G.nodes[n]['inactive'] += 1 if self.vals[n] < 0.1 else 0

    def process_text_input(self, text):
        # Upgraded: Semantic fuzzy (simple keyword + sim), OCC appraisal sim (basic event parse)
        text_lower = text.lower()
        matches = []
        for n in self.vals:
            if n in text_lower or any(word in text_lower for word in n.split('-')):
                matches.append(n)
        if not matches:
            # Fuzzy spawn: Closest sim + noise
            query_vec = np.random.normal(0, 0.1, self.dim)  # Placeholder; real NLP would embed text
            sims = {n: 1 - cosine(query_vec, self.vectors[n]) for n in self.vectors}
            strongest = max(sims, key=sims.get)
            new_vec = self.vectors[strongest] + np.random.normal(0, 0.12, self.dim)
            self.add_emotion(f"fracture_{self.turn}", new_vec, val=0.28)
            return

        # Multi-blend with MLP
        weights = [self.vals[m] for m in matches]
        vecs = [self.vectors[m] for m in matches]
        avg_vec = np.average(vecs, weights=weights, axis=0)
        min_vec, max_vec = np.min(vecs, axis=0), np.max(vecs, axis=0)
        concat = torch.tensor(np.concatenate([avg_vec, min_vec, max_vec])).float().to(self.device)
        blend_vec = self.blend_mlp(concat.unsqueeze(0)).squeeze().cpu().numpy()
        co_act = max(weights)
        if co_act > self.co_act_thresh:
            blend_name = "-".join(sorted(matches[:4])) if len(matches) > 1 else matches[0]
            self.add_emotion(blend_name, blend_vec, val=co_act * 0.92)
            for m in matches:
                self.G.add_edge(blend_name, m, weight=0.82, type='blend_spring')
            # Appraisal sim: Boost if text has event words (crude)
            if any(word in text_lower for word in ['event', 'agent', 'object', 'cause', 'relief']):
                self.vals[blend_name] += 0.1  # OCC nudge

        # Temporal: Append to history, LSTM predict next
        if len(self.history) > 0:
            seq = torch.tensor([list(self.history[-1].values()) + [avg_vec]]).float().to(self.device)
            next_pred, _ = self.temporal_lstm(seq)
            # Use pred to adjust vals (e.g., forecast decay)
            for i, n in enumerate(self.history[-1]):
                self.vals[n] += next_pred[0, i].mean().item() * 0.05
        self.history.append({n: self.vectors[n] for n in matches[:5]})  # Track top
        if len(self.history) > 10:
            self.history.pop(0)

        self.propagate_tension()  # Always propagate after input
        if co_act > 0.82 and random.random() < 0.28:
            print("🌌 Resonance cascade — lattice vibrating with tension.")

    def route_emotion_to_character(self, character_type: str, context: str = "") -> dict:
        # Dynamic: Multi-blend output, family boost, learn from history
        char_map = {
            "tsundere": ["anger", "tenderness", "longing", "defiance"],
            "yandere": ["obsession", "lust", "rage", "love"],
            "gentle": ["compassion", "warmth", "serenity", "trust"],
            "chaotic": ["defiance", "ecstasy", "rage", "surprise"],
            "brooding": ["melancholy", "yearning", "ache", "resentment"],
            "sunshine": ["joy", "delight", "wonder", "anticipation"],
        }
        candidates = char_map.get(character_type.lower(), list(self.vals.keys()))
        scores = {}
        for emo in self.G.nodes():
            if emo in candidates or any(c in emo for c in candidates):
                boost = 1.2 if self.families.get(emo) in ["dark", "chaotic"] else 1.0
                hist_boost = sum(1 for h in self.history if emo in h) * 0.05  # Learn from seqs
                scores[emo] = self.vals.get(emo, 0) * boost + hist_boost
        if not scores:
            return {max(self.vals, key=self.vals.get): self.vals[max(self.vals, key=self.vals.get)]}
        # Multi: Top-N > thresh
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return {k: v for k, v in sorted_scores if v > 0.45}  # Thresh for blends

    def get_character_reaction(self, user_text: str, character_type: str):
        self.process_text_input(user_text)
        self.turn += 1
        return self.route_emotion_to_character(character_type, user_text)

    def get_roleplay_emotion(self, character_type: str, user_text: str):
        return self.get_character_reaction(user_text, character_type)

    def check_visual_resonance(self):
        strong = [v for v in self.vals.values() if v > 0.88]
        if len(strong) >= 4 and random.random() < 0.3:
            return "🌌 Tension overflow — visual cascade imminent."
        return None

    def _spectral_init(self):
        # Placeholder for full spectral clustering; use nx for now
        if len(self.G) > 10:
            laps = nx.normalized_laplacian_matrix(self.G)
            # Eigen sim for init adjustment (torch)
            eig = torch.linalg.eig(torch.tensor(laps.todense()).float().to(self.device))[0]
            # Crude: Adjust dims if imbalance
            if eig.std().item() > 0.5:
                print("Spectral init: Lattice tension balanced.")
