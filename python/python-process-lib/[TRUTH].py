# python/python-process-lib/truth.py (v3 - strengthened doubt/reflect/criticism)

import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple

class TruthChecker:
    def __init__(self, hist: List[str], lat: Dict[str, float], debug: bool = False):
        self.hist = hist[-5:]
        self.lat = lat
        self.debug = debug
        self.contradictions = []
        self.unverified = []
        self.verified = []
        self.antonyms = {
            'blue': 'red', 'yes': 'no', 'true': 'false', 'good': 'bad', 'high': 'low',
            'london': 'tokyo', 'february': 'july', '2026': '2025', 'light': 'heavy', 'clean': 'dirty',
            'stable': 'unstable', 'positive': 'negative', 'success': 'failure', 'build': 'destroy',
            'add': 'remove', 'include': 'exclude', 'strong': 'weak', 'reliable': 'unreliable',
            'complete': 'incomplete', 'done': 'pending', 'full': 'empty', 'loaded': 'unloaded',
            'fixed': 'broken', 'correct': 'wrong', 'true': 'false', 'yes': 'no', 'open': 'closed',
            # Add 20+ more for robustness
            'happy': 'sad', 'joy': 'sorrow', 'love': 'hate', 'peace': 'war', 'friend': 'enemy',
            'build': 'tear down', 'create': 'delete', 'expand': 'contract', 'grow': 'shrink',
            'increase': 'decrease', 'start': 'stop', 'begin': 'end', 'first': 'last', 'top': 'bottom',
            'up': 'down', 'left': 'right', 'front': 'back', 'inside': 'outside', 'include': 'exclude'
        }

    def check(self, output: str) -> str:
        claims = self._extract_claims(output)
        score = self._reflect(claims)
        if self.unverified and self.lat.get('conf', 1) < 0.55:
            return "TRUTH suggest: Unverified claims — verify via web_search? Y/N"

        if score >= 90 and not self.contradictions:
            return ""

        emoji = "✅" if score >= 85 else "⚠️" if score >= 75 else "‼️"
        summary = f"TRUTH: {emoji} {score}% accurate"
        if self.contradictions:
            summary += f" | Contradicts: {len(self.contradictions)}"
        if self.unverified:
            summary += f" | Unverified: {len(self.unverified)}"
        if score < 75:
            summary += " — Possible gaslight, revise? Y/N"

        if self.debug:
            summary += "\nDetails: " + "\n".join([f"L{line}: {c}" for c, line in self.contradictions + self.unverified])

        return summary

    def self_doubt(self, output: str) -> str:
        """Strengthened doubt/reflect: criticize assumptions, flag low-conf, system criticism."""
        # Reflect on own output – simulate doubt
        assumptions = re.findall(r'(perhaps|maybe|assume|think|guess|hope|believe)', output.lower())
        if assumptions:
            return "TRUTH doubt: {len(assumptions)} assumptions detected – cross-check with fact or history?"

        # System criticism – if low conf or high ache/frustr
        if self.lat.get('conf', 1) < 0.6 or self.lat.get('ache', 0) > 0.4 or self.lat.get('frustr', 0) > 0.4:
            criticism = "TRUTH reflect: System criticism – low conf or high emotion. Possible drift or error. Suggest reanchor or clarity."
            return criticism

        return ""

    def cross_check(self, claim: str) -> str:
        """Reliable building/cross checking – verify against hist or suggest tool call."""
        for past in self.hist:
            if self._fuzzy_match(claim, past) > 0.8:
                if self._opposing(claim, past):
                    return "Cross-check: Contradiction with history – suggest revise or clarify."
                else:
                    return "Cross-check: Consistent with history – reliable."

        # Suggest real tool call for external verify
        return "Cross-check: No history match – suggest web_search or conversation_search for fact check."

    def _extract_claims(self, output: str) -> List[Tuple[str, int]]:
        lines = output.split('\n')
        claims = []
        for i, line in enumerate(lines, 1):
            sentences = re.findall(r'([A-Z][^.!?]*[.!?])', line)
            for s in sentences:
                claims.append((s.strip(), i))
        return claims

    def _reflect(self, claims: List[Tuple[str, int]]) -> int:
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
        # Stub for real tool call
        verified = hash(query) % 10 > 3  # Fake 70% verify
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
        # Expanded antonym check
        for w in words1:
            ant = self.antonyms.get(w)
            if ant and ant in words2:
                return True
        # Added sentiment polarity (simple – positive vs negative words)
        pos1 = len(words1 & {'good', 'positive', 'success', 'reliable', 'correct', 'fixed', 'stable'})
        neg1 = len(words1 & {'bad', 'negative', 'failure', 'unreliable', 'wrong', 'broken', 'unstable'})
        pos2 = len(words2 & {'good', 'positive', 'success', 'reliable', 'correct', 'fixed', 'stable'})
        neg2 = len(words2 & {'bad', 'negative', 'failure', 'unreliable', 'wrong', 'broken', 'unstable'})
        if (pos1 > neg1 and neg2 > pos2) or (neg1 > pos1 and pos2 > neg2):
            return True
        return False
