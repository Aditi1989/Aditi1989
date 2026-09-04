import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "Aditi1989"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")


def fetch_contributions():

    print(f"Fetching contributions for {USERNAME}...")

    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html",
        },
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    days = []

    # Current GitHub contribution calendar
    cells = soup.select(
        "td.ContributionCalendar-day[data-date]"
    )

    print(f"Found {len(cells)} contribution days.")

    # GitHub stores the actual contribution count
    # in the tooltip associated with each cell.
    tooltips = {}

    for tooltip in soup.select("tool-tip[for]"):

        tooltip_id = tooltip.get("for")

        if tooltip_id:
            tooltips[tooltip_id] = tooltip.get_text(
                " ",
                strip=True
            )

    for cell in cells:

        date = cell.get("data-date")
        level = cell.get("data-level", "0")

        try:
            level = int(level)
        except ValueError:
            level = 0

        count = 0

        # Find tooltip associated with this cell
        cell_id = cell.get("id")

        tooltip_text = ""

        if cell_id:
            tooltip_text = tooltips.get(
                cell_id,
                ""
            )

        # Example:
        # "2 contributions on September 21st"
        match = re.search(
            r"([\d,]+)\s+contribution",
            tooltip_text,
            re.IGNORECASE
        )

        if match:

            count = int(
                match.group(1).replace(",", "")
            )

        days.append(
            {
                "date": date,
                "level": level,
                "count": count,
            }
        )

    if not days:

        raise RuntimeError(
            "No contribution days found."
        )

    # Sort chronologically
    days.sort(
        key=lambda x: x["date"]
    )

    # Total contributions
    total = sum(
        day["count"]
        for day in days
    )

    # Current streak
    current_streak = 0

    for day in reversed(days):

        if day["count"] > 0:
            current_streak += 1
        else:
            break

    # Longest streak
    longest_streak = 0
    streak = 0

    for day in days:

        if day["count"] > 0:

            streak += 1

            longest_streak = max(
                longest_streak,
                streak
            )

        else:
            streak = 0

    # Best day
    best_day = max(
        days,
        key=lambda x: x["count"]
    )

    result = {
        "username": USERNAME,
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": days,
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(
        json.dumps(
            result,
            indent=2
        ),
        encoding="utf-8"
    )

    print()
    print("SUCCESS!")
    print(f"Total contributions: {total}")
    print(f"Current streak: {current_streak}")
    print(f"Longest streak: {longest_streak}")
    print(f"Best day: {best_day['date']} ({best_day['count']} contributions)")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    fetch_contributions()