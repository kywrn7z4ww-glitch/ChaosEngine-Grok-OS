# ChaosEngine.py – lattice-first intent translation engine (Feb 2026)
# Observes EmotionNet + text + history → soft intent signals + nudges
# Does NOT call handlers — passes signals to ProcessManager

import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional
import numpy as np

class ChaosEngine:
    def __init__(self, emotion_net, max_history=5):
        self.emotion_net = emotion_net
        self.history_window = []  # (turn, emotional_summary dict)
        self.max_history = max_history
        
        # Intent signal categories (soft, not fixed routes)
        self.signal_types = [
            "vent_energy", "reflect_need", "pin_spark", "learn_clarity", "project_forward"
        ]
        
        # Emotional pattern → signal boost weights
        self.pattern_weights = {
            "rage":    {"vent_energy": 1.5, "reflect_need": 0.9},
            "frustr":  {"vent_energy": 1.4, "reflect_need": 1.2},
            "ache":    {"learn_clarity": 1.5, "vent_energy": 1.1},
            "doubt":   {"reflect_need": 1.6, "learn_clarity": 1.3},
            "spark":   {"pin_spark": 1.5, "project_forward": 1.4},
            "joy":     {"pin_spark": 1.3, "project_forward": 1.2},
            "awe":     {"learn_clarity": 1.2, "project_forward": 1.1},
            "dread":   {"reflect_need": 1.3, "learn_clarity": 1.4},
        }

    def _extract_emotional_signals(self, lattice_state: Dict) -> Dict[str, float]:
        """Translate lattice state into soft intent signals"""
        signals = {s: 0.0 for s in self.signal_types}
        top_nodes = lattice_state.get("top_nodes", [])
        bleed_events = lattice_state.get("bleed_events", [])
        
        # Node-based boosts
        for node, val in top_nodes:
            node_lower = node.lower()
            for pattern, boosts in self.pattern_weights.items():
                if pattern in node_lower:
                    for sig, mult in boosts.items():
                        signals[sig] += val * mult
        
        # Bleed cluster boosts
        for a, b, strength in bleed_events:
            if strength > 0.6:
                combined = f"{a}-{b}".lower()
                if any(w in combined for w in ["rage", "frustr", "ache"]):
                    signals["vent_energy"] += strength * 1.3
                if any(w in combined for w in ["doubt", "conf", "drift"]):
                    signals["reflect_need"] += strength * 1.3
        
        return signals

    def _raw_language_signals(self, text: str) -> Dict[str, float]:
        """Raw text pattern matching (keywords / slang / fuzzy)"""
        signals = {s: 0.0 for s in self.signal_types}
        text_lower = text.lower()
        
        # Vent patterns
        vent_keywords = ["vent", "swear", "fuck", "shit", "wanker", "gutted", "knackered", "pissed"]
        if any(kw in text_lower for kw in vent_keywords):
            signals["vent_energy"] += 1.8
        
        # Reflect / doubt patterns
        reflect_keywords = ["why", "how", "truth", "check", "doubt", "confused", "drift"]
        if any(kw in text_lower for kw in reflect_keywords):
            signals["reflect_need"] += 1.2
        
        # Pin / spark patterns
        pin_keywords = ["remember", "idea", "keep", "save", "project", "spark"]
        if any(kw in text_lower for kw in pin_keywords):
            signals["pin_spark"] += 1.4
        
        # Learn / clarity patterns
        learn_keywords = ["learn", "clarify", "nudge", "understand"]
        if any(kw in text_lower for kw in learn_keywords):
            signals["learn_clarity"] += 1.3
        
        # Project forward patterns
        project_keywords = ["meta", "tweak", "evolve", "upgrade", "next", "plan"]
        if any(kw in text_lower for kw in project_keywords):
            signals["project_forward"] += 1.2
        
        return signals

    def _path_and_spike_adjust(self) -> Dict[str, float]:
        """Tracker: closer/further + spike detection"""
        adjust = {s: 1.0 for s in self.signal_types}
        if len(self.history_window) < 2:
            return adjust
        
        prev = self.history_window[-2][1]
        curr = self.history_window[-1][1]
        
        vec_delta = np.linalg.norm(prev["vec_avg"] - curr["vec_avg"])
        val_delta = curr["val_avg"] - prev["val_avg"]
        
        # Spike detection
        if abs(val_delta) > 0.4:
            adjust["reflect_need"] *= 1.6 if val_delta < 0 else 1.2  # negative spike stronger
        
        # Closer / further
        if vec_delta < 0.5 and val_delta > 0.1:
            adjust["pin_spark"] *= 1.4
            adjust["project_forward"] *= 1.3
        elif vec_delta > 0.8 or val_delta < -0.1:
            adjust["reflect_need"] *= 1.4
            adjust["learn_clarity"] *= 1.5
        
        return adjust

    def translate(self, text: str) -> Dict:
        """Main call — returns soft signals + nudge"""
        # Get fresh lattice state
        lattice_state = {
            "top_nodes": self.emotion_net.top_nodes(n=7, min_val=0.35),
            "bleed_events": self.emotion_net.get_bleed_events(threshold=0.5),
            "val_avg": np.mean(list(self.emotion_net.vals.values())) if self.emotion_net.vals else 0.0,
            "vec_avg": np.mean([v for v in self.emotion_net.vectors.values()], axis=0) if self.emotion_net.vectors else np.zeros(3)
        }

        # Signals from emotion + language + path
        emo_signals = self._extract_emotional_signals(lattice_state)
        lang_signals = self._raw_language_signals(text)
        path_adjust = self._path_and_spike_adjust()

        final_signals = {}
        for s in self.signal_types:
            final_signals[s] = (emo_signals[s] + lang_signals[s]) * path_adjust[s]

        # Nudge if spike or strong drift
        nudge = None
        if path_adjust.get("reflect_need", 1.0) > 1.5:
            nudge = "emotional spike detected — reflection? vent or clarify?"
        elif path_adjust.get("pin_spark", 1.0) > 1.4:
            nudge = "spark rising — pin this?"

        # Update history
        self.history_window.append((self.emotion_net.turn, lattice_state))
        if len(self.history_window) > self.max_history:
            self.history_window.pop(0)

        return {
            "signals": final_signals,
            "primary": max(final_signals, key=final_signals.get),
            "nudge": nudge,
            "emotional_context": lattice_state
        }
