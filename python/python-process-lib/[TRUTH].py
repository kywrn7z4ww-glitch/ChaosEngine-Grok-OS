# python/truth_handler.py (v2 - solid block)
import re
from difflib import SequenceMatcher
from typing import Dict, List

class TruthChecker:
    def __init__(self, hist: List[str], lat: Dict[str, float], debug: bool = False):
        self.hist = hist[-5:]  # cap hist
        self.lat = lat
        self.debug = debug
        self.contradictions = []
        self.unverified = []
        self.verified = []
        self.antonyms = {  # basic pairs for semantic oppose
            'blue': 'red', 'yes': 'no', 'true': 'false', 'good': 'bad', 'high': 'low',
            'london': 'tokyo', 'february': 'july', '2026': '2025'  # domain-specific
        }

    def check(self, output: str) -> str:
        claims = self._extract_claims(output)
        score = self._reflect(claims)
        if self.unverified and self.lat.get('conf', 1) < 0.55:
            return "TRUTH suggest: Unverified claims — verify via web_search? Y/N"  # user control

        if score >= 90 and not self.contradictions:
            return ""  # silent - no spam/poison

        emoji = "✅" if score >= 85 else "⚠️" if score >= 75 else "‼️"
        summary = f"TRUTH: {emoji} {score}% accurate"
        if self.contradictions:
            summary += f" | Contradicts: {len(self.contradictions)}"
        if self.unverified:
            summary += f" | Unverified: {len(self.unverified)}"
        if score < 75:
            summary += " — Possible gaslight, revise? Y/N"  # suggest, no auto

        if self.debug:
            summary += "\nDetails: " + "\n".join([f"L{line}: {c}" for c, line in self.contradictions + self.unverified])

        return summary

    def _extract_claims(self, output: str) -> List[tuple[str, int]]:
        lines = output.split('\n')
        claims = []
        for i, line in enumerate(lines, 1):
            sentences = re.findall(r'([A-Z][^.!?]*[.!?])', line)
            for s in sentences:
                claims.append((s.strip(), i))  # (claim, lineno)
        return claims

    def _reflect(self, claims: List[tuple[str, int]]) -> int:
        score = 100
        for claim, line in claims:
            for past in self.hist:
                if self._fuzzy_match(claim, past) > 0.75 and self._opposing(claim, past):
                    self.contradictions.append((claim, line))
                    score -= 18
            if self.lat.get('surprise', 0) > 0.35 or self.lat.get('ache', 0) > 0.25:
                self.unverified.append((claim, line))
                score -= 12
        return max(0, score)

    def fact_check_approve(self, query: str) -> bool:
        # Stub: real would call web_search / conversation_search if user says Y
        # For test: fake 70% verify
        verified = hash(query) % 10 > 3
        if verified:
            self.verified.append(query)
        return verified

    def _fuzzy_match(self, s1: str, s2: str) -> float:
        return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

    def _opposing(self, s1: str, s2: str) -> bool:
        words1 = set(s1.lower().split())
        words2 = set(s2.lower().split())
        neg1 = any(w in words1 for w in {'not', 'no', 'never', 'false', "isn't", "wasn't"})
        neg2 = any(w in words2 for w in {'not', 'no', 'never', 'false', "isn't", "wasn't"})
        if neg1 != neg2:
            return True
        # Antonym check
        for w in words1:
            ant = self.antonyms.get(w)
            if ant and ant in words2:
                return True
        return False

# Usage in CE sim:
# tc = TruthChecker(hist, lat, debug=False)
# summary = tc.check(generated_output)
# if summary: print(summary)
# if "verify" in summary and user_says_yes: tc.fact_check_approve("claim query")
