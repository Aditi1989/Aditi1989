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

# Light gray ASCII on dark terminal background
TEXT_COLOR = "#c9d1d9"
BACKGROUND_COLOR = "#0d1117"

# -----------------------------
# Load image
# -----------------------------

if not INPUT.exists():
    raise FileNotFoundError(
        f"Could not find {INPUT}. "
        "Run prep_photo.py first."
    )

image = Image.open(INPUT).convert("L")

# Preserve approximate aspect ratio
# because terminal characters are taller
# than they are wide.
width, height = image.size

chars_height = max(
    1,
    round(
        height / width
        * CHARS_WIDE
        * 0.45
    )
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

        brightness = pixels[
            y * CHARS_WIDE + x
        ]

        # White = sparse characters
        # Black = dense characters
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

# SVG opening
svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{svg_width}" '
    f'height="{svg_height}" '
    f'viewBox="0 0 {svg_width} {svg_height}">'
)

# Dark terminal background
svg.append(
    f'<rect '
    f'x="0" '
    f'y="0" '
    f'width="100%" '
    f'height="100%" '
    f'fill="{BACKGROUND_COLOR}"/>'
)

# -----------------------------
# CSS
# -----------------------------

svg.append(
    f'''
<style>

.ascii {{
    font-family: "Courier New", monospace;
    font-size: {FONT_SIZE}px;
    fill: {TEXT_COLOR};
}}

</style>
'''
)

# -----------------------------
# Animated rows
# -----------------------------

for i, row in enumerate(rows):

    y = 8 + i * LINE_HEIGHT

    # Escape special XML characters
    safe_row = html.escape(row)

    # Each row starts slightly after
    # the previous row.
    delay = i * 0.035

    # -------------------------
    # Clip path
    # -------------------------

    svg.append(
        f'''
<clipPath id="clip{i}">
    <rect
        x="0"
        y="{y - LINE_HEIGHT}"
        width="0"
        height="{LINE_HEIGHT}">

        <animate
            attributeName="width"
            from="0"
            to="{svg_width}"
            dur="0.45s"
            begin="{delay:.3f}s"
            fill="freeze"/>

    </rect>
</clipPath>
'''
    )

    # -------------------------
    # ASCII row
    # -------------------------

    svg.append(
        f'''
<text
    x="0"
    y="{y}"
    class="ascii"
    clip-path="url(#clip{i})"
    xml:space="preserve">{safe_row}</text>
'''
    )

# Close SVG
svg.append("</svg>")

# -----------------------------
# Write SVG
# -----------------------------

OUTPUT.write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print(f"Created: {OUTPUT}")
print(
    f"Size: {CHARS_WIDE} x "
    f"{chars_height} characters"
)