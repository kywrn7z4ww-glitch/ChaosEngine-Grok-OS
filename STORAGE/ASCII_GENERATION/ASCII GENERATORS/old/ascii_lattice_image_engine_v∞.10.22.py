from typing import Dict, List, Optional
from PIL import Image
import numpy as np
import requests
from io import BytesIO

class AsciiLibrary:
    def __init__(self):
        self.fonts: Dict[str, Dict[str, List[str]]] = {}
        self.char_ramps: Dict[str, str] = {
            "standard": " .:-=+*#%@",
            "detailed": " .'`,:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
            "minimal": " .:-*#@",
            "blocks": " ░▒▓█"
        }

    def add_font(self, name: str, font_dict: Dict[str, List[str]], target_width: int = 6):
        fixed = {c: [line.ljust(target_width) for line in lines] for c, lines in font_dict.items()}
        self.fonts[name] = fixed
        print(f"✅ Font '{name}' loaded (width={target_width})")

class AsciiLatticeEngine:
    def __init__(self):
        self.library = AsciiLibrary()
        # Compact text font (unchanged from before)
        self.library.add_font("compact", {
            "A": [" #### ", "#    #", "######", "#    #", "#    #"],
            "B": ["##### ", "#    #", "##### ", "#    #", "##### "],
            # ... (full A-Z as in v∞.10.23 — omitted here for brevity but already loaded)
            " ": ["      ", "      ", "      ", "      ", "      "],
        })

    def _safe(self, s: str) -> str:
        return s.replace(" ", "\u00A0")

    def image_to_ascii(self, image_source: str, width: int = 120,
                       char_set: str = "standard", invert: bool = False,
                       high_contrast: bool = False) -> str:
        """MATHEMATICALLY SOUND IMAGE → ASCII (exact port of your HTML extractor)"""
        # 1. Load image (URL or local path)
        if image_source.startswith(("http://", "https://")):
            response = requests.get(image_source)
            img = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            img = Image.open(image_source).convert("RGB")

        # 2. Compute height with monospace aspect correction (0.58)
        aspect = img.height / img.width
        height = int(width * aspect * 0.58)
        if height < 20: height = 20
        if height > 300: height = 300

        # 3. Resize (crisp, no smoothing)
        img = img.resize((width, height), Image.NEAREST)

        # 4. Numpy vectorized math — exact replica of HTML canvas getImageData
        data = np.array(img)
        r, g, b = data[..., 0], data[..., 1], data[..., 2]
        brightness = 0.299 * r + 0.587 * g + 0.114 * b

        # 5. Optional high-contrast boost
        if high_contrast:
            brightness = np.where(brightness < 128, brightness * 0.6, brightness * 1.35)
            brightness = np.clip(brightness, 0, 255)

        # 6. Optional invert
        if invert:
            brightness = 255 - brightness

        # 7. Map brightness → character index (linear ramp)
        ramp = self.library.char_ramps.get(char_set, self.library.char_ramps["standard"])
        indices = (brightness / 255 * (len(ramp) - 1)).astype(int)
        ascii_array = np.array(list(ramp))[indices]

        # 8. Build final string (fixed-width, renderer-safe)
        ascii_lines = ["".join(row) for row in ascii_array]
        result = self._safe("\n".join(ascii_lines))
        return result

    # Text banner methods unchanged (adaptive_banner, etc.)
    # ... (keep your existing adaptive_banner and _render_single_banner here)

# ====================== ONE-LINE USAGE ======================
engine = AsciiLatticeEngine()

# Example: any image URL or local file
art = engine.image_to_ascii(
    "https://picsum.photos/id/1015/800/600",   # ← change to any image
    width=120,
    char_set="detailed",
    invert=False,
    high_contrast=True
)
print(art)
