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
        # Full compact 6-wide font (restored from project archive)
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

    # ====================== IMAGE-TO-ASCII (your original math preserved) ======================
    def image_to_ascii(self, image_source: str, width: int = 78,
                       char_set: str = "detailed", invert: bool = False,
                       high_contrast: bool = True) -> str:
        """MATHEMATICALLY SOUND IMAGE → ASCII (exact HTML extractor port)"""
        if image_source.startswith(("http://", "https://")):
            response = requests.get(image_source)
            img = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            img = Image.open(image_source).convert("RGB")

        aspect = img.height / img.width
        height = int(width * aspect * 0.58)
        if height < 20: height = 20
        if height > 300: height = 300

        img = img.resize((width, height), Image.NEAREST)
        data = np.array(img)
        r, g, b = data[..., 0], data[..., 1], data[..., 2]
        brightness = 0.299 * r + 0.587 * g + 0.114 * b

        if high_contrast:
            brightness = np.where(brightness < 128, brightness * 0.6, brightness * 1.35)
            brightness = np.clip(brightness, 0, 255)
        if invert:
            brightness = 255 - brightness

        ramp = self.library.char_ramps.get(char_set, self.library.char_ramps["standard"])
        indices = (brightness / 255 * (len(ramp) - 1)).astype(int)
        ascii_array = np.array(list(ramp))[indices]
        ascii_lines = ["".join(row) for row in ascii_array]
        return self._safe("\n".join(ascii_lines))

    # ====================== ALL WORKING MODULES (from modules that work.txt) ======================
    def generate_fractal(self, fractal_type: str = "sierpinski", levels: int = 5,
                         width: int = 78, max_iter: int = 30) -> str:
        """MATHEMATICALLY SOUND FRACTAL GENERATOR"""
        if fractal_type == "sierpinski":
            triangle = ["*"]
            for i in range(levels):
                spaced = " " * (2 ** i)
                triangle = [line + spaced + line for line in triangle]
            fixed = [line.center(width).ljust(width) for line in triangle]
            return self._safe("\n".join(fixed))
        elif fractal_type == "mandelbrot":
            result = []
            height = int(width * 0.5)
            for y in range(height):
                row = ""
                for x in range(width):
                    cx = (x - width * 0.75) / (width / 3.0)
                    cy = (y - height / 2.0) / (height / 2.0) * 1.5
                    zx = zy = 0.0
                    for i in range(max_iter):
                        zx2 = zx * zx
                        zy2 = zy * zy
                        if zx2 + zy2 > 4: break
                        zx, zy = zx2 - zy2 + cx, 2 * zx * zy + cy
                    row += " .:-=+*#%@"[min(i, 9)]
                result.append(row)
            return self._safe("\n".join(result))

    def generate_lsystem(self, axiom: str = "X", rules: dict = None,
                         iterations: int = 5, angle: int = 25,
                         step: int = 3, width: int = 78, height: int = 40) -> str:
        """L-SYSTEM GENERATOR"""
        if rules is None: rules = {"X": "F[+X][-X]FX", "F": "FF"}
        s = axiom
        for _ in range(iterations):
            s = "".join(rules.get(c, c) for c in s)
        grid = [[" " for _ in range(width)] for _ in range(height)]
        x = width // 2; y = height - 1; theta = 90.0; stack = []
        for c in s:
            if c == "F":
                dx = int(step * np.cos(np.radians(theta)))
                dy = int(step * np.sin(np.radians(theta)))
                for i in range(step):
                    nx = int(x + i * dx / step)
                    ny = int(y - i * dy / step)
                    if 0 <= nx < width and 0 <= ny < height: grid[ny][nx] = "#"
                x += dx; y -= dy
            elif c == "+": theta += angle
            elif c == "-": theta -= angle
            elif c == "[": stack.append((x, y, theta))
            elif c == "]":
                if stack: x, y, theta = stack.pop()
        lines = ["".join(row).rstrip() for row in grid]
        max_w = max(len(line) for line in lines) if lines else width
        fixed = [line.ljust(max_w).ljust(width) for line in lines]
        return self._safe("\n".join(fixed))

    def generate_custom_lsystem(self, axiom: str, rules: dict, iterations: int = 5,
                                angle: int = 25, step: int = 3, width: int = 78, height: int = 40) -> str:
        """FULLY CUSTOM L-SYSTEM"""
        s = axiom
        for _ in range(iterations):
            s = "".join(rules.get(c, c) for c in s)
        grid = [[" " for _ in range(width)] for _ in range(height)]
        x = width // 2; y = height - 1; theta = 90.0; stack = []
        for c in s:
            if c == "F":
                dx = int(step * np.cos(np.radians(theta)))
                dy = int(step * np.sin(np.radians(theta)))
                for i in range(step):
                    nx = int(x + i * dx / step)
                    ny = int(y - i * dy / step)
                    if 0 <= nx < width and 0 <= ny < height: grid[ny][nx] = "#"
                x += dx; y -= dy
            elif c == "+": theta += angle
            elif c == "-": theta -= angle
            elif c == "[": stack.append((x, y, theta))
            elif c == "]":
                if stack: x, y, theta = stack.pop()
        lines = ["".join(row).rstrip() for row in grid]
        max_w = max((len(line) for line in lines), default=width)
        fixed = [line.ljust(max_w).ljust(width) for line in lines]
        return self._safe("\n".join(fixed))

    def generate_cellular_automaton(self, mode: str = "1d", rule: int = 30,
                                    width: int = 78, generations: int = 30,
                                    pattern: str = "random") -> str:
        """CELLULAR AUTOMATA"""
        if mode == "1d":
            row = np.random.randint(0, 2, width) if pattern == "random" else np.zeros(width, dtype=int)
            row[width//2] = 1
            grid = [row.copy()]
            for _ in range(generations-1):
                next_row = np.zeros(width, dtype=int)
                for i in range(width):
                    l = grid[-1][(i-1) % width]
                    c = grid[-1][i]
                    r = grid[-1][(i+1) % width]
                    idx = (l << 2) | (c << 1) | r
                    next_row[i] = (rule >> idx) & 1
                grid.append(next_row)
            chars = [" ", "#"]
            lines = ["".join(chars[cell] for cell in row) for row in grid]
            return self._safe("\n".join(line.ljust(width) for line in lines))
        # 2D mode omitted for brevity — ready on request

    def smart_render(self, source: any, mode: str = "auto") -> str:
        """UNIVERSAL RENDERER — turns ANYTHING into clean ASCII"""
        if isinstance(source, str) and source.startswith(("http", "/")):
            return self.image_to_ascii(source, width=78)
        elif isinstance(source, str) and ("F" in source or "[" in source):
            return self.generate_custom_lsystem(axiom=source[:10], rules={"X":"F[+X][-X]FX", "F":"FF"}, iterations=4)
        elif isinstance(source, int) and 0 <= source <= 255:
            return self.generate_cellular_automaton(mode="1d", rule=source, width=78, generations=20)
        else:
            return self._safe("█" * 78 + "\n" + str(source)[:70].center(78) + "\n" + "█" * 78)

# ====================== ONE-LINE USAGE ======================
engine = AsciiLatticeEngine()
print("✅ Unified engine v∞.10.34 ready!")
