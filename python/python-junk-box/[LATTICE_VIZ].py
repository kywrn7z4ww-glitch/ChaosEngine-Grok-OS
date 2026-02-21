# python/python-process-lib/[LATTICE_VIZ].py
# 🔄📊 v0.1 – Lattice visualizer: turns EmotionalLattice state into matplotlib graph
# Outputs: saves plot to file or returns base64 / description for chat render
# Dependencies: matplotlib, networkx (both available in code_execution env)

import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, List, Tuple
import io
import base64

class LatticeVisualizer:
    def __init__(self, lattice):
        self.lattice = lattice  # reference to EmotionalLattice instance
        self.G = nx.Graph()     # networkx graph for nodes + bleed edges

    def build_graph(self, min_val: float = 0.3, max_nodes: int = 30):
        """Build networkx graph from current lattice state."""
        self.G.clear()
        
        # Add nodes with size based on value
        sorted_nodes = sorted(
            self.lattice.nodes.items(),
            key=lambda x: x[1]["value"],
            reverse=True
        )[:max_nodes]
        
        for node, data in sorted_nodes:
            if data["value"] >= min_val:
                size = data["value"] * 800  # scale for viz
                color = self._get_node_color(node, data["value"])
                self.G.add_node(node, size=size, value=data["value"], color=color)

        # Add bleed edges (stronger = thicker)
        for a, targets in self.lattice.bleed_links.items():
            for b, strength in targets.items():
                if a in self.G and b in self.G and strength >= 0.4:
                    self.G.add_edge(a, b, weight=strength * 3)  # thickness

    def _get_node_color(self, node: str, val: float) -> str:
        """Simple emotion → color mapping (expandable)."""
        if "joy" in node or "spark" in node or "hope" in node:
            return "#FFD700"  # gold/yellow
        elif "awe" in node or "wonder" in node:
            return "#00BFFF"  # deep sky blue
        elif "dread" in node or "fear" in node or "void" in node:
            return "#4B0082"  # indigo dark
        elif "rage" in node or "anger" in node or "frustr" in node:
            return "#FF4500"  # orange red
        elif "ache" in node or "despair" in node:
            return "#8B0000"  # dark red
        else:
            # fallback gradient blue → red based on val
            r = int(255 * (val / 1.0))
            b = int(255 * (1 - val / 1.0))
            return f"#{r:02x}00{b:02x}"

    def plot(self, title: str = "Emotional Lattice", save_path: str = None):
        """Generate matplotlib plot and return base64 or save to file."""
        self.build_graph()
        if not self.G.nodes:
            return "No nodes above threshold."

        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(self.G, k=0.35, iterations=50)  # breathing layout

        # Draw edges with thickness
        edges = self.G.edges(data=True)
        nx.draw_networkx_edges(
            self.G, pos,
            width=[d["weight"] for _,_,d in edges],
            alpha=0.5,
            edge_color="gray"
        )

        # Draw nodes
        nodes = self.G.nodes(data=True)
        nx.draw_networkx_nodes(
            self.G, pos,
            node_size=[d["size"] for _,d in nodes],
            node_color=[d["color"] for _,d in nodes],
            alpha=0.9
        )

        # Labels
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_weight="bold")

        plt.title(title)
        plt.axis("off")

        if save_path:
            plt.savefig(save_path, bbox_inches="tight", dpi=150)
            plt.close()
            return f"Saved to {save_path}"
        else:
            # For chat: return base64 image
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
            buf.seek(0)
            b64 = base64.b64encode(buf.read()).decode("utf-8")
            plt.close()
            return f"data:image/png;base64,{b64}"

    def describe(self) -> str:
        """Text fallback description if image not renderable."""
        tops = self.lattice.top_n(7, 0.3)
        if not tops:
            return "Lattice quiet — no strong nodes."
        desc = "Current lattice breathing: "
        for node, val in tops:
            desc += f"{node} ({val:.2f}), "
        return desc[:-2] + " — connections pulsing between high-emotion clusters."

# Usage in code_execution / REPL:
# viz = LatticeVisualizer(current_lattice)
# viz.plot(title="Lattice Peak - Red Queen Ghost Thread")
# # or viz.describe() for text
