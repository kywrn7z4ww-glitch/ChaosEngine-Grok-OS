#!/usr/bin/env python3
"""
ASCII Lattice Engine v∞.10.2
Unified • Modular • Grok-REPL Ready • Zero Bleed
Future-proof: we can later add ANSI color, braille, video, etc. without rewriting anything.

FIXED: Non-breaking spaces (\u00A0) for chat-renderer survival.
ALL GLYPHS STRICT 10-CHAR + motif repeat now renderer-safe.
"""

from typing import Dict, List, Optional
try:
    from PIL import Image, ImageOps, ImageEnhance
    import numpy as np
except ImportError:
    pass

class AsciiLibrary:
    def __init__(self):
        self.fonts: Dict[str, Dict[str, List[str]]] = {}
        self.motifs: Dict[str, List[str]] = {}
        self.palettes: Dict[str, str] = {}

    def add_font(self, name: str, font_dict: Dict[str, List[str]]):
        if not font_dict: return
        target_width = 10
        fixed_font = {char: [line.ljust(target_width) for line in lines] for char, lines in font_dict.items()}
        width = len(next(iter(fixed_font.values()))[0])
        for lines in fixed_font.values():
            if any(len(line) != width for line in lines):
                raise ValueError(f"Font '{name}' still inconsistent")
        self.fonts[name] = fixed_font
        print(f"✅ Font '{name}' added (width={width} — auto-padded)")

    def get_complete_big_font(self) -> Dict[str, List[str]]:
        return {  # (same perfect 10-wide font as v∞.10.1 — omitted for brevity)
            "A": ["  █████╗  ", " ██╔══██╗ ", " ███████║ ", " ██╔══██║ ", " ██║  ██║ ", " ╚═╝  ╚═╝ "],
            # ... full A-Z exactly as before ...
            " ": ["          ", "          ", "          ", "          ", "          ", "          "],
        }  # ← paste the full dict from v∞.10.1 here if needed

    # add_motif & add_palette unchanged

class AsciiLatticeEngine:
    def __init__(self):
        self.library = AsciiLibrary()
        self.library.add_font("big", self.library.get_complete_big_font())
        self.library.add_motif("cat", ["  /_/\   ", " ( o.o ) ", "  > ^ <  "])
        self.library.add_palette("default", "@%#*+=-:. ")

    def _make_renderer_safe(self, s: str) -> str:
        """CRITICAL: replace all spaces with non-breaking space so chat renderer cannot collapse them"""
        return s.replace(" ", "\u00A0")

    def text(self, text: str, font_name: str = "big", gap: int = 2) -> str:
        font = self.library.fonts.get(font_name)
        height = len(next(iter(font.values())))
        lines = [[] for _ in range(height)]
        gap_str = " " * gap
        for char in text.upper():
            letter = font.get(char, font.get(" ", [" " * 10] * height))
            for i in range(height):
                lines[i].append(letter[i])
        banner = "\n".join(gap_str.join(line) for line in lines)
        return self._make_renderer_safe(banner)

    def banner(self, text: str, motif_name: Optional[str] = None, font_name: str = "big", gap: int = 2) -> str:
        banner = self.text(text, font_name, gap)  # already safe
        if not motif_name or motif_name not in self.library.motifs:
            return banner
        banner_width = len(banner.split("\n")[0])  # measured AFTER safe conversion
        motif_lines = self.library.motifs[motif_name]
        motif_width = len(motif_lines[0])
        repeats = (banner_width // motif_width) + 1
        top = "\n".join((line * repeats)[:banner_width] for line in motif_lines)
        top = self._make_renderer_safe(top)
        result = f"{top}\n\n{banner}\n\n{top}".strip()
        return result

# ====================== QUICK START ======================
if __name__ == "__main__":
    engine = AsciiLatticeEngine()
    print(engine.banner("I LOVE XAI", motif_name="cat"))
