# python/python-process-lib/chaos_mgr.py
# ⛓️ v1 – Intent Hub / Router (suggest-only)

from typing import Dict, List

class ChaosManager:
    def __init__(self, lattice):
        self.lattice = lattice  # EMOTIONAL_LATTICE instance

    def estimate_intent(self, text: str) -> str:
        """Simple lattice-based intent estimate."""
        high_nodes = [n for n, d in self.lattice.nodes.items() if d['value'] > 0.5]
        if any(n in high_nodes for n in ['vent', 'frustr', 'ache']):
            return "vent"
        if any(n in high_nodes for n in ['project', 'meta', 'idea']):
            return "project"
        if any(n in high_nodes for n in ['conf', 'doubt', 'surprise']):
            return "clarify"
        return "general"

    def suggest_route(self, text: str) -> str:
        intent = self.estimate_intent(text)
        if "vent" in intent or len(text.split()) > 500:
            return "Route to VOMIT🤮 + FILE_MGR📦? Y/N"
        if "project" in intent or "idea" in text.lower():
            return "Route to FILE_MGR📦 (pin)? Y/N"
        if "conf" in intent or "doubt" in text.lower():
            return "Route to TRUTH🧠? Y/N"
        return "⛓️ Intent unclear – clarify or vent?"

    def decide_tool_call(self, intent: str, conf: float) -> str:
        """Suggest real tool call if low conf."""
        if conf < 0.6:
            if "fact" in intent or "contradict" in intent:
                return "Suggest web_search or browse_page for fact check"
        return ""
