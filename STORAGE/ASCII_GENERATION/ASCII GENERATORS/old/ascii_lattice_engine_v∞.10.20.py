from typing import Dict, List

class AsciiLibrary:
    def __init__(self):
        self.fonts: Dict[str, Dict[str, List[str]]] = {}

    def add_font(self, name: str, font_dict: Dict[str, List[str]], target_width: int = 6):
        fixed = {c: [line.ljust(target_width) for line in lines] for c, lines in font_dict.items()}
        self.fonts[name] = fixed
        print(f"✅ Font '{name}' loaded (width={target_width})")

class AsciiLatticeEngine:
    def __init__(self):
        self.library = AsciiLibrary()
        self.library.add_font("compact", {
            "A": [" #### ", "#    #", "######", "#    #", "#    #"],
            "B": ["##### ", "#    #", "##### ", "#    #", "##### "],
            "C": [" #### ", "#     ", "#     ", "#     ", " #### "],
            "D": ["##### ", "#    #", "#    #", "#    #", "##### "],
            "E": ["######", "#     ", "##### ", "#     ", "######"],
            "F": ["######", "#     ", "##### ", "#     ", "#     "],
            "G": [" #### ", "#     ", "#  ###", "#    #", " #### "],
            "H": ["#    #", "#    #", "######", "#    #", "#    #"],
            "I": ["##### ", "  #   ", "  #   ", "  #   ", "##### "],
            "J": [" #### ", "   #  ", "   #  ", "#  #  ", " ##   "],
            "K": ["#   # ", "#  #  ", "###   ", "#  #  ", "#   # "],
            "L": ["#     ", "#     ", "#     ", "#     ", "######"],
            "M": ["#    #", "##  ##", "# ## #", "#    #", "#    #"],
            "N": ["#    #", "##   #", "# #  #", "#  # #", "#   ##"],
            "O": [" #### ", "#    #", "#    #", "#    #", " #### "],
            "P": ["##### ", "#    #", "##### ", "#     ", "#     "],
            "Q": [" #### ", "#    #", "#    #", "#  # #", " #### "],
            "R": ["##### ", "#    #", "##### ", "#  #  ", "#   # "],
            "S": [" #### ", "#     ", " #### ", "     #", " #### "],
            "T": ["######", "  #   ", "  #   ", "  #   ", "  #   "],
            "U": ["#    #", "#    #", "#    #", "#    #", " #### "],
            "V": ["#    #", "#    #", " #  # ", " #  # ", "  ##  "],
            "W": ["#    #", "#    #", "# ## #", "##  ##", "#    #"],
            "X": ["#    #", " #  # ", "  ##  ", " #  # ", "#    #"],
            "Y": ["#    #", " #  # ", "  ##  ", "  #   ", "  #   "],
            "Z": ["######", "    # ", "   #  ", "  #   ", "######"],
            " ": ["      ", "      ", "      ", "      ", "      "],
        })

    def _safe(self, s: str) -> str:
        return s.replace(" ", "\u00A0")

    def adaptive_banner(self, text: str, max_safe_width: int = 85, base_gap: int = 1) -> list:
        """MATH-DRIVEN ADAPTIVE BANNER — exactly what you asked for"""
        font = self.library.fonts["compact"]
        letter_width = 6
        height = 5
        text_upper = text.upper()
        words = text_upper.split()

        # Step 1: Calculate projected width
        n = len(text_upper)
        projected = n * letter_width + max(0, n - 1) * base_gap

        if projected <= max_safe_width:
            # Fits in one banner — use full gap
            return [self._render_single_banner(text_upper, base_gap)]

        # Step 2: Try reduced gap
        if base_gap > 0:
            reduced_gap = max(0, (max_safe_width - n * letter_width) // max(1, n - 1))
            projected_reduced = n * letter_width + max(0, n - 1) * reduced_gap
            if projected_reduced <= max_safe_width:
                return [self._render_single_banner(text_upper, reduced_gap)]

        # Step 3: Chunk into multiple banners (greedy word wrap)
        chunks = []
        current = []
        current_w = 0
        for word in words:
            word_w = len(word) * letter_width + max(0, len(word) - 1) * base_gap
            if current and current_w + word_w + letter_width > max_safe_width:  # + letter_width for space
                chunks.append(" ".join(current))
                current = [word]
                current_w = word_w
            else:
                current.append(word)
                current_w += word_w + letter_width
        if current:
            chunks.append(" ".join(current))

        return [self._render_single_banner(chunk, base_gap) for chunk in chunks]

    def _render_single_banner(self, text: str, gap: int) -> str:
        font = self.library.fonts["compact"]
        height = 5
        lines = [[] for _ in range(height)]
        gap_str = " " * gap
        for char in text:
            letter = font.get(char, font[" "])
            for i in range(height):
                lines[i].append(letter[i])
        return self._safe("\n".join(gap_str.join(row) for row in lines))

# ====================== ONE-LINE USAGE ======================
engine = AsciiLatticeEngine()
banners = engine.adaptive_banner("the quick brown fox jumps over the lazy dog")
for i, banner in enumerate(banners, 1):
    print(f"--- CHUNK {i} (math-optimized) ---")
    print(banner)
    print()
