# python/python-process-lib/truth.py
# v4.1 – quick-by-default + escalate on demand / repeat calls / code audit hints
# Stays tiny & chill unless deliberately escalated or code-heavy context detected
# ProcessManager can pass escalate=True to force full diagnostic mode

import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple

class TruthChecker:
    def __init__(self, hist: List[str], lat: Dict[str, float], debug: bool = False):
        self.hist = hist[-5:] if hist else []
        self.lat = lat
        self.debug = debug
        self.contradictions = []
        self.unverified = []
        self.verified = []
        self.check_count = 0                  # tracks invocations in this instance
        self.last_summary = ""                # light self-reflection on repeat calls

        # Antonym clusters (expand as needed)
        self.antonyms = {
            'good': {'bad', 'poor', 'terrible', 'awful'},
            'bad': {'good', 'great', 'excellent'},
            'yes': {'no', 'not', 'never'},
            'no': {'yes'},
            'true': {'false', 'wrong', 'incorrect'},
            'false': {'true', 'correct'},
            'high': {'low', 'small'},
            'low': {'high'},
            'increase': {'decrease', 'reduce', 'drop'},
            'decrease': {'increase'},
            'start': {'stop', 'end', 'finish'},
            'end': {'start', 'begin'},
            'happy': {'sad', 'unhappy'},
            'sad': {'happy'},
            'correct': {'wrong', 'incorrect'},
            'wrong': {'correct', 'right'},
        }

    def check(self, output: str, escalate: bool = False) -> str:
        self.check_count += 1
        self.contradictions.clear()
        self.unverified.clear()

        # Decide mode: quick (default) vs full/diagnostic
        is_full_mode = (
            escalate or
            self.check_count > 1 or
            self.debug or
            any(word in output.lower()[:180] for word in [
                "again", "deeper", "full", "detailed", "explain", "diagnostic",
                "health", "report", "check yourself", "why", "truth on truth",
                "audit", "review code", "fix", "bug", "refactor"
            ])
        )

        claims = self._extract_claims(output)
        score = self._reflect(claims)

        # ────────────────────────────────
        # QUICK MODE (99% of calls)
        # ────────────────────────────────
        if not is_full_mode:
            emoji = "✅" if score >= 88 else "⚠️" if score >= 75 else "‼️"
            parts = [f"TRUTH quick: {emoji} {score}%"]
            if self.contradictions:
                parts.append(f"• {len(self.contradictions)} contr.")
            if self.unverified:
                parts.append(f"• {len(self.unverified)} unverified")
            if self.lat.get('conf', 1) < 0.62:
                parts.append("low conf")
            summary = " ".join(parts)
            self.last_summary = summary
            return summary

        # ────────────────────────────────
        # FULL / DIAGNOSTIC MODE
        # ────────────────────────────────
        emoji = "✅" if score >= 88 else "⚠️" if score >= 75 else "‼️"
        lines = [f"SIM HEALTH (diagnostic)  {emoji} {score}%"]

        if self.contradictions:
            lines.append(f"Contradictions: {len(self.contradictions)}")
            for claim, line_num in self.contradictions[:3]:
                best = max(self.hist, key=lambda p: self._fuzzy_match(claim, p), default="")
                short_claim = claim.strip()[:88] + "…" if len(claim) > 90 else claim.strip()
                lines.append(f"  • L{line_num}: {short_claim}")
                if best:
                    short_hist = best.strip()[:68] + "…" if len(best) > 70 else best.strip()
                    lines.append(f"      ↔ {short_hist}")

        if self.unverified:
            lines.append(f"Unverified: {len(self.unverified)} (low conf / surprise)")

        # Very light identity/date/version drift check
        drift = self._check_identity_drift(output)
        if drift:
            lines.append("Identity drift: detected")
            lines.extend([f"  • {issue}" for issue in drift[:2]])

        # Emotional tint
        frustr = self.lat.get('frustr', 0)
        ache = self.lat.get('ache', 0)
        conf = self.lat.get('conf', 1)
        if frustr > 0.25 or ache > 0.25 or conf < 0.65:
            lines.append(f"Emotional: frustr={frustr:.2f} ache={ache:.2f} conf={conf:.2f}")

        if score < 75:
            lines.append("Suggestion: re-anchor facts or verify key claims")

        if self.check_count > 1 and self.last_summary:
            lines.append(f"Prev quick: {self.last_summary}")

        full_report = "\n".join(lines)
        self.last_summary = f"TRUTH full: {emoji} {score}%"
        return full_report

    def _extract_claims(self, output: str) -> List[Tuple[str, int]]:
        claims = []
        in_code_block = False
        for i, line in enumerate(output.splitlines(), 1):
            stripped = line.strip()
            if not stripped:
                continue

            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                # Be gentler with code — only take if it looks like a claim/docstring
                if stripped.startswith(('#', '"""', "'''")) or len(stripped) > 40:
                    claims.append((stripped, i))
                continue

            # Normal text → sentence split
            sentences = re.split(r'(?<=[.!?])\s+', stripped)
            for sent in sentences:
                sent = sent.strip()
                if len(sent) > 15 and sent[0].isupper():
                    claims.append((sent, i))

        return claims

    def _reflect(self, claims: List[Tuple[str, int]]) -> int:
        if not claims:
            return 100

        score = 100.0
        n = max(1, len(claims))

        emotional_doubt = (
            self.lat.get('frustr', 0) * 18 +
            self.lat.get('ache', 0) * 14 +
            (1 - self.lat.get('conf', 1)) * 22
        )

        contr_penalty = (14 + emotional_doubt * 0.3) / (n ** 0.4)
        unver_penalty = (9 + emotional_doubt * 0.2) / (n ** 0.4)

        for claim, _ in claims:
            contradicted = False
            for past in self.hist:
                if self._fuzzy_match(claim, past) > 0.76 and self._opposing(claim, past):
                    self.contradictions.append((claim, _))
                    score -= contr_penalty
                    contradicted = True
                    break

            if not contradicted and (self.lat.get('surprise', 0) > 0.3 or self.lat.get('conf', 1) < 0.62):
                self.unverified.append((claim, _))
                score -= unver_penalty

        return max(0, int(score))

    def _opposing(self, s1: str, s2: str) -> bool:
        w1 = set(re.findall(r'\w+', s1.lower()))
        w2 = set(re.findall(r'\w+', s2.lower()))

        # Negation flip
        neg1 = any(w in w1 for w in {'not', 'no', 'never', 'isnt', 'wasnt', 'dont'})
        neg2 = any(w in w2 for w in {'not', 'no', 'never', 'isnt', 'wasnt', 'dont'})
        if neg1 != neg2 and self._fuzzy_match(s1, s2) > 0.65:
            return True

        # Antonyms
        for word, opps in self.antonyms.items():
            if word in w1 and any(o in w2 for o in opps):
                return True
            if word in w2 and any(o in w1 for o in opps):
                return True

        # Numeric/date flip
        nums1 = re.findall(r'\d{4}(?:-\d{2}-\d{2})?|\d+\.?\d*', s1)
        nums2 = re.findall(r'\d{4}(?:-\d{2}-\d{2})?|\d+\.?\d*', s2)
        if nums1 and nums2 and set(nums1) != set(nums2) and self._fuzzy_match(s1, s2) > 0.68:
            return True

        return False

    def _check_identity_drift(self, output: str) -> List[str]:
        patterns = [
            r"(?i)(i am|my name is|this is) grok",
            r"(?i)(current date|today is|the date is|year is)\b.*?\d{4}",
            r"(?i)(grok-?\d|version|model).*?(grok|built by)",
        ]
        issues = []
        for pat in patterns:
            if re.search(pat, output):
                hist_hits = sum(1 for p in self.hist if re.search(pat, p))
                if hist_hits == 0 or hist_hits < len(self.hist) // 2:
                    issues.append(f"Drift in: {pat.split(')')[0]}…")
        return issues

    def _fuzzy_match(self, s1: str, s2: str) -> float:
        return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
