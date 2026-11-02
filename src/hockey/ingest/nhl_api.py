"""Pull data from the free, public NHL API (api-web.nhle.com). No key needed.

The API is unofficial and undocumented, so field names can change. Every
response is saved untouched under data/raw/ so you can re-parse later
without hitting the API again.

Examples:
    python -m hockey.ingest.nhl_api standings
    python -m hockey.ingest.nhl_api games --date 2026-11-01
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import date, timedelta
from pathlib import Path

import httpx

BASE_URL = "https://api-web.nhle.com/v1"
RAW_DIR = Path("data/raw")
USER_AGENT = "hockey-stats-starter/0.1 (personal analytics project)"


def fetch_json(path: str, save_as: Path | None = None, retries: int = 3) -> dict:
    """GET {BASE_URL}/{path} and return parsed JSON, saving a raw copy if asked."""
    url = f"{BASE_URL}/{path.lstrip('/')}"
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            resp = httpx.get(
                url, headers={"User-Agent": USER_AGENT}, timeout=30, follow_redirects=True
            )
            resp.raise_for_status()
            data = resp.json()
            break
        except (httpx.HTTPError, ValueError) as err:
            last_error = err
            time.sleep(2**attempt)  # be polite and back off: 1s, 2s, 4s
    else:
        raise RuntimeError(f"Could not fetch {url}: {last_error}")

    if save_as is not None:
        save_as.parent.mkdir(parents=True, exist_ok=True)
        save_as.write_text(json.dumps(data, indent=2))
    return data


def load_or_fetch(path: str, save_as: Path) -> dict:
    """Use the cached raw file if we already have it, otherwise fetch it."""
    if save_as.exists():
        return json.loads(save_as.read_text())
    return fetch_json(path, save_as)


# ---------- standings ----------

def pull_standings(on: date | None = None) -> dict:
    """Current standings (or standings as of a date). Always re-fetched."""
    day = (on or date.today()).isoformat()
    path = f"standings/{on.isoformat()}" if on else "standings/now"
    return fetch_json(path, RAW_DIR / "standings" / f"{day}.json")


# ---------- games ----------

def games_on(day: date) -> list[dict]:
    """Games scheduled on one date. The schedule endpoint returns a whole week."""
    data = fetch_json(f"schedule/{day.isoformat()}")
    for week_day in data.get("gameWeek", []):
        if week_day.get("date") == day.isoformat():
            return week_day.get("games", [])
    return []


def pull_play_by_play(game_id: int, day: date) -> dict:
    save_as = RAW_DIR / "pbp" / day.isoformat() / f"{game_id}.json"
    return load_or_fetch(f"gamecenter/{game_id}/play-by-play", save_as)


def pull_games(day: date) -> list[dict]:
    """Save play-by-play for every finished game on `day` and return them."""
    out = []
    for game in games_on(day):
        # Only finished games have full play-by-play. "OFF" = official, "FINAL" = final.
        if game.get("gameState") not in {"OFF", "FINAL"}:
            continue
        out.append(pull_play_by_play(game["id"], day))
        time.sleep(0.5)  # gentle on a free API
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Pull NHL API data into data/raw/")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("standings", help="save current standings")

    g = sub.add_parser("games", help="save play-by-play for one date's finished games")
    g.add_argument(
        "--date",
        type=date.fromisoformat,
        default=date.today() - timedelta(days=1),
        help="YYYY-MM-DD (default: yesterday)",
    )

    args = parser.parse_args()

    if args.command == "standings":
        data = pull_standings()
        print(f"Saved standings for {len(data.get('standings', []))} teams.")
    else:
        from hockey.transform.shots import shots_from_pbp

        games = pull_games(args.date)
        total = 0
        for pbp in games:
            shots = shots_from_pbp(pbp)
            total += len(shots)
            away, home = pbp["awayTeam"]["abbrev"], pbp["homeTeam"]["abbrev"]
            print(f"  {away} @ {home} (game {pbp['id']}): {len(shots)} shot attempts")
        print(f"{args.date}: {len(games)} finished games, {total} shot attempts saved.")


if __name__ == "__main__":
    main()
