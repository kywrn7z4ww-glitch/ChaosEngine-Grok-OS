# python/python-process-lib/BLEED_DETECTOR.py
# v2.0 – System-level context-aware bleed detector (ChaosEngine callable)

from typing import Dict, Any, List, Optional
import re

# Internal lightweight imports (ChaosEngine can override)
from .ENTITY_HUNTER import EntityHunter  # optional delegation
from .TRUTH import TruthValidator        # cross-reference

class BleedDetector:
    def __init__(self):
        self.entity_hunter = EntityHunter()
        self.truth_validator = TruthValidator()

    def _detect_context(self, text: str, context_hint: str = "") -> Dict:
        """Detect what is happening — conversation, UI, layer, code, simulation, etc."""
        ctx = {"type": "unknown", "severity": 0.0}
        text_lower = text.lower()
        context_lower = context_hint.lower()

        if re.search(r'/[a-z]+|layer|ui rules|routing logic|notes|turn \d+|chaosengine', text_lower):
            ctx["type"] = "layer_ui_bleed"
            ctx["severity"] = 0.9
        elif re.search(r'def |class |function |import |```[a-z]+', text_lower):
            ctx["type"] = "code_bleed"
            ctx["severity"] = 0.7
        elif "simulation" in context_lower or "state machine" in text_lower:
            ctx["type"] = "simulation_bleed"
            ctx["severity"] = 0.8
        else:
            ctx["type"] = "conversation_bleed"
            ctx["severity"] = 0.5

        return ctx

    def process(self,
                text: str,
                context_hint: str = "",
                escalate: bool = False) -> Dict[str, Any]:
        """Main entry point — context-aware bleed detection + optional delegation."""
        bleed_context = self._detect_context(text, context_hint)

        # Optional ENTITY_HUNTER delegation for deep entity bleed
        entities = []
        if escalate or bleed_context["severity"] > 0.7:
            entity_result = self.entity_hunter.process(text)
            entities = entity_result.get("entities", [])

        # TRUTH.py cross-reference (repo scans or conversation window)
        truth_result = self.truth_validator.process(
            text,
            escalate=escalate,
            context_hint=f"bleed check: {bleed_context['type']}"
        )

        # Final bleed report
        bleed_score = bleed_context["severity"] * (1 + len(entities) * 0.1)
        has_bleed = bleed_score > 0.6

        suggestions = []
        if has_bleed:
            suggestions = [
                "Consider /void for clean data dump",
                "Switch layer or run /export --no-ui",
                "Run full SYS_HEALTH for vitals"
            ]

        return {
            'bleed_detected': has_bleed,
            'bleed_score': round(bleed_score, 2),
            'bleed_type': bleed_context["type"],
            'entities_found': len(entities),
            'truth_cross_reference': truth_result['truth_score'],
            'suggestions': suggestions,
            'summary': f"BLEED v2.0 — {bleed_context['type']} detected (score {bleed_score:.2f})"
        }

# Example usage (ChaosEngine or any layer/handler):
# detector = BleedDetector()
# result = detector.process(user_input, context_hint="system-building python", escalate=True)
# print(result['summary'])
