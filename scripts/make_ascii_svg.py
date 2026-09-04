from pathlib import Path
from PIL import Image
import html

# -----------------------------
# Settings
# -----------------------------

INPUT = Path("source-prepped.png")
OUTPUT = Path("aditi-ascii.svg")

# Width of the ASCII portrait
CHARS_WIDE = 100

# ASCII density:
# light areas -> sparse characters
# dark areas  -> dense characters
RAMP = " .`:-=+*cs#%@"

# SVG appearance
FONT_SIZE = 8
CHAR_WIDTH = 4.8
LINE_HEIGHT = 9
TEXT_COLOR = "#c9d1d9"

# -----------------------------
# Load image
# -----------------------------

if not INPUT.exists():
    raise FileNotFoundError(
        f"Could not find {INPUT}. "
        "Run prep_photo.py first."
    )

image = Image.open(INPUT).convert("L")

# Preserve the approximate aspect ratio of characters.
# Terminal characters are taller than they are wide.
width, height = image.size

chars_height = max(
    1,
    round(height / width * CHARS_WIDE * 0.45)
)

image = image.resize(
    (CHARS_WIDE, chars_height)
)

# -----------------------------
# Convert pixels -> ASCII
# -----------------------------

pixels = list(image.getdata())

rows = []

for y in range(chars_height):
    row = []

    for x in range(CHARS_WIDE):
        brightness = pixels[y * CHARS_WIDE + x]

        # 255 = white -> first character
        # 0   = black -> last character
        index = int(
            (255 - brightness)
            / 255
            * (len(RAMP) - 1)
        )

        row.append(RAMP[index])

    rows.append("".join(row))

# -----------------------------
# Build SVG
# -----------------------------

svg_width = CHARS_WIDE * CHAR_WIDTH
svg_height = chars_height * LINE_HEIGHT + 10

svg = []

svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{svg_width}" height="{svg_height}" '
    f'viewBox="0 0 {svg_width} {svg_height}">'
)

svg.append(
    f'<rect width="100%" height="100%" fill="white"/>'
)

svg.append(
    f'<style>'
    f'.ascii {{ '
    f'font-family: "Courier New", monospace; '
    f'font-size: {FONT_SIZE}px; '
    f'fill: {TEXT_COLOR}; '
    f'}}'
    f'</style>'
)

# -----------------------------
# Animated rows
# -----------------------------

for i, row in enumerate(rows):

    y = 8 + i * LINE_HEIGHT

    # Escape special XML characters
    safe_row = html.escape(row)

    delay = i * 0.035

    # Each row appears from left to right.
    svg.append(
        f'<clipPath id="clip{i}">'
        f'<rect x="0" y="{y - LINE_HEIGHT}" '
        f'width="{svg_width}" height="{LINE_HEIGHT}">'
        f'<animate attributeName="width" '
        f'from="0" to="{svg_width}" '
        f'dur="0.45s" '
        f'begin="{delay:.3f}s" '
        f'fill="freeze"/>'
        f'</rect>'
        f'</clipPath>'
    )

    svg.append(
        f'<text x="0" y="{y}" '
        f'class="ascii" '
        f'clip-path="url(#clip{i})" '
        f'xml:space="preserve">'
        f'{safe_row}'
        f'</text>'
    )

svg.append("</svg>")

OUTPUT.write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print(f"Created: {OUTPUT}")
print(f"Size: {CHARS_WIDE} x {chars_height} characters")