import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.svg")

# GitHub-style contribution colors
PALETTE = [
    "#161b22",  # 0
    "#0e4429",  # 1
    "#006d32",  # 2
    "#26a641",  # 3
    "#39d353",  # 4
    "#69f0a0",  # 5
]

# Grid settings
CELL = 13
GAP = 4
STEP = CELL + GAP

LEFT = 35
TOP = 30

WIDTH = 860
HEIGHT = 205


def load_data():

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "data/contributions.json not found."
        )

    return json.loads(
        DATA_FILE.read_text(
            encoding="utf-8"
        )
    )


def level_from_count(count, maximum):

    if count <= 0:
        return 0

    if maximum <= 0:
        return 1

    ratio = count / maximum

    if ratio <= 0.20:
        return 1

    if ratio <= 0.40:
        return 2

    if ratio <= 0.60:
        return 3

    if ratio <= 0.80:
        return 4

    return 5


def main():

    data = load_data()

    days = data["days"]

    total = data["total"]
    current_streak = data["current_streak"]
    longest_streak = data["longest_streak"]

    maximum = max(
        day["count"]
        for day in days
    )

    # Convert dates into a dictionary
    day_map = {
        day["date"]: day
        for day in days
    }

    # ---------------------------------
    # SVG
    # ---------------------------------

    svg = []

    svg.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{WIDTH}"
        height="{HEIGHT}"
        viewBox="0 0 {WIDTH} {HEIGHT}">'''
    )

    # Background
    svg.append(
        f'''
        <rect
            x="0"
            y="0"
            width="{WIDTH}"
            height="{HEIGHT}"
            rx="12"
            fill="#0d1117"
        />
        '''
    )

    # Animation
    svg.append(
        '''
        <style>

        .cell {
            opacity: 0;
            transform: translateY(-8px);
            animation: appear 0.45s ease forwards;
        }

        @keyframes appear {

            from {
                opacity: 0;
                transform: translateY(-8px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }

        }

        .title {
            font-family:
                "Courier New",
                monospace;

            font-size: 15px;
            font-weight: bold;
        }

        .small {
            font-family:
                "Courier New",
                monospace;

            font-size: 11px;
        }

        </style>
        '''
    )

    # ---------------------------------
    # Title
    # ---------------------------------

    svg.append(
        '''
        <text
            x="25"
            y="20"
            class="title"
            fill="#c9d1d9">
            Aditi1989 • GitHub Contributions
        </text>
        '''
    )

    # ---------------------------------
    # Contribution grid
    # ---------------------------------

    # Only use the last ~53 weeks
    recent_days = days[-371:]

    # Find the weekday of the first day
    first_date = datetime.strptime(
        recent_days[0]["date"],
        "%Y-%m-%d"
    )

    start_weekday = (
        first_date.weekday() + 1
    ) % 7

    for index, day in enumerate(recent_days):

        position = start_weekday + index

        week = position // 7
        weekday = position % 7

        x = LEFT + week * STEP
        y = TOP + weekday * STEP

        level = level_from_count(
            day["count"],
            maximum
        )

        color = PALETTE[level]

        delay = (
            week * 0.035
            + weekday * 0.025
        )

        svg.append(
            f'''
            <rect
                class="cell"
                x="{x}"
                y="{y}"
                width="{CELL}"
                height="{CELL}"
                rx="3"
                fill="{color}"
                style="animation-delay:{delay:.3f}s"
            >
                <title>
                    {day["date"]}: {day["count"]} contributions
                </title>
            </rect>
            '''
        )

    # ---------------------------------
    # Legend
    # ---------------------------------

    legend_y = 155

    svg.append(
        f'''
        <text
            x="25"
            y="{legend_y + 12}"
            class="small"
            fill="#8b949e">
            Less
        </text>
        '''
    )

    for i, color in enumerate(PALETTE):

        x = 65 + i * 18

        svg.append(
            f'''
            <rect
                x="{x}"
                y="{legend_y}"
                width="12"
                height="12"
                rx="3"
                fill="{color}"
            />
            '''
        )

    svg.append(
        f'''
        <text
            x="180"
            y="{legend_y + 12}"
            class="small"
            fill="#8b949e">
            More
        </text>
        '''
    )

    # ---------------------------------
    # Stats
    # ---------------------------------

    svg.append(
        f'''
        <text
            x="25"
            y="195"
            class="small"
            fill="#c9d1d9">

            {total} contributions •
            current streak: {current_streak} •
            longest streak: {longest_streak}

        </text>
        '''
    )

    svg.append("</svg>")

    OUTPUT_FILE.write_text(
        "\n".join(svg),
        encoding="utf-8"
    )

    print(
        f"Created: {OUTPUT_FILE}"
    )

    print(
        f"Contributions: {total}"
    )

    print(
        f"Maximum day: {maximum}"
    )


if __name__ == "__main__":
    main()