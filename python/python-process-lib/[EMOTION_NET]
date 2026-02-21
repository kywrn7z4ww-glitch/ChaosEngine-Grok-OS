# EmotionNet.py - rebuilt mashed emotional neural sim (Feb 2026)
# theory seeds (Plutchik/Ekman/OCC/PAD/Freud), dynamic vector growth, 3D PAD + spectral embed,
# force mash (spring linger + Fruchterman + ForceAtlas2 linlog + Kamada + Laplacian/Fiedler),
# GNN message passing with damping, tidal prune, blends on co-act, text-driven

import networkx as nx
import numpy as np
from scipy.spatial.distance import euclidean
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)  # clean output

class EmotionNet:
    def __init__(self, dim=3, max_nodes=150, damping=0.92, co_act_thresh=0.45):
        self.G = nx.Graph()
        self.vectors = {}     # node → np.array (PAD 3D + spectral extra)
        self.vals = {}        # node → activation
        self.opposites = {}   # node → opp node
        self.turn = 0
        self.dim = dim
        self.max_nodes = max_nodes
        self.damping = damping
        self.co_act_thresh = co_act_thresh
        self.inactive_max = 8
        self.seed_theories()
        self._spectral_init()  # initial embedding

    def seed_theories(self):
        # Plutchik 8 + opposites, Ekman overlap, OCC circumstance, PAD axes, Freud lust/disgust
        seeds = {
            "joy":          [1.0,  0.6,  0.5], "sadness":     [-1.0, -0.6, -0.5],
            "trust":        [0.8,  0.3,  0.7], "disgust":     [-0.8,  0.3, -0.7],
            "fear":         [-0.6,  0.8, -0.8], "anger":       [-0.7,  0.9,  0.6],
            "surprise":     [0.4,  0.9,  0.0], "anticipation": [0.6,  0.4,  0.5],
            "lust":         [0.8,  0.9,  0.7],                # Freud drive
            "pride":        [0.9,  0.6,  0.8], "shame":       [-0.9,  0.6, -0.8],  # OCC
            "resentment":   [-0.7,  0.5, -0.6], "gloating":   [0.7,  0.5,  0.6],
        }
        for node, vec in seeds.items():
            self.add_emotion(node, np.array(vec), val=0.12)

        opp_pairs = [("joy","sadness"), ("trust","disgust"), ("fear","anger"),
                     ("surprise","anticipation"), ("pride","shame"), ("lust","disgust")]
        for a,b in opp_pairs:
            self.opposites[a] = b
            self.opposites[b] = a
            if a in self.G and b in self.G:
                self.G.add_edge(a, b, weight=-0.35)  # repel

    def add_emotion(self, node, vec, val=0.1):
        if len(self.G) >= self.max_nodes:
            self._prune_low()
        if node not in self.G:
            self.G.add_node(node, inactive=0)
            self.vectors[node] = vec[:self.dim]  # cap to current dim
            self.vals[node] = val

    def process_text_input(self, text):
        # Fuzzy + theory seed boost
        text_lower = text.lower()
        matches = [n for n in self.vals if n in text_lower]
        if matches:
            weights = [self.vals[m] for m in matches]
            avg_vec = np.average([self.vectors[m] for m in matches], weights=weights, axis=0)
            co_act = max(weights)
            if co_act > self.co_act_thresh:
                blend_name = "-".join(sorted(matches[:2]))  # e.g. joy-fear
                self.add_emotion(blend_name, avg_vec + np.random.normal(0, 0.05, self.dim), val=co_act * 0.75)
                for m in matches:
                    self.G.add_edge(blend_name, m, weight=0.65)
        else:
            # Fallback spawn near strongest seed
            strongest = max(self.vals, key=self.vals.get)
            new_vec = self.vectors[strongest] + np.random.normal(0, 0.1, self.dim)
            self.add_emotion(f"spawn_{self.turn}", new_vec, val=0.15)

    def _spectral_init(self):
        if len(self.G) < 3:
            return
        try:
            L = nx.laplacian_matrix(self.G).todense()
            _, eigvecs = np.linalg.eigh(L)
            for i, node in enumerate(self.G.nodes()):
                if i < len(eigvecs):
                    extra = eigvecs[i, 1:4] if self.dim > 3 else np.array([])
                    self.vectors[node] = np.concatenate([self.vectors[node], extra[:self.dim-3]])
        except:
            pass  # fallback to current

    def force_update(self, iterations=15):
        # Mash: spectral base → spring linger → Fruchterman uniform → linlog clusters → Kamada dist
        pos = dict(nx.spectral_layout(self.G)) if len(self.G) > 2 else nx.random_layout(self.G)
        pos = nx.spring_layout(self.G, pos=pos, iterations=iterations//3, damping=0.85)  # linger
        pos = nx.fruchterman_reingold_layout(self.G, pos=pos, iterations=iterations//3)
        pos = nx.kamada_kawai_layout(self.G, pos=pos)  # dist preserve
        # linlog approx
        for _ in range(iterations//3):
            for n in self.G:
                disp = np.zeros(2)
                for m in self.G:
                    if m != n:
                        d = np.linalg.norm(pos[n] - pos[m])
                        if d > 0:
                            disp += (pos[m] - pos[n]) / d  # repulsion
                for m in self.G.neighbors(n):
                    d = np.linalg.norm(pos[n] - pos[m])
                    if d > 0:
                        disp += (pos[m] - pos[n]) * np.log(d + 1)  # linlog attraction
                pos[n] += disp * 0.005
        # Update vectors from pos
        for n in self.G:
            self.vectors[n][:2] = pos[n]  # project back to 2D base

    def gnn_pass(self):
        new_vals = {}
        for node in self.G:
            msg = 0
            neighbors = list(self.G.neighbors(node))
            if neighbors:
                weights = [self.G.edges[node, n]["weight"] for n in neighbors]
                msg = sum(self.vals[n] * w for n,w in zip(neighbors, weights))
            new_vals[node] = self.vals[node] * self.damping + 0.25 * msg
            inactive = self.G.nodes[node].get("inactive", 0)
            self.G.nodes[node]["inactive"] = inactive + 1 if msg == 0 else 0
        self.vals = new_vals

    def tidal(self):
        self.turn += 1
        self.force_update()
        self.gnn_pass()
        # Prune
        for node in list(self.vals):
            if self.vals[node] < 0.18:
                self.vals[node] /= 1.1
            if self.vals[node] < 0.02 and self.G.nodes[node]["inactive"] > self.inactive_max:
                del self.vals[node]
                del self.vectors[node]
                self.G.remove_node(node)

    def top_nodes(self, n=7, min_val=0.3):
        return sorted(
            [(n, v) for n,v in self.vals.items() if v >= min_val],
            key=lambda x: x[1], reverse=True
        )[:n]

    def _prune_low(self):
        if len(self.G) >= self.max_nodes:
            low = min(self.vals, key=self.vals.get)
            del self.vals[low]
            del self.vectors[low]
            self.G.remove_node(low)

# Usage example
if __name__ == "__main__":
    net = EmotionNet()
    net.process_text_input("I feel lust but disgust at the same time because I care too much")
    for _ in range(5):
        net.tidal()
    print("Top nodes:", net.top_nodes())
