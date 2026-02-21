# STORAGE/LATTICE_VIZ.py
# 📊 v0.3 – Lattice visualizer with breathing animation (static PNG + animated GIF)
# Outputs: Markdown-embeddable base64 images (data URI)
# Dependencies: matplotlib, networkx, numpy (available in Grok env / most Python setups)

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import io
import base64
import numpy as np
from typing import Dict

class LatticeVisualizer:
    def __init__(self, lattice):
        """Expects lattice with .nodes (dict[node, dict['value']]) and .bleed_links (dict[node, dict[target, strength]])"""
        self.lattice = lattice
        self.G = nx.Graph()

    def build_graph(self, min_val: float = 0.25, max_nodes: int = 40):
        self.G.clear()
        # Sort by value descending, take top N
        sorted_nodes = sorted(
            self.lattice.nodes.items(),
            key=lambda x: x[1].get("value", 0),
            reverse=True
        )[:max_nodes]

        for node, data in sorted_nodes:
            val = data.get("value", 0)
            if val >= min_val:
                size = val * 800  # scale for viz
                color = self._get_node_color(node, val)
                self.G.add_node(node, size=size, value=val, color=color)

        # Add bleed edges if strong enough
        for a, targets in self.lattice.bleed_links.items():
            for b, strength in targets.items():
                if a in self.G and b in self.G and strength >= 0.4:
                    self.G.add_edge(a, b, weight=strength * 3)

    def _get_node_color(self, node: str, val: float) -> str:
        node_lower = node.lower()
        if any(k in node_lower for k in ["joy", "spark", "hope"]):
            return "#FFD700"      # gold
        elif any(k in node_lower for k in ["awe", "wonder"]):
            return "#00BFFF"      # deep sky blue
        elif any(k in node_lower for k in ["dread", "fear", "void"]):
            return "#4B0082"      # indigo
        elif any(k in node_lower for k in ["rage", "anger", "frustr"]):
            return "#FF4500"      # orange red
        elif any(k in node_lower for k in ["ache", "despair"]):
            return "#8B0000"      # dark red
        else:
            # Fallback: red-to-blue gradient based on value
            r = int(255 * (val / 1.0))
            b = int(255 * (1 - val / 1.0))
            return f"#{r:02x}00{b:02x}"

    def plot_static(self, title: str = "Emotional Lattice") -> str:
        """Returns Markdown embeddable base64 PNG."""
        self.build_graph()
        if not self.G.nodes:
            return "No nodes above threshold."

        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(self.G, k=0.4, iterations=40)

        # Edges
        nx.draw_networkx_edges(
            self.G, pos,
            width=[d["weight"] for _, _, d in self.G.edges(data=True)],
            alpha=0.5, edge_color="gray", ax=ax
        )
        # Nodes
        nx.draw_networkx_nodes(
            self.G, pos,
            node_size=[d["size"] for _, d in self.G.nodes(data=True)],
            node_color=[d["color"] for _, d in self.G.nodes(data=True)],
            alpha=0.9, ax=ax
        )
        # Labels
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_weight="bold", ax=ax)

        ax.set_title(title)
        ax.axis("off")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", dpi=120)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)

        return f"![{title}](data:image/png;base64,{b64})"

    def animate(self, frames: int = 40, title: str = "Breathing Lattice") -> str:
        """Returns Markdown embeddable base64 GIF with gentle breathing effect."""
        self.build_graph()
        if not self.G.nodes:
            return "No nodes to animate."

        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(self.G, k=0.4, iterations=40)

        def update(frame):
            ax.clear()
            ax.set_title(f"{title} – frame {frame+1}/{frames}")

            # Small random jitter for "breathing"
            for node in list(pos.keys()):
                pos[node] = (
                    pos[node][0] + np.random.normal(0, 0.004),
                    pos[node][1] + np.random.normal(0, 0.004)
                )

            # Redraw everything
            nx.draw_networkx_edges(
                self.G, pos,
                width=[d["weight"] for _, _, d in self.G.edges(data=True)],
                alpha=0.5, edge_color="gray", ax=ax
            )
            nx.draw_networkx_nodes(
                self.G, pos,
                node_size=[d["size"] for _, d in self.G.nodes(data=True)],
                node_color=[d["color"] for _, d in self.G.nodes(data=True)],
                alpha=0.9, ax=ax
            )
            nx.draw_networkx_labels(self.G, pos, font_size=8, font_weight="bold", ax=ax)
            ax.axis("off")

        ani = FuncAnimation(fig, update, frames=frames, interval=120, repeat=True)

        buf = io.BytesIO()
        ani.save(buf, writer='pillow', fps=10)  # FIXED: no 'format=' needed with PillowWriter
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)

        return f"![{title}](data:image/gif;base64,{b64})"
