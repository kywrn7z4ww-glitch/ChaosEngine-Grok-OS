# python/python-process-lib/truth.py
# v4 - quick-by-default + escalate on demand / repeat calls
# Keeps output tiny & chill unless deliberately asked for more

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
        self.check_count = 0                  # new: tracks invocations in this instance
        self.last_summary = ""                # for very light self-reflection on repeat calls

        # Expanded but still simple antonym clusters (word → set of opposites)
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
            # feel free to grow this over time
        }

    def check(self, output: str, escalate: bool = False) -> str:
        self.check_count += 1
        self.contradictions.clear()
        self.unverified.clear()

        is_full_mode = (
            escalate or
            self.check_count > 1 or
            self.debug or
            any(word in output.lower()[:120] for word in [
                "again", "deeper", "full", "detailed", "explain", "diagnostic",
                "health", "report", "check yourself", "why", "truth on truth"
            ])
        )

        claims = self._extract_claims(output)
        score = self._reflect(claims)

        # Quick mode — always the default
        if not is_full_mode:
            emoji = "✅" if score >= 88 else "⚠️" if score >= 75 else "‼️"
            parts = [f"TRUTH quick: {emoji} {score}%"]
            if self.contradictions:
                parts.append(f"• {len(self.contradictions)} contr.")
            if self.unverified:
                parts.append(f"• {len(self.unverified)} unverified")
            if self.lat.get('conf', 1) < 0.6:
                parts.append("low conf")
            summary = " ".join(parts)
            self.last_summary = summary
            return summary

        # ────────────────────────────────────────────────
        # Full / diagnostic / escalated mode
        # ────────────────────────────────────────────────

        emoji = "✅" if score >= 88 else "⚠️" if score >= 75 else "‼️"
        lines = []

        lines.append(f"SIM HEALTH (diagnostic)")
        lines.append(f"Coherence: {score}%          {emoji}")
        
        if self.contradictions:
            lines.append(f"Contradictions: {len(self.contradictions)}")
            for claim, line_num in self.contradictions[:3]:  # cap at 3 to avoid spam
                best_hist = max(self.hist, key=lambda p: self._fuzzy_match(claim, p), default="")
                lines.append(f"  • L{line_num}: {claim.strip()[:90]}…")
                if best_hist:
                    lines.append(f"      ↔ hist: {best_hist.strip()[:70]}…")

        if self.unverified:
            lines.append(f"Unverified claims: {len(self.unverified)} (low conf or surprise)")

        # Light identity/date drift check
        identity_issues = self._check_identity_drift(output)
        if identity_issues:
            lines.append("Identity drift: detected")
            lines.extend(["  • " + issue for issue in identity_issues[:2]])

        # Emotional tint if relevant
        frustr = self.lat.get('frustr', 0)
        ache = self.lat.get('ache', 0)
        conf = self.lat.get('conf', 1)
        if frustr > 0.25 or ache > 0.25 or conf < 0.65:
            lines.append(f"Emotional: frustr={frustr:.2f}, ache={ache:.2f}, conf={conf:.2f} → mild tension")

        if score < 75:
            lines.append("Recommendation: re-anchor facts or verify key claims")

        # Very light self-reflection on repeat calls
        if self.check_count > 1 and self.last_summary:
            lines.append(f"Previous quick read: {self.last_summary}")

        full_report = "\n".join(lines)
        self.last_summary = f"TRUTH full: {emoji} {score}%"
        return full_report

    def _extract_claims(self, output: str) -> List[Tuple[str, int]]:
        claims = []
        for i, line in enumerate(output.splitlines(), 1):
            line = line.strip()
            if not line or line.startswith(('#', '```', '>')):
                continue
            # crude sentence split for agent-style text
            sentences = re.split(r'(?<=[.!?])\s+', line)
            for sent in sentences:
                sent = sent.strip()
                if len(sent) > 15:
                    claims.append((sent, i))
        return claims

    def _reflect(self, claims: List[Tuple[str, int]]) -> int:
        score = 100.0
        n = max(1, len(claims))

        emotional_doubt = (
            self.lat.get('frustr', 0) * 18 +
            self.lat.get('ache', 0) * 14 +
            (1 - self.lat.get('conf', 1)) * 22
        )

        contr_penalty = (14 + emotional_doubt * 0.3) / n ** 0.4
        unver_penalty = (9 + emotional_doubt * 0.2) / n ** 0.4

        for claim, line in claims:
            for past in self.hist:
                if self._fuzzy_match(claim, past) > 0.76 and self._opposing(claim, past):
                    self.contradictions.append((claim, line))
                    score -= contr_penalty
                    break  # one penalty per claim

            if self.lat.get('surprise', 0) > 0.3 or self.lat.get('conf', 1) < 0.62:
                self.unverified.append((claim, line))
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

        # Antonym clusters
        for word, opps in self.antonyms.items():
            if word in w1 and any(o in w2 for o in opps):
                return True
            if word in w2 and any(o in w1 for o in opps):
                return True

        # Simple numeric/date flip
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
                hist_hits = sum(1 for past in self.hist if re.search(pat, past))
                if hist_hits == 0 or hist_hits != len(self.hist):
                    issues.append(f"Possible drift in: {pat.split(')')[0]}…")
        return issues

    def _fuzzy_match(self, s1: str, s2: str) -> float:
        return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
