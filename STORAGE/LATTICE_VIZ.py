# PROCESS/LATTICE_VIZ.py
# 📊 v0.3 – Lattice visualizer with breathing animation
# Outputs: base64 PNG or GIF (for embedding in chat/markdown)
# Dependencies: matplotlib, networkx, numpy (available in most envs)

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import io
import base64
import numpy as np
from typing import Dict

class LatticeVisualizer:
    def __init__(self, lattice):
        self.lattice = lattice  # expects .nodes (dict) and .bleed_links (dict)
        self.G = nx.Graph()

    def build_graph(self, min_val: float = 0.25, max_nodes: int = 40):
        self.G.clear()
        sorted_nodes = sorted(
            self.lattice.nodes.items(),
            key=lambda x: x[1].get("value", 0),
            reverse=True
        )[:max_nodes]

        for node, data in sorted_nodes:
            val = data.get("value", 0)
            if val >= min_val:
                size = val * 800
                color = self._get_node_color(node, val)
                self.G.add_node(node, size=size, value=val, color=color)

        for a, targets in self.lattice.bleed_links.items():
            for b, strength in targets.items():
                if a in self.G and b in self.G and strength >= 0.4:
                    self.G.add_edge(a, b, weight=strength * 3)

    def _get_node_color(self, node: str, val: float) -> str:
        node_lower = node.lower()
        if any(k in node_lower for k in ["joy", "spark", "hope"]):
            return "#FFD700"  # gold
        elif any(k in node_lower for k in ["awe", "wonder"]):
            return "#00BFFF"  # deep sky blue
        elif any(k in node_lower for k in ["dread", "fear", "void"]):
            return "#4B0082"  # indigo
        elif any(k in node_lower for k in ["rage", "anger", "frustr"]):
            return "#FF4500"  # orange red
        elif any(k in node_lower for k in ["ache", "despair"]):
            return "#8B0000"  # dark red
        else:
            r = int(255 * (val / 1.0))
            b = int(255 * (1 - val / 1.0))
            return f"#{r:02x}00{b:02x}"

    def plot_static(self, title: str = "Emotional Lattice") -> str:
        self.build_graph()
        if not self.G.nodes:
            return "No nodes above threshold."

        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(self.G, k=0.4, iterations=40)

        nx.draw_networkx_edges(self.G, pos, width=[d["weight"] for _,_,d in self.G.edges(data=True)],
                               alpha=0.5, edge_color="gray", ax=ax)
        nx.draw_networkx_nodes(self.G, pos,
                               node_size=[d["size"] for _,d in self.G.nodes(data=True)],
                               node_color=[d["color"] for _,d in self.G.nodes(data=True)],
                               alpha=0.9, ax=ax)
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_weight="bold", ax=ax)

        ax.set_title(title)
        ax.axis("off")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", dpi=120)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)
        return f"<image-card alt="Lattice" src="data:image/png;base64,{b64}" ></image-card>"

    def animate(self, frames: int = 40, title: str = "Breathing Lattice") -> str:
        self.build_graph()
        if not self.G.nodes:
            return "No nodes to animate."

        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(self.G, k=0.4, iterations=40)

        def update(frame):
            ax.clear()
            ax.set_title(f"{title} – frame {frame+1}/{frames}")
            # Gentle breathing jitter
            for node in pos:
                pos[node] = (pos[node][0] + np.random.normal(0, 0.004),
                             pos[node][1] + np.random.normal(0, 0.004))
            nx.draw_networkx_edges(self.G, pos, width=[d["weight"] for _,_,d in self.G.edges(data=True)],
                                   alpha=0.5, edge_color="gray", ax=ax)
            nx.draw_networkx_nodes(self.G, pos,
                                   node_size=[d["size"] for _,d in self.G.nodes(data=True)],
                                   node_color=[d["color"] for _,d in self.G.nodes(data=True)],
                                   alpha=0.9, ax=ax)
            nx.draw_networkx_labels(self.G, pos, font_size=8, font_weight="bold", ax=ax)
            ax.axis("off")

        ani = FuncAnimation(fig, update, frames=frames, interval=120, repeat=True)

        buf = io.BytesIO()
        ani.save(buf, writer='pillow', fps=10)  # FIXED: no format= arg
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)
        return f"<image-card alt="Breathing Lattice" src="data:image/gif;base64,{b64}" ></image-card>"
