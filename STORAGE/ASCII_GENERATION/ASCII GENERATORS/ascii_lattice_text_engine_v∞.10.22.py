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
        self.library.add_font("compact", { ... })  # ← full A-Z dict from before (unchanged)

    def _safe(self, s: str) -> str:
        return s.replace(" ", "\u00A0")

    def adaptive_banner(self, text: str, max_safe_width: int = 78, base_gap: int = 1) -> list:
        """v∞.10.22 — tighter math + zero-gap fallback"""
        font = self.library.fonts["compact"]
        letter_width = 6
        text_upper = text.upper()
        words = text_upper.split()

        n = len(text_upper)
        projected = n * letter_width + max(0, n - 1) * base_gap
        print(f"[MATH] Input chars={n} | Projected width={projected} | Max={max_safe_width}")

        if projected <= max_safe_width:
            return [self._render_single_banner(text_upper, base_gap)]

        if base_gap > 0:
            reduced_gap = max(0, (max_safe_width - n * letter_width) // max(1, n - 1))
            if n * letter_width + max(0, n - 1) * reduced_gap <= max_safe_width:
                return [self._render_single_banner(text_upper, reduced_gap)]

        # Ultra-long → force zero-gap + word chunks
        return self._chunk_with_zero_gap(text_upper, max_safe_width)

    def _chunk_with_zero_gap(self, text: str, max_w: int) -> list:
        words = text.split()
        chunks = []
        current = []
        current_w = 0
        for word in words:
            word_w = len(word) * 6
            if current and current_w + word_w + 6 > max_w:
                chunks.append(" ".join(current))
                current = [word]
                current_w = word_w
            else:
                current.append(word)
                current_w += word_w + 6
        if current:
            chunks.append(" ".join(current))
        return [self._render_single_banner(chunk, 0) for chunk in chunks]  # zero gap

    def _render_single_banner(self, text: str, gap: int) -> str:
        # ... (unchanged — full fixed-width renderer)
        pass  # (same as v∞.10.21)

# ONE-LINE USAGE (now even stronger)
engine = AsciiLatticeEngine()
banners = engine.adaptive_banner("paste any text here — even 500 characters")
for i, b in enumerate(banners, 1):
    print(f"--- CHUNK {i} ---")
    print(b)
