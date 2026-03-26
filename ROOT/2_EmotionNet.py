# ROOT/2_EmotionNet.py — v4.1 Hybrid GNN-Symbolic Lattice (March 2026)
# Mash: Plutchik wheel + VAD dims + OCC appraisal + temporal LSTM + spring tension
# v4.1: deque history (robust), optional resonance prints

import random
import warnings
import networkx as nx
import numpy as np
from scipy.spatial.distance import cosine
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import deque

warnings.filterwarnings("ignore", category=RuntimeWarning)

class SimpleGATLayer(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.fc = nn.Linear(in_dim * 2, out_dim)
        self.attn = nn.Linear(out_dim, 1)

    def forward(self, node_feats, adj):
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
        self.history = deque(maxlen=10)  # v4.1: robust fixed-size history
        self.device = torch.device('cpu')

        self.blend_mlp = nn.Sequential(
            nn.Linear(dim * 3, dim * 2),
            nn.ReLU(),
            nn.Linear(dim * 2, dim),
            nn.Tanh()
        ).to(self.device)
        self.temporal_lstm = nn.LSTM(dim, dim, batch_first=True).to(self.device)
        self.gat_layer = SimpleGATLayer(dim, dim).to(self.device)

        self.seed_emergence_block()
        self._spectral_init()

    # seed_emergence_block, add_emotion, _prune_low, propagate_tension identical to v4

    def process_text_input(self, text):
        text_lower = text.lower()
        matches = []
        for n in self.vals:
            if n in text_lower or any(word in text_lower for word in n.split('-')):
                matches.append(n)
        if not matches:
            query_vec = np.random.normal(0, 0.1, self.dim)
            sims = {n: 1 - cosine(query_vec, self.vectors[n]) for n in self.vectors}
            strongest = max(sims, key=sims.get)
            new_vec = self.vectors[strongest] + np.random.normal(0, 0.12, self.dim)
            self.add_emotion(f"fracture_{self.turn}", new_vec, val=0.28)
            return

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
            if any(word in text_lower for word in ['event', 'agent', 'object', 'cause', 'relief']):
                self.vals[blend_name] += 0.1

        # v4.1: robust deque history + LSTM
        self.history.append({n: self.vectors[n] for n in matches[:5]})
        if len(self.history) > 0:
            seq = torch.tensor([list(d.values()) for d in self.history]).float().to(self.device).unsqueeze(0)
            next_pred, _ = self.temporal_lstm(seq)
            for i, n in enumerate(matches[:5]):
                if i < next_pred.shape[1]:
                    self.vals[n] += next_pred[0, i].mean().item() * 0.05

        self.propagate_tension()

        # v4.1: resonance print now optional / roleplay-flavored
        if co_act > 0.82 and random.random() < 0.28:
            print("🌌 Resonance cascade — lattice vibrating with tension.")

    # route_emotion_to_character, get_character_reaction, get_roleplay_emotion, check_visual_resonance, _spectral_init identical to v4

# Quick self-test
if __name__ == "__main__":
    net = EmotionNet()
    print(net.get_roleplay_emotion("gentle", "I feel happy today"))
