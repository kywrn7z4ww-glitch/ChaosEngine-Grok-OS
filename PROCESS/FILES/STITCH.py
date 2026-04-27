# python/python-process-lib/STITCH.py
# v1 – Smart document & code stitcher with internal validation, self-tracking, and adaptive breaking

from typing import List, Dict, Any, Optional
import re
from difflib import SequenceMatcher

# Temporary lightweight bleed check until full BLEED_DETECTOR rework (system-level)
from .BLEED_DETECTOR import BleedDetector  # type: ignore

class Stitcher:
    def __init__(self):
        self.bleed_detector = BleedDetector()  # lightweight internal use only
        self.stitch_map: List[Dict] = []       # self-tracking log

    def _clean_section(self, text: str) -> str:
        """Strip conversation/UI/amendments/meta/bleed before any processing."""
        # Remove common bleed patterns
        text = re.sub(r'(?i)/[a-z]+|ChaosEngine|Grok OS|layer indicator|amended in editor|UI Rules|Routing Logic|Notes|turn \d+', '', text)
        text = re.sub(r'\[turn\]|\[xlanzilla@root ~\]\$|EmotionNet|Emoji palette|Chatter cap', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _detect_content_type(self, chunks: List[Dict[str, Any]]) -> str:
        """Smart auto-detect: code vs document vs hybrid."""
        code_score = 0
        total = len(chunks)
        for chunk in chunks:
            content = chunk.get('content', chunk.get('full_content', ''))
            if re.search(r'(def |class |function |import |from |if __name__|```[a-z]+)', content, re.IGNORECASE):
                code_score += 1
        ratio = code_score / total if total > 0 else 0
        if ratio > 0.6:
            return "code"
        elif ratio > 0.3:
            return "hybrid"
        return "document"

    def _predict_max_tokens(self) -> int:
        """QOL: One-shot LLM self-query for current max output tokens (cached per session)."""
        # In real deployment this would be a tiny internal call to the current LLM
        # For now we use a safe default; replace with actual prompt response when wired
        return 8192  # placeholder — will be replaced by real auto-detect in production

    def _validate_section(self, section: str, index: int) -> Dict:
        """Internal validation + bleed stripping for every section."""
        cleaned = self._clean_section(section)
        bleed_result = self.bleed_detector.process(cleaned)  # lightweight call
        passed = bleed_result.get('bleed_detected', False) is False
        self.stitch_map.append({
            'section': index,
            'original_length': len(section),
            'cleaned_length': len(cleaned),
            'validation_passed': passed,
            'bleed_score': bleed_result.get('bleed_score', 0.0)
        })
        return {'content': cleaned, 'valid': passed}

    def _insert_adaptive_break(self, content_type: str, previous: str, current: str, index: int) -> str:
        """Smart, context-aware breaking — no rigid rules."""
        if content_type == "code":
            # Function/module boundary detection
            match = re.search(r'(def |class |function )(\w+)', current)
            name = match.group(2) if match else f"block_{index}"
            return f"\n\n—— End of Module: {name} ——\n\n"
        else:
            # Natural topic/section shift for documents
            coherence = SequenceMatcher(None, previous[-200:].lower(), current[:200].lower()).ratio()
            if coherence < 0.7:
                summary = current[:60].strip() + "..." if len(current) > 60 else current
                return f"\n\n—— End of Section: {summary} ——\n\n"
        return "\n\n"  # minimal fallback

    def process(self,
                chunks: List[Dict[str, Any]],
                max_tokens: Optional[int] = None,
                context_hint: str = "") -> Dict[str, Any]:
        """Main entry point — single call with full internal validation + tracking + final check."""
        if not chunks:
            return {'stitched_doc': '', 'stitch_map': [], 'summary': 'No chunks provided'}

        if max_tokens is None:
            max_tokens = self._predict_max_tokens()

        content_type = self._detect_content_type(chunks)
        self.stitch_map = []  # reset tracking

        # Phase 1: Per-section validation + cleaning
        validated_chunks = []
        for i, chunk in enumerate(chunks):
            raw = chunk.get('content', chunk.get('full_content', ''))
            validated = self._validate_section(raw, i)
            if validated['valid']:
                validated_chunks.append(validated['content'])

        # Phase 2: Adaptive assembly with smart breaks
        stitched = []
        current = ""
        for i, section in enumerate(validated_chunks):
            if i == 0:
                current = section
                continue
            break_marker = self._insert_adaptive_break(content_type, current, section, i)
            current += break_marker + section

        stitched.append(current)

        # Phase 3: Final holistic check on complete document
        final_doc = "\n\n".join(stitched)
        final_validation = self._validate_section(final_doc, -1)  # -1 = whole doc
        final_passed = final_validation['valid']

        # Add context_hint awareness (e.g. system-building = extra file/module care)
        if context_hint == "system-building":
            final_doc = f"# System-Building Context\n{context_hint.upper()}\n\n{final_doc}"

        summary = (f"STITCH v1 complete — {len(validated_chunks)} sections, "
                   f"type: {content_type}, final validation: {'PASS' if final_passed else 'WARN'}, "
                   f"max_tokens respected: {max_tokens}")

        return {
            'stitched_doc': final_doc,
            'stitch_map': self.stitch_map,
            'type_detected': content_type,
            'final_validation_passed': final_passed,
            'summary': summary,
            'total_sections': len(validated_chunks)
        }

# Example usage (Luna/ChaosEngine or /export layer):
# stitcher = Stitcher()
# result = stitcher.process(chunks_from_vomit_or_deepdive, max_tokens=8192, context_hint="system-building")
# print(result['summary'])
# print(result['stitched_doc'][:500] + "...")
