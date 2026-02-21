# python/python-junk-box/[LATTICE_VIZ].py
# 📊 v0.2 – Lattice visualizer with breathing animation (static + GIF)
# Outputs: base64 PNG or GIF, text fallback
# Dependencies: matplotlib, networkx, numpy (all available)

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import io
import base64
import numpy as np
from typing import Dict, List, Tuple

class LatticeVisualizer:
    def __init__(self, lattice):
        self.lattice = lattice
        self.G = nx.Graph()

    def build_graph(self, min_val: float = 0.25, max_nodes: int = 40):
        self.G.clear()
        sorted_nodes = sorted(
            self.lattice.nodes.items(),
            key=lambda x: x[1]["value"],
            reverse=True
        )[:max_nodes]
        
        for node, data in sorted_nodes:
            if data["value"] >= min_val:
                size = data["value"] * 800
                color = self._get_node_color(node, data["value"])
                self.G.add_node(node, size=size, value=data["value"], color=color)

        for a, targets in self.lattice.bleed_links.items():
            for b, strength in targets.items():
                if a in self.G and b in self.G and strength >= 0.4:
                    self.G.add_edge(a, b, weight=strength * 3)

    def _get_node_color(self, node: str, val: float) -> str:
        if any(k in node for k in ["joy", "spark", "hope"]):
            return "#FFD700"
        elif any(k in node for k in ["awe", "wonder"]):
            return "#00BFFF"
        elif any(k in node for k in ["dread", "fear", "void"]):
            return "#4B0082"
        elif any(k in node for k in ["rage", "anger", "frustr"]):
            return "#FF4500"
        elif any(k in node for k in ["ache", "despair"]):
            return "#8B0000"
        else:
            r = int(255 * (val / 1.0))
            b = int(255 * (1 - val / 1.0))
            return f"#{r:02x}00{b:02x}"

    def plot_static(self, title: str = "Emotional Lattice", return_base64: bool = True):
        self.build_graph()
        if not self.G.nodes:
            return "No nodes above threshold."

        fig, ax = plt.subplots(figsize=(12, 10))
        pos = nx.spring_layout(self.G, k=0.35, iterations=50)

        edges = self.G.edges(data=True)
        nx.draw_networkx_edges(self.G, pos, width=[d["weight"] for _,_,d in edges],
                               alpha=0.5, edge_color="gray", ax=ax)

        nodes = self.G.nodes(data=True)
        nx.draw_networkx_nodes(self.G, pos,
                               node_size=[d["size"] for _,d in nodes],
                               node_color=[d["color"] for _,d in nodes],
                               alpha=0.9, ax=ax)

        nx.draw_networkx_labels(self.G, pos, font_size=8, font_weight="bold", ax=ax)
        ax.set_title(title)
        ax.axis("off")

        if return_base64:
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
            buf.seek(0)
            b64 = base64.b64encode(buf.read()).decode("utf-8")
            plt.close(fig)
            return f"data:image/png;base64,{b64}"
        else:
            plt.show()
            plt.close(fig)
            return "Plot displayed (local only)"

    def animate(self, frames: int = 60, interval: int = 100, title: str = "Breathing Lattice"):
        self.build_graph(min_val=0.25, max_nodes=40)
        if not self.G.nodes:
            return "No nodes to animate."

        fig, ax = plt.subplots(figsize=(12, 10))
        pos = nx.spring_layout(self.G, k=0.35, iterations=20)

        def update(frame):
            ax.clear()
            ax.set_title(f"{title} - frame {frame}")

            for node in pos:
                pos[node] = (pos[node][0] + np.random.normal(0, 0.005),
                             pos[node][1] + np.random.normal(0, 0.005))

            edges = self.G.edges(data=True)
            nx.draw_networkx_edges(self.G, pos,
                                   width=[d["weight"] for _,_,d in edges],
                                   alpha=0.5, edge_color="gray", ax=ax)

            nodes = self.G.nodes(data=True)
            nx.draw_networkx_nodes(self.G, pos,
                                   node_size=[d["size"] for _,d in nodes],
                                   node_color=[d["color"] for _,d in nodes],
                                   alpha=0.9, ax=ax)

            nx.draw_networkx_labels(self.G, pos, font_size=8, font_weight="bold", ax=ax)
            ax.axis("off")

        ani = FuncAnimation(fig, update, frames=frames, interval=interval, repeat=True)

        buf = io.BytesIO()
        ani.save(buf, format='gif', writer='pillow', fps=10)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)

        return f"data:image/gif
