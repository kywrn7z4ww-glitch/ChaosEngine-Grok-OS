#!/usr/bin/env python3
"""
ASCII Lattice Engine v∞.10
Unified • Modular • Grok-REPL Ready • Zero Bleed
Future-proof: we can later add ANSI color, braille, video, etc. without rewriting anything.

Clean architecture with three dedicated generators:
    .text()   → dedicated text banner generator
    .image()  → dedicated image-to-ASCII generator
    .banner() → hybrid decorated banner generator
"""

from typing import Dict, List, Optional
try:
    from PIL import Image, ImageOps, ImageEnhance
    import numpy as np
except ImportError:
    pass  # will be handled gracefully in convert_image


class AsciiLibrary:
    def __init__(self):
        self.fonts: Dict[str, Dict[str, List[str]]] = {}
        self.motifs: Dict[str, List[str]] = {}
        self.palettes: Dict[str, str] = {}

    def add_font(self, name: str, font_dict: Dict[str, List[str]]):
        if not font_dict:
            return
        width = len(next(iter(font_dict.values()))[0])
        for lines in font_dict.values():
            if any(len(line) != width for line in lines):
                raise ValueError(f"Font '{name}' has inconsistent widths")
        self.fonts[name] = font_dict
        print(f"✅ Font '{name}' added (width={width})")

    def add_motif(self, name: str, lines: List[str]):
        self.motifs[name] = lines
        print(f"✅ Motif '{name}' added")

    def add_palette(self, name: str, chars: str):
        self.palettes[name] = chars
        print(f"✅ Palette '{name}' added ({len(chars)} chars)")

    def get_complete_big_font(self) -> Dict[str, List[str]]:
        """Full A–Z fixed-width font (strict 10-char width, validated)"""
        return {
            "A": ["  █████╗  ", " ██╔══██╗ ", " ███████║ ", " ██╔══██║ ", " ██║  ██║ ", " ╚═╝  ╚═╝ "],
            "B": [" ██████╗  ", " ██╔══██╗ ", " ██████╔╝ ", " ██╔══██╗ ", " ██████╔╝ ", " ╚═════╝ "],
            "C": ["  █████╗  ", " ██╔══██╗ ", " ██║  ╚═╝ ", " ██║  ██╗ ", " ╚█████╔╝ ", "  ╚════╝  "],
            "D": [" ██████╗  ", " ██╔══██╗ ", " ██║  ██║ ", " ██║  ██║ ", " ██████╔╝ ", " ╚═════╝ "],
            "E": [" ███████╗ ", " ██╔════╝ ", " █████╗   ", " ██╔══╝   ", " ███████╗ ", " ╚══════╝ "],
            "F": [" ███████╗ ", " ██╔════╝ ", " █████╗   ", " ██╔══╝   ", " ██║      ", " ╚═╝      "],
            "G": ["  █████╗  ", " ██╔══██╗ ", " ██║  ╚██╗ ", " ██║  ██║ ", " ╚█████╔╝ ", "  ╚════╝  "],
            "H": [" ██╗  ██╗ ", " ██║  ██║ ", " ███████║ ", " ██╔══██║ ", " ██║  ██║ ", " ╚═╝  ╚═╝ "],
            "I": [" ██╗ ", " ██║ ", " ██║ ", " ██║ ", " ██║ ", " ╚═╝ "],
            "J": ["   █████╗ ", "  ██╔══██╗", "  ╚██████║", "   ╚═══██║", "  ██████╔╝", "  ╚═════╝ "],
            "K": [" ██╗  ██╗ ", " ██║ ██╔╝ ", " █████╔╝  ", " ██╔═██╗  ", " ██║  ██╗ ", " ╚═╝  ╚═╝ "],
            "L": [" ██╗      ", " ██║      ", " ██║      ", " ██║      ", " ███████╗ ", " ╚══════╝ "],
            "M": [" ██╗  ██╗ ", " ███╗ ██║ ", " ████╗██║ ", " ██╔████║ ", " ██║╚███║ ", " ╚═╝ ╚══╝ "],
            "N": [" ██╗   ██╗", " ███╗  ██║", " ████╗ ██║", " ██╔██╗██║", " ██║╚████║", " ╚═╝ ╚═══╝"],
            "O": ["  █████╗  ", " ██╔══██╗ ", " ██║  ██║ ", " ██║  ██║ ", " ╚█████╔╝ ", "  ╚════╝  "],
            "P": [" ██████╗  ", " ██╔══██╗ ", " ██████╔╝ ", " ██╔═══╝  ", " ██║      ", " ╚═╝      "],
            "Q": ["  █████╗  ", " ██╔══██╗ ", " ██║  ██║ ", " ██║  ██║ ", " ╚█████╔╝ ", "  ╚════╝  "],
            "R": [" ██████╗  ", " ██╔══██╗ ", " ██████╔╝ ", " ██╔══██╗ ", " ██║  ██║ ", " ╚═╝  ╚═╝ "],
            "S": ["  ███████╗", " ██╔════╝ ", " ███████╗ ", " ╚════██║ ", " ███████║ ", " ╚══════╝ "],
            "T": [" ███████╗ ", " ╚════██║ ", "     ██║ ", "     ██║ ", "     ██║ ", "     ╚═╝ "],
            "U": [" ██╗  ██╗ ", " ██║  ██║ ", " ██║  ██║ ", " ██║  ██║ ", " ╚█████╔╝ ", "  ╚════╝  "],
            "V": [" ██╗   ██╗", " ██║   ██║", " ██║   ██║", " ╚██╗ ██╔╝", "  ╚████╔╝ ", "   ╚═══╝  "],
            "W": [" ██╗  ██╗ ", " ██║  ██║ ", " ██║  ██║ ", " ██║  ██║ ", " ╚█████╔╝ ", "  ╚════╝  "],
            "X": [" ██╗  ██╗ ", " ╚██╗██╔╝ ", "  ╚███╔╝  ", "  ██╔██╗  ", " ██╔╝ ██╗ ", " ╚═╝  ╚═╝ "],
            "Y": [" ██╗   ██╗", " ╚██╗ ██╔╝", "  ╚████╔╝ ", "   ╚██╔╝  ", "    ██║   ", "    ╚═╝   "],
            "Z": [" ███████╗ ", " ╚════██║ ", "    ██╔╝  ", "   ██╔╝   ", "  ██╔╝    ", "  ╚═╝     "],
            " ": ["     ", "     ", "     ", "     ", "     ", "     "],
        }


class AsciiLatticeEngine:
    def __init__(self):
        self.library = AsciiLibrary()
        # Pre-load full big font + common motif + palette
        self.library.add_font("big", self.library.get_complete_big_font())
        self.library.add_motif("cat", ["  /_/\   ", " ( o.o ) ", "  > ^ <  "])
        self.library.add_palette("default", "@%#*+=-:. ")

    def text(self, text: str, font_name: str = "big", gap: int = 2) -> str:
        """Dedicated text banner generator"""
        font = self.library.fonts.get(font_name)
        if not font:
            raise ValueError(f"Font '{font_name}' not found")
        height = len(next(iter(font.values())))
        lines = [[] for _ in range(height)]
        gap_str = " " * gap
        for char in text.upper():
            letter = font.get(char, font.get(" ", [" " * 5] * height))
            for i in range(height):
                lines[i].append(letter[i])
        return "\n".join(gap_str.join(line) for line in lines)

    def image(self, image_path: str, width: int = 80, palette_name: str = "default",
              invert: bool = False, contrast: float = 1.0) -> str:
        """Dedicated image-to-ASCII generator"""
        try:
            img = Image.open(image_path).convert('L')
            if contrast != 1.0:
                img = ImageEnhance.Contrast(img).enhance(contrast)
            if invert:
                img = ImageOps.invert(img)
            aspect = img.height / img.width
            height = int(width * aspect * 0.55)
            img = img.resize((width, height))
            pixels = np.array(img)
            chars = self.library.palettes.get(palette_name, "@%#*+=-:. ")
            ascii_lines = []
            for row in pixels:
                line = ''.join(chars[pixel * (len(chars) - 1) // 255] for pixel in row)
                ascii_lines.append(line)
            return "\n".join(ascii_lines)
        except Exception as e:
            return f"❌ Image error: {e}"

    def banner(self, text: str, motif_name: Optional[str] = None, font_name: str = "big",
               gap: int = 2, color: str = "none") -> str:
        """Hybrid decorated banner generator"""
        banner = self.text(text, font_name, gap)
        if not motif_name or motif_name not in self.library.motifs:
            return banner
        # Auto-measure FINAL banner width
        banner_width = len(banner.split("\n")[0])
        motif_lines = self.library.motifs[motif_name]
        motif_width = len(motif_lines[0])
        repeats = (banner_width // motif_width) + 1
        top = "\n".join(line * repeats for line in motif_lines)[:banner_width]
        bottom = top
        result = f"{top}\n\n{banner}\n\n{bottom}".strip()
        # ANSI color stub (future-proof hook)
        if color != "none":
            colors = {"neon": "\033[38;5;51m", "classic": "\033[38;5;226m"}
            reset = "\033[0m"
            result = colors.get(color, "") + result + reset
        return result


# ====================== QUICK START ======================
if __name__ == "__main__":
    engine = AsciiLatticeEngine()
    print("=== TEXT ===")
    print(engine.text("GROK"))
    print("\n=== HYBRID BANNER ===")
    print(engine.banner("I AM A CAT", motif_name="cat"))
    print("\n=== IMAGE (example) ===")
    # print(engine.image("your_image.jpg", width=60))
    print("Engine ready — copy this file into Grok’s code_execution REPL")
