#!/usr/bin/env python3
"""
ASCII Lattice Engine v∞.10.3
Unified • Modular • Grok-REPL Ready • Zero Bleed
NOW WITH: add_motif / add_palette + FULL A–Z font
Dynamic pulling handled by Architect (baked-in)
"""

from typing import Dict, List, Optional

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

    def add_motif(self, name: str, motif_lines: List[str]):
        if not motif_lines: return
        self.motifs[name] = [line for line in motif_lines]
        print(f"✅ Motif '{name}' added (width={len(motif_lines[0])})")

    def add_palette(self, name: str, chars: str):
        self.palettes[name] = chars
        print(f"✅ Palette '{name}' added")

    def get_complete_big_font(self) -> Dict[str, List[str]]:
        return {  # FULL A–Z — 10-wide, renderer-safe, pulled from archive
            "A": ["  █████╗  ", " ██╔══██╗ ", " ███████║ ", " ██╔══██║ ", " ██║  ██║ ", " ╚═╝  ╚═╝ "],
            "B": [" ██████╗  ", " ██╔══██╗ ", " ██████╔╝ ", " ██╔══██╗ ", " ██████╔╝ ", " ╚═════╝  "],
            "C": [" ██████╗  ", " ██╔════╝ ", " ██║      ", " ██║      ", " ╚██████╗ ", "  ╚═════╝ "],
            "D": [" ██████╗  ", " ██╔══██╗ ", " ██║  ██║ ", " ██║  ██║ ", " ██████╔╝ ", " ╚═════╝  "],
            "E": [" ███████╗ ", " ██╔════╝ ", " █████╗   ", " ██╔══╝   ", " ███████╗ ", " ╚══════╝ "],
            "F": [" ███████╗ ", " ██╔════╝ ", " █████╗   ", " ██╔══╝   ", " ██║      ", " ╚═╝      "],
            "G": [" ██████╗  ", " ██╔════╝ ", " ██║  ███╗", " ██║   ██║", " ╚██████╔╝", "  ╚═════╝ "],
            "H": [" ██╗  ██╗ ", " ██║  ██║ ", " ███████║ ", " ██╔══██║ ", " ██║  ██║ ", " ╚═╝  ╚═╝ "],
            "I": [" ██████╗  ", " ╚════██╗ ", "  █████╔╝ ", " ██╔═══╝  ", " ███████╗ ", " ╚══════╝ "],
            "J": ["  ██████╗ ", " ╚════██╗ ", "  █████╔╝ ", " ██╔══██╗ ", " ╚█████╔╝ ", "  ╚═════╝ "],
            "K": [" ██╗  ██╗ ", " ██║ ██╔╝ ", " █████╔╝  ", " ██╔══██╗ ", " ██║  ██║ ", " ╚═╝  ╚═╝ "],
            "L": [" ██╗      ", " ██║      ", " ██║      ", " ██║      ", " ███████╗ ", " ╚══════╝ "],
            "M": [" ██╗   ██╗", " ███╗ ███╗", " ████╔███║", " ██╔██╔██║", " ██║╚═╝██║", " ╚═╝  ╚═╝ "],
            "N": [" ██╗   ██╗", " ███╗  ██║", " ████╗ ██║", " ██╔██╗██║", " ██║╚████║", " ╚═╝ ╚═══╝"],
            "O": ["  █████╗  ", " ██╔══██╗ ", " ██║  ██║ ", " ██║  ██║ ", " ╚█████╔╝ ", "  ╚═════╝ "],
            "P": [" ██████╗  ", " ██╔══██╗ ", " ██████╔╝ ", " ██╔═══╝  ", " ██║      ", " ╚═╝      "],
            "Q": ["  █████╗  ", " ██╔══██╗ ", " ██║  ██║ ", " ██║  ██║ ", " ╚█████╔╝ ", "  ╚════╝  "],
            "R": [" ██████╗  ", " ██╔══██╗ ", " ██████╔╝ ", " ██╔══██╗ ", " ██║  ██║ ", " ╚═╝  ╚═╝ "],
            "S": ["  █████╗  ", " ██╔══██╗ ", " ╚█████╔╝ ", "  ╚═══██╗ ", " ██████╔╝ ", " ╚═════╝  "],
            "T": [" ███████╗ ", " ╚════██╗ ", "  █████╔╝ ", " ██╔═══╝  ", " ██║      ", " ╚═╝      "],
            "U": [" ██╗  ██╗ ", " ██║  ██║ ", " ██║  ██║ ", " ██║  ██║ ", " ╚█████╔╝ ", "  ╚═════╝ "],
            "V": [" ██╗  ██╗ ", " ██║  ██║ ", " ██║  ██║ ", " ╚██╗██╔╝ ", "  ╚███╔╝  ", "   ╚══╝   "],
            "W": [" ██╗   ██╗", " ██║   ██║", " ██║   ██║", " ██║   ██║", " ╚██████╔╝", "  ╚═════╝ "],
            "X": [" ██╗  ██╗ ", " ╚██╗██╔╝ ", "  ╚███╔╝  ", "  ██╔██╗  ", " ██╔╝ ██╗ ", " ╚═╝  ╚═╝ "],
            "Y": [" ██╗  ██╗ ", " ╚██╗██╔╝ ", "  ╚███╔╝  ", "   ██╔╝   ", "   ██║    ", "   ╚═╝    "],
            "Z": [" ███████╗ ", " ╚════██╗ ", "  █████╔╝ ", " ██╔═══╝  ", " ███████╗ ", " ╚══════╝ "],
            " ": ["          ", "          ", "          ", "          ", "          ", "          "],
            # Add digits/symbols on next iteration if needed
        }

class AsciiLatticeEngine:
    def __init__(self):
        self.library = AsciiLibrary()
        self.library.add_font("big", self.library.get_complete_big_font())
        self.library.add_motif("cat", ["  /_/\   ", " ( o.o ) ", "  > ^ <  "])
        self.library.add_palette("default", "@%#*+=-:. ")

    def _make_renderer_safe(self, s: str) -> str:
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
        banner = self.text(text, font_name, gap)
        if not motif_name or motif_name not in self.library.motifs:
            return banner
        banner_width = len(banner.split("\n")[0])
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
    print(engine.banner("DYNAMIC FIXED", motif_name="cat"))
