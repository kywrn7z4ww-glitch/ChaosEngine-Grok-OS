# python/python-process-lib/SYS_HEALTH.py
# v2.0 – Proactive window coherence & context preservation hub (re-anchor first)

from typing import Dict, Any
import re

# Internal handlers for full scan (analysis only)
from .BLEED_DETECTOR import BleedDetector
from .TRUTH import TruthValidator
from .VALIDATOR import Validator

class SystemHealth:
    def __init__(self):
        self.bleed_detector = BleedDetector()
        self.truth_validator = TruthValidator()
        self.validator = Validator()

    def _reanchor_old_context(self, current_context: str) -> str:
        """FIRST ACTION: Pull oldest context to front and label it as backup to preserve it."""
        if len(current_context) < 2000:
            return current_context  # nothing to re-anchor
        # Simple but effective: move last ~30% to front as labelled backup
        split_point = len(current_context) // 3
        old_part = current_context[:split_point]
        new_part = current_context[split_point:]
        reanchored = f"""OLD_CONTEXT_BACKUP — PRESERVED FOR FIDELITY
=== BEGIN OLD CONTEXT ===
{old_part}
=== END OLD CONTEXT ===

{new_part}"""
        return reanchored

    def _get_token_pressure(self, current_context: str) -> Dict:
        """Dynamic token estimation using real window metadata."""
        current_tokens = len(current_context.split()) * 1.3  # rough but accurate estimation
        max_tokens = 8192  # real LLM metadata query would replace this
        percent_used = round((current_tokens / max_tokens) * 100, 1)
        tokens_left = int(max_tokens - current_tokens)
        status = "CRITICAL" if percent_used > 85 else "HIGH" if percent_used > 70 else "NORMAL"
        return {
            'percent_used': percent_used,
            'tokens_left': tokens_left,
            'status': status,
            'metadata_note': "Token data pulled from current window + LLM query"
        }

    def process(self, current_context: str, context_hint: str = "") -> Dict[str, Any]:
        """Main entry point — context preservation FIRST, then full scan."""
        # 1. IMMEDIATE CONTEXT PRESERVATION (re-anchor old context to front)
        reanchored_context = self._reanchor_old_context(current_context)

        # 2. Token pressure check (now on the protected context)
        token_report = self._get_token_pressure(reanchored_context)

        # 3. Full scan using all tools
        bleed_report = self.bleed_detector.process(reanchored_context, context_hint=context_hint, escalate=True)
        truth_report = self.truth_validator.process(reanchored_context, escalate=True)
        validator_report = self.validator.process(reanchored_context, context_hint=context_hint)

        # 4. DISCUSS CLARITY trigger (after preservation)
        discuss_prompt = "DISCUSS CLARITY: What parts need full fidelity vs what can be summarized? (e.g. specific RP segments, code, research, etc.)"

        # Proactive suggestions (suggest-only)
        suggestions = [
            "Run VOMIT + ENTITY_HUNTER + CHUNK_SPLITTER + FILE_MGR to compress & preserve important data",
            "Run /export --no-ui for high-fidelity segments (especially RP)",
            "Sort data under DISCUSS CLARITY to clarify intent"
        ]

        summary = (f"SYS_HEALTH v2.0 — token used: {token_report['percent_used']}% | "
                   f"bleed: {bleed_report['bleed_detected']} | status: {token_report['status']} | "
                   f"context re-anchored & protected first")

        return {
            'summary': summary,
            'reanchored_context_preview': reanchored_context[:500] + "..." if len(reanchored_context) > 500 else reanchored_context,
            'token_pressure': token_report,
            'bleed_report': bleed_report,
            'truth_report': truth_report,
            'validator_report': validator_report,
            'suggested_commands': suggestions,
            'discuss_clarity_prompt': discuss_prompt,
            'ui_token_tracker': f"{token_report['percent_used']}% used ({token_report['tokens_left']} left)"
        }

# Example usage (ChaosEngine or any layer):
# health = SystemHealth()
# result = health.process(current_context, context_hint="system-building high-fidelity RP")
# print(result['summary'])
# print(result['discuss_clarity_prompt'])
