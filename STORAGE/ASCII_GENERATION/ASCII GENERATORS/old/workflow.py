# 1. SHARED LIBRARY (fonts + palettes)
class AsciiLibrary: ...


# 2. TEXT BANNER GENERATOR (what we've been using)
class TextBannerGenerator:
    def __init__(self):
        self.library = AsciiLibrary()

    def generate(self, text: str, decoration: str = None):
        # stitches big letters
        # automatically repeats & aligns decoration (cats, stars, borders)
        # returns clean multi-line string only
        ...


# 3. IMAGE ASCII GENERATOR (new)
class ImageAsciiGenerator:
    def generate(
        self,
        image_path: str = None,
        width: int = 80,
        palette: str = "standard",
        invert: bool = False,
    ):
        # handles real image files or later "generate image from description"
        # uses density palettes
        # returns clean ASCII only
        ...


# 4. HIGH-LEVEL HELPER (optional but nice)
def create_art(request: str):
    # smart router: decides text vs image based on your input
    ...
