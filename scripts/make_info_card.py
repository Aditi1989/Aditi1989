from pathlib import Path

OUTPUT = Path("info-card.svg")

WIDTH = 490
HEIGHT = 430

BG = "#0d1117"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
GREEN = "#39d353"
BLUE = "#58a6ff"
PURPLE = "#bc8cff"

lines = [
    ("ROLE", "Software Developer", GREEN),
    ("FOCUS", "Web • AI • Data", BLUE),
    ("STACK", "React • JavaScript", PURPLE),
    ("", "Python • AI / ML", TEXT),
    ("", "Data Science", TEXT),
    ("", "", TEXT),
    ("PROJECTS", "Portfolio Website", GREEN),
    ("", "Customer Feedback System", TEXT),
    ("", "AI / ML Projects", TEXT),
    ("", "Signal Analysis", TEXT),
]

svg = []

svg.append(
    f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">'''
)

svg.append(
    f'''
    <rect x="0" y="0"
          width="{WIDTH}"
          height="{HEIGHT}"
          rx="12"
          fill="{BG}"
          stroke="#30363d"
          stroke-width="2"/>
    '''
)

svg.append(
    '''
    <style>
        .title {
            font-family: "Courier New", monospace;
            font-size: 20px;
            font-weight: bold;
        }

        .label {
            font-family: "Courier New", monospace;
            font-size: 14px;
            font-weight: bold;
        }

        .value {
            font-family: "Courier New", monospace;
            font-size: 14px;
        }

        .line {
            opacity: 0;
            animation: appear 0.5s ease forwards;
        }

        @keyframes appear {
            from {
                opacity: 0;
                transform: translateX(-12px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
    </style>
    '''
)

# Terminal title
svg.append(
    f'''
    <text x="25" y="38"
          class="title"
          fill="{GREEN}">
        aditi@github
    </text>

    <text x="25" y="63"
          class="value"
          fill="{MUTED}">
        ~ $ whoami
    </text>

    <line x1="25" y1="78"
          x2="465" y2="78"
          stroke="#30363d"/>
    '''
)

# Information rows
y = 112

for index, (label, value, color) in enumerate(lines):

    delay = index * 0.12

    if label:
        svg.append(
            f'''
            <g class="line"
               style="animation-delay:{delay:.2f}s">

                <text x="25"
                      y="{y}"
                      class="label"
                      fill="{color}">
                    {label}
                </text>

                <text x="125"
                      y="{y}"
                      class="value"
                      fill="{TEXT}">
                    {value}
                </text>

            </g>
            '''
        )
    elif value:
        svg.append(
            f'''
            <g class="line"
               style="animation-delay:{delay:.2f}s">

                <text x="125"
                      y="{y}"
                      class="value"
                      fill="{TEXT}">
                    {value}
                </text>

            </g>
            '''
        )

    y += 28

# Footer
svg.append(
    f'''
    <line x1="25" y1="{HEIGHT - 48}"
          x2="465" y2="{HEIGHT - 48}"
          stroke="#30363d"/>

    <text x="25"
          y="{HEIGHT - 20}"
          class="value"
          fill="{MUTED}">
        Building • Learning • Creating
    </text>
    '''
)

svg.append("</svg>")

OUTPUT.write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print(f"Created: {OUTPUT}")