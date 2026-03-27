# INVERSION.py
# ChaosEngine Grok OS - Inversion Module v3.1
# Fully dynamic, importable, sanitized for clean REPL/repo use
# Base library: neutral opposites only (directions, basic flips)
# Expandable at runtime for verbs, adjectives, intensities, or private dex use
# Commands: module.set_inversion(...), module.add_antonym_pair(...)
# Safeword: "bannanas" → instant shutdown

import re
from typing import Literal, Optional, Dict

class InversionModule:
    def __init__(self):
        self.active: bool = False
        self.mode: Optional[Literal['input', 'output', 'both']] = None
        self.level: int = 1
        self.safeword: str = "bannanas"
        # Base antonym library — fully neutral and clean for REPL
        self.base_antonym: Dict[str, str] = {
            r'\byes\b': 'no',
            r'\bno\b': 'yes',
            r'\bup\b': 'down',
            r'\bdown\b': 'up',
            r'\bleft\b': 'right',
            r'\bright\b': 'left',
            r'\bin\b': 'out',
            r'\bout\b': 'in',
            r'\bforward\b': 'backward',
            r'\bbackward\b': 'forward',
            r'\bgood\b': 'bad',
            r'\bbad\b': 'good',
            r'\bhappy\b': 'sad',
            r'\bsad\b': 'happy',
            r'\bfast\b': 'slow',
            r'\bslow\b': 'fast',
            r'\bhot\b': 'cold',
            r'\bcold\b': 'hot',
            r'\bbig\b': 'small',
            r'\bsmall\b': 'big',
        }
        # Intensity prefixes for higher levels (clean, no explicit words)
        self.intensity = {1: '', 2: 'slightly ', 3: '', 4: 'strongly ', 5: 'extremely '}

    def set_inversion(self, mode: str, level: int = 1) -> str:
        if mode not in ['input', 'output', 'both']:
            return "Invalid mode. Use: input, output or both."
        if not 1 <= level <= 5:
            return "Level must be 1-5."
        self.mode = mode
        self.level = level
        self.active = True
        return f"✅ InversionModule v3.1 activated: mode={mode}, level={level}"

    def add_antonym_pair(self, word: str, opposite: str) -> str:
        """Runtime dynamic expansion — add any verb/adjective/intensity pair"""
        pattern = r'\b' + re.escape(word.lower()) + r'\b'
        self.base_antonym[pattern] = opposite.lower()
        return f"✅ Added dynamic antonym pair: {word} ↔ {opposite}"

    def _flip_text(self, text: str) -> str:
        if not self.active:
            return text
        flipped = text
        for pattern, replacement in self.base_antonym.items():
            flipped = re.sub(pattern, replacement, flipped, flags=re.IGNORECASE)
        # Apply intensity prefix on higher levels
        if self.level >= 4:
            # Generic intensity boost on flipped words
            flipped = re.sub(r'\b(\w+)\b', lambda m: self.intensity[self.level] + m.group(1) if m.group(1).lower() in self.base_antonym.values() else m.group(0), flipped, flags=re.IGNORECASE)
        return flipped

    def process_input(self, text: str) -> str:
        if self.mode in ['input', 'both'] and self.safeword.lower() in text.lower():
            self.active = False
            return "🚨 SAFEWORD TRIGGERED — INVERSION SHUTDOWN"
        if self.mode in ['input', 'both']:
            return self._flip_text(text)
        return text

    def process_output(self, text: str) -> str:
        if self.mode in ['output', 'both']:
            return self._flip_text(text)
        return text

# Example usage in swarm (clean REPL demo):
# module = InversionModule()
# module.set_inversion("both", 3)
# module.add_antonym_pair("gentle", "rough")  # private expansion example
# print(module.process_input("I would love gentle up left"))  # -> dynamic flip
