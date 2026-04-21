#!/usr/bin/env python3
"""
ASCII Lattice Engine v∞.10.8
Unified • Modular • Grok-REPL Ready • Zero Bleed
PIVOT: PURE ASCII FONT (no Unicode blocks — renderer-safe)
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
        print(f"✅ Font '{name}' added (width={width} — pure ASCII)")

    def add_motif(self, name: str, motif_lines: List[str]):
        if not motif_lines: return
        self.motifs[name] = [line for line in motif_lines]
        print(f"✅ Motif '{name}' added (width={len(motif_lines[0])})")

    def get_pure_ascii_font(self) -> Dict[str, List[str]]:  # NEW — 100% safe
        return {
            "A": ["  ######  ", " #      # ", " #      # ", " ######## ", " #      # ", " #      # "],
            "B": [" #######  ", " #      # ", " #######  ", " #      # ", " #      # ", " #######  "],
            "C": ["  ######  ", " #        ", " #        ", " #        ", " #        ", "  ######  "],
            "D": [" #######  ", " #      # ", " #      # ", " #      # ", " #      # ", " #######  "],
            "E": [" ######## ", " #        ", " #######  ", " #        ", " #        ", " ######## "],
            "F": [" ######## ", " #        ", " #######  ", " #        ", " #        ", " #        "],
            "G": ["  ######  ", " #        ", " #   #### ", " #      # ", " #      # ", "  ######  "],
            "H": [" #      # ", " #      # ", " ######## ", " #      # ", " #      # ", " #      # "],
            "I": [" ######## ", "    #     ", "    #     ", "    #     ", "    #     ", " ######## "],
            "J": ["  ######  ", "     #    ", "     #    ", "     #    ", " #   #    ", "  ###     "],
            "K": [" #     #  ", " #    #   ", " ####     ", " #    #   ", " #     #  ", " #     #  "],
            "L": [" #        ", " #        ", " #        ", " #        ", " #        ", " ######## "],
            "M": [" #      # ", " ##    ## ", " # #  # # ", " #  ##  # ", " #      # ", " #      # "],
            "N": [" #      # ", " ##     # ", " # #    # ", " #  #   # ", " #   #  # ", " #    ### "],
            "O": ["  ######  ", " #      # ", " #      # ", " #      # ", " #      # ", "  ######  "],
            "P": [" #######  ", " #      # ", " #######  ", " #        ", " #        ", " #        "],
            "Q": ["  ######  ", " #      # ", " #      # ", " #   #  # ", " #    ### ", "  ######  "],
            "R": [" #######  ", " #      # ", " #######  ", " #    #   ", " #     #  ", " #      # "],
            "S": ["  ######  ", " #        ", "  ######  ", "       #  ", "       #  ", "  ######  "],
            "T": [" ######## ", "    #     ", "    #     ", "    #     ", "    #     ", "    #     "],
            "U": [" #      # ", " #      # ", " #      # ", " #      # ", " #      # ", "  ######  "],
            "V": [" #      # ", " #      # ", " #      # ", "  #    #  ", "   #  #   ", "    ##    "],
            "W": [" #      # ", " #      # ", " #  ##  # ", " # #  # # ", " ##    ## ", " #      # "],
            "X": [" #      # ", "  #    #  ", "   ####   ", "   ####   ", "  #    #  ", " #      # "],
            "Y": [" #      # ", "  #    #  ", "   ####   ", "    ##    ", "    #     ", "    #     "],
            "Z": [" ######## ", "      #   ", "     #    ", "    #     ", "   #      ", " ######## "],
            " ": ["          ", "          ", "          ", "          ", "          ", "          "],
        }

class AsciiLatticeEngine:
    def __init__(self):
        self.library = AsciiLibrary()
        self.library.add_font("pure", self.library.get_pure_ascii_font())
        self.library.add_motif("cat", ["  /_/\   ", " ( o.o ) ", "  > ^ <  "])

    def _make_renderer_safe(self, s: str) -> str:
        return s.replace(" ", "\u00A0")

    def text(self, text: str, font_name: str = "pure", gap: int = 1) -> str:
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

    def banner(self, text: str, motif_name: Optional[str] = None, font_name: str = "pure", gap: int = 1) -> str:
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
    print(engine.banner("IT WILL WORK", motif_name="cat"))
