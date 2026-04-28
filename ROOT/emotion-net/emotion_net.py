#!/usr/bin/env python3
"""
emotion-net.py — EmotionNet v3.0 (Lean Core)
Real-time emotional state engine for Grok OS.

Preserves the original aggressive seeding and unique multi-model mashup:
Plutchik + VAD + OCC + Temporal LSTM + GAT + Spring Tension + Resonance

This is the lean, working version. All heavy future logic will move to emotion_lib/ later.
"""

import random
import warnings
from collections import deque

import networkx as nx
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy.spatial.distance import cosine

warnings.filterwarnings("ignore", category=RuntimeWarning)


class SimpleGATLayer(nn.Module):
    """Simple Graph Attention Layer for emotion tension propagation"""

    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.fc = nn.Linear(in_dim * 2, out_dim)
        self.attn = nn.Linear(out_dim, 1)

    def forward(self, node_feats, adj):
        h = torch.cat(
            [node_feats.unsqueeze(1).repeat(1, adj.size(1), 1), node_feats[adj.long()]],
            dim=-1,
        )
        h = F.leaky_relu(self.fc(h.view(-1, h.size(-1))))
        attn_scores = self.attn(h).view(adj.size())
        attn_scores = F.softmax(
            attn_scores.masked_fill(~adj.bool(), float("-inf")), dim=1
        )
        return torch.matmul(attn_scores, node_feats)


class EmotionNet:
    """
    Core emotional state engine.
    Tracks, blends, and propagates emotions in real time.
    """

    def __init__(
        self, dim=4, max_nodes=512, damping=0.85, co_act_thresh=0.45, inactive_max=12
    ):
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
        self.history = deque(maxlen=10)
        self.device = torch.device("cpu")

        # Neural components
        self.blend_mlp = nn.Sequential(
            nn.Linear(dim * 3, dim * 2), nn.ReLU(), nn.Linear(dim * 2, dim), nn.Tanh()
        ).to(self.device)

        self.temporal_lstm = nn.LSTM(dim, dim, batch_first=True).to(self.device)
        self.gat_layer = SimpleGATLayer(dim, dim).to(self.device)

        # Initialize
        self.seed_emergence_block()
        self._spectral_init()

    def seed_emergence_block(self):
        """Seed the initial emotion graph (aggressive seeding preserved)"""
        base_emotions = {
            "joy": [0.9, 0.7, 0.6, 0.8],
            "sadness": [-0.8, 0.4, 0.3, 0.2],
            "anger": [-0.6, 0.9, 0.7, 0.5],
            "fear": [-0.7, 0.8, 0.4, 0.3],
            "disgust": [-0.5, 0.6, 0.5, 0.4],
            "surprise": [0.4, 0.9, 0.6, 0.7],
            "trust": [0.7, 0.3, 0.8, 0.6],
            "anticipation": [0.5, 0.6, 0.7, 0.8],
        }

        for name, vec in base_emotions.items():
            self.add_emotion(name, np.array(vec), val=0.9)

        # Add opposites
        self.opposites = {
            "joy": "sadness",
            "sadness": "joy",
            "anger": "fear",
            "fear": "anger",
            "trust": "disgust",
            "disgust": "trust",
            "anticipation": "surprise",
            "surprise": "anticipation",
        }

    def add_emotion(self, name, vector, val=0.5):
        """Add a new emotion to the graph"""
        if len(self.vectors) >= self.max_nodes:
            self._prune_low()
        self.vectors[name] = vector
        self.vals[name] = val
        self.G.add_node(name)

    def _prune_low(self):
        """Remove low-value emotions"""
        to_remove = [n for n in self.vals if self.vals[n] < 0.1]
        for n in to_remove:
            if n in self.vectors:
                del self.vectors[n]
            if n in self.vals:
                del self.vals[n]
            if self.G.has_node(n):
                self.G.remove_node(n)

    def propagate_tension(self):
        """Propagate emotional tension through the graph"""
        for edge in list(self.G.edges()):
            n1, n2 = edge
            if n1 in self.vals and n2 in self.vals:
                tension = abs(self.vals[n1] - self.vals[n2]) * self.damping
                self.vals[n1] = max(0.0, min(1.0, self.vals[n1] + tension * 0.05))
                self.vals[n2] = max(0.0, min(1.0, self.vals[n2] - tension * 0.05))

    def process_text_input(self, text):
        """Main entry point — process user text and update emotional state"""
        text_lower = text.lower()
        matches = []

        for n in self.vals:
            if n in text_lower or any(word in text_lower for word in n.split("-")):
                matches.append(n)

        if not matches:
            # Create a new "fracture" emotion
            query_vec = np.random.normal(0, 0.1, self.dim)
            sims = {n: 1 - cosine(query_vec, self.vectors[n]) for n in self.vectors}
            strongest = max(sims, key=sims.get)
            new_vec = self.vectors[strongest] + np.random.normal(0, 0.12, self.dim)
            self.add_emotion(f"fracture_{self.turn}", new_vec, val=0.28)
            return

        # Blend emotions
        weights = [self.vals[m] for m in matches]
        vecs = [self.vectors[m] for m in matches]
        avg_vec = np.average(vecs, weights=weights, axis=0)
        min_vec, max_vec = np.min(vecs, axis=0), np.max(vecs, axis=0)

        concat = (
            torch.tensor(np.concatenate([avg_vec, min_vec, max_vec]))
            .float()
            .to(self.device)
        )
        blend_vec = self.blend_mlp(concat.unsqueeze(0)).squeeze().cpu().numpy()

        co_act = max(weights)
        if co_act > self.co_act_thresh:
            blend_name = (
                "-".join(sorted(matches[:4])) if len(matches) > 1 else matches[0]
            )
            self.add_emotion(blend_name, blend_vec, val=co_act * 0.92)

            for m in matches:
                self.G.add_edge(blend_name, m, weight=0.82, type="blend_spring")

            if any(
                word in text_lower
                for word in ["event", "agent", "object", "cause", "relief"]
            ):
                self.vals[blend_name] += 0.1

        # Update history + LSTM
        self.history.append({n: self.vectors[n] for n in matches[:5]})
        if len(self.history) > 0:
            seq = (
                torch.tensor([list(d.values()) for d in self.history])
                .float()
                .to(self.device)
                .unsqueeze(0)
            )
            next_pred, _ = self.temporal_lstm(seq)
            for i, n in enumerate(matches[:5]):
                if i < next_pred.shape[1]:
                    self.vals[n] += next_pred[0, i].mean().item() * 0.05

        self.propagate_tension()

        # Optional resonance print (roleplay flavored)
        if co_act > 0.82 and random.random() < 0.28:
            print("🌌 Resonance cascade — lattice vibrating with tension.")

    def get_roleplay_emotion(self, style, context):
        """Get emotion for roleplay output"""
        dominant = max(self.vals, key=self.vals.get) if self.vals else "neutral"
        return f"[{style}] Feeling {dominant} — {context}"

    def get_character_reaction(self, emotion, event):
        """Get character reaction to an event"""
        return f"Character reacts to '{event}' with {emotion} energy."

    def _spectral_init(self):
        """Initialize spectral properties (placeholder for future expansion)"""
        pass


# Quick self-test
if __name__ == "__main__":
    net = EmotionNet()
    print(net.get_roleplay_emotion("gentle", "I feel happy today"))
    net.process_text_input("I am so angry and frustrated right now!")
    print("Emotional state updated successfully.")
