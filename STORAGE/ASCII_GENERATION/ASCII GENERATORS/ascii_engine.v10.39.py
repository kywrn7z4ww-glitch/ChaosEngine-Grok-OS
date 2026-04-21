# GENERATOR MODULE — SIMPLE ASCII ART REFERENCEfor simple ascii art references go here → https://www.asciiart.eu/(animals, objects, borders, etc. — instant on-demand fallback when KaTeX/render components not required)



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

    # ====================== IMAGE-TO-ASCII (with new logic systems) ======================
    def image_to_ascii(self, image_source: str, width: int = 78,
                       char_set: str = "detailed", invert: bool = False,
                       high_contrast: bool = True, dither: bool = True,
                       adaptive_threshold: bool = True, directional: bool = False,
                       edges: bool = True) -> str:
        """FULLY COHERENT IMAGE → ASCII — all logic systems included"""
        # Load
        if image_source.startswith(("http://", "https://")):
            response = requests.get(image_source)
            img = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            img = Image.open(image_source).convert("RGB")

        # Resize
        aspect = img.height / img.width
        height = int(width * aspect * 0.58)
        if height < 20: height = 20
        if height > 300: height = 300
        img = img.resize((width, height), Image.NEAREST)
        data = np.array(img, dtype=float)
        brightness = 0.299 * data[..., 0] + 0.587 * data[..., 1] + 0.114 * data[..., 2]

        if high_contrast:
            brightness = np.where(brightness < 128, brightness * 0.6, brightness * 1.35)
            brightness = np.clip(brightness, 0, 255)

        # 1. Floyd-Steinberg dithering
        if dither:
            for y in range(height):
                for x in range(width):
                    old = brightness[y, x]
                    new = round(old / 255 * 9) * (255 / 9)
                    err = old - new
                    brightness[y, x] = new
                    if x + 1 < width: brightness[y, x+1] += err * 7/16
                    if y + 1 < height:
                        if x - 1 >= 0: brightness[y+1, x-1] += err * 3/16
                        brightness[y+1, x] += err * 5/16
                        if x + 1 < width: brightness[y+1, x+1] += err * 1/16

        # 2. Local Adaptive Thresholding
        if adaptive_threshold:
            local_mean = np.zeros_like(brightness)
            for y in range(height):
                for x in range(width):
                    y1, y2 = max(0, y-2), min(height, y+3)
                    x1, x2 = max(0, x-2), min(width, x+3)
                    local_mean[y, x] = brightness[y1:y2, x1:x2].mean()
            brightness = np.where(brightness > local_mean, brightness * 1.2, brightness * 0.7)
            brightness = np.clip(brightness, 0, 255)

        if invert:
            brightness = 255 - brightness

        # 3. Directional Character Mapping (gradient-based)
        if directional:
            sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
            sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
            gx = np.abs(np.convolve(brightness, sobel_x, mode='same'))
            gy = np.abs(np.convolve(brightness, sobel_y, mode='same'))
            angle = np.arctan2(gy, gx) * 180 / np.pi
            dir_chars = ["-", "\\", "|", "/", "-", "\\", "|", "/"]
            indices = (angle / 45).astype(int) % 8
            ramp = np.array(dir_chars)[indices]
        else:
            ramp = self.library.char_ramps.get(char_set, self.library.char_ramps["standard"])
            indices = (brightness / 255 * (len(ramp) - 1)).astype(int)
            ramp = np.array(list(ramp))[indices]

        # 4. Optional Sobel edge boost
        if edges and not directional:
            edge_x = np.abs(np.convolve(brightness, sobel_x, mode='same'))
            edge_y = np.abs(np.convolve(brightness, sobel_y, mode='same'))
            edges_map = np.hypot(edge_x, edge_y)
            edges_map = (edges_map > np.percentile(edges_map, 85)).astype(float) * 255
            brightness = np.maximum(brightness, edges_map)

        ascii_lines = ["".join(row) for row in ramp]
        return self._safe("\n".join(ascii_lines))

    # ====================== ALL GENERATIVE MODULES (fully expanded) ======================
    def generate_fractal(self, fractal_type: str = "sierpinski", levels: int = 5,
                         width: int = 78, max_iter: int = 30, fill_char: str = "#") -> str:
        if fractal_type == "sierpinski":
            triangle = [fill_char]
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
                         iterations: int = 5, angle: int = 25, step: int = 3,
                         width: int = 78, height: int = 40, fill_char: str = "#") -> str:
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
                    if 0 <= nx < width and 0 <= ny < height: grid[ny][nx] = fill_char
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
                                angle: int = 25, step: int = 3, width: int = 78,
                                height: int = 40, fill_char: str = "#") -> str:
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
                    if 0 <= nx < width and 0 <= ny < height: grid[ny][nx] = fill_char
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
                                    pattern: str = "random", fill_char: str = "#") -> str:
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
            chars = [" ", fill_char]
            lines = ["".join(chars[cell] for cell in row) for row in grid]
            return self._safe("\n".join(line.ljust(width) for line in lines))

    def smart_render(self, source: any, mode: str = "auto") -> str:
        if isinstance(source, str) and source.startswith(("http", "/")):
            return self.image_to_ascii(source, width=78)
        elif isinstance(source, str) and ("F" in source or "[" in source):
            return self.generate_custom_lsystem(axiom=source[:10], rules={"X":"F[+X][-X]FX", "F":"FF"}, iterations=4)
        elif isinstance(source, int) and 0 <= source <= 255:
            return self.generate_cellular_automaton(mode="1d", rule=source, width=78, generations=20)
        else:
            return self._safe("█" * 78 + "\n" + str(source)[:70].center(78) + "\n" + "█" * 78)

# ====================== ONE-LINE USAGE ======================
if __name__ == "__main__":
    engine = AsciiLatticeEngine()
    print("✅ ascii_engine.py v∞.10.39 — ALL modules restored + new logic systems added")
