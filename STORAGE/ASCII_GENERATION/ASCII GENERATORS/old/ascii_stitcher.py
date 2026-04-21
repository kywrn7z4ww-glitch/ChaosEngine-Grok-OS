#!/usr/bin/env python3
"""
Neutral ASCII Stitcher v∞.6
Pure text → ASCII banner. Zero bleed. Fonts generated on demand.
"""

class AsciiStitcher:
    def __init__(self):
        self.fonts = {}          # starts empty
        self.palettes = {}       # starts empty

    def add_font(self, name: str, font_dict: dict):
        """Generate font on demand — fully dynamic."""
        if not font_dict:
            raise ValueError("Font cannot be empty")
        # Auto-validate all letters have same width
        width = len(next(iter(font_dict.values()))[0])
        for lines in font_dict.values():
            if any(len(line) != width for line in lines):
                raise ValueError(f"Font '{name}' has inconsistent widths")
        self.fonts[name] = font_dict
        print(f"✅ Font '{name}' added (width={width})")

    def add_palette(self, name: str, chars: str):
        """Generate density palette on demand."""
        self.palettes[name] = chars
        print(f"✅ Palette '{name}' added ({len(chars)} chars)")

    def stitch_text(self, text: str, font_name: str = None, gap: str = "  ", font_dict: dict = None):
        """Pure stitch — returns ONLY the ASCII banner (no frames)."""
        # Use provided font_dict first (on-demand), otherwise lookup by name
        if font_dict:
            font = font_dict
        elif font_name and font_name in self.fonts:
            font = self.fonts[font_name]
        else:
            raise ValueError("Provide either font_name (registered) or font_dict")

        height = len(next(iter(font.values())))
        banner_lines = [[] for _ in range(height)]

        for char in text.upper():
            letter = font.get(char, font.get(' ', [' ' * 9] * height))
            for i in range(height):
                banner_lines[i].append(letter[i])

        assembled = [gap.join(line) for line in banner_lines]
        return '\n'.join(assembled)

    def convert_image(self, image_path: str, width: int = 80, palette: str = None, palette_chars: str = None,
                      invert: bool = False, contrast: float = 1.0):
        """Image → ASCII using on-demand palette (requires pillow)."""
        try:
            from PIL import Image, ImageOps, ImageEnhance
            import numpy as np
        except ImportError:
            return "❌ Install pillow first: pip install pillow"

        img = Image.open(image_path).convert('L')
        if contrast != 1.0:
            img = ImageEnhance.Contrast(img).enhance(contrast)
        if invert:
            img = ImageOps.invert(img)

        aspect = img.height / img.width
        height = int(width * aspect * 0.55)
        img = img.resize((width, height))

        pixels = np.array(img)

        # Use on-demand palette
        if palette_chars:
            chars = palette_chars
        elif palette and palette in self.palettes:
            chars = self.palettes[palette]
        else:
            chars = "@%#*+=-:. "  # fallback

        ascii_lines = []
        for row in pixels:
            line = ''.join(chars[pixel * (len(chars) - 1) // 255] for pixel in row)
            ascii_lines.append(line)

        return '\n'.join(ascii_lines)


# ====================== QUICK START EXAMPLE ======================
if __name__ == "__main__":
    engine = AsciiStitcher()

    # === 1. Generate fonts on demand (only once) ===
    big_font = {
        'G': ['  ██████╗ ', ' ██╔════╝ ', ' ██║  ███╗', ' ██║   ██║', ' ╚██████╔╝', '  ╚═════╝ '],
        'R': [' ██████╗  ', ' ██╔══██╗ ', ' ██████╔╝ ', ' ██╔══██╗ ', ' ██║  ██║ ', ' ╚═╝  ╚═╝ '],
        'O': ['  █████╗  ', ' ██╔══██╗ ', ' ██║  ██║ ', ' ██║  ██║ ', ' ╚█████╔╝ ', '  ╚════╝  '],
        'K': [' ██╗  ██╗ ', ' ██║ ██╔╝ ', ' █████╔╝  ', ' ██╔═██╗  ', ' ██║  ██╗ ', ' ╚═╝  ╚═╝ '],
        'S': ['  ███████╗', ' ██╔════╝ ', ' ███████╗ ', ' ╚════██║ ', ' ███████║ ', ' ╚══════╝ '],
        ' ': ['     ', '     ', '     ', '     ', '     ', '     '],
    }
    engine.add_font('big', big_font)

    # === 2. Use it (pure output, no bleed) ===
    print(engine.stitch_text("GROK OS", font_name='big'))
    # or even cleaner:
    # print(engine.stitch_text("YOUR TEXT HERE", font_dict=big_font))

    # For pictures:
    # print(engine.convert_image("your_image.jpg", width=80, palette_chars="@%#*+=-:. ", invert=True))
