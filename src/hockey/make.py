"""One command per post. Pulls fresh data, builds the chart, saves the PNG.

Examples:
    python -m hockey.make standings
    python -m hockey.make shotmap --date 2026-11-01 --team TOR
    python -m hockey.make standings --sample      # offline preview, watermarked
    python -m hockey.make standings --size portrait
"""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from importlib import resources

from hockey.ingest import nhl_api
from hockey.transform.shots import shots_from_pbp, standings_table
from hockey.viz import charts, style


def _sample(name: str) -> dict:
    return json.loads(resources.files("hockey.sample_data").joinpath(name).read_text())


def make_standings(sample: bool, size: str) -> None:
    raw = _sample("standings_sample.json") if sample else nhl_api.pull_standings()
    df = standings_table(raw)
    path = style.save(charts.team_scatter(df, sample=sample, size=size), f"gf_ga_scatter_{size}")
    print(f"Saved {path}")


def make_shotmap(day: date, team: str | None, sample: bool, size: str) -> None:
    if sample:
        games = [_sample("pbp_sample.json")]
    else:
        games = nhl_api.pull_games(day)
    if not games:
        print(f"No finished games found on {day}.")
        return
    for pbp in games:
        home, away = pbp["homeTeam"]["abbrev"], pbp["awayTeam"]["abbrev"]
        if team and team not in (home, away):
            continue
        shots = shots_from_pbp(pbp)
        for t, opp in ((home, away), (away, home)):
            if team and t != team:
                continue
            post = charts.shot_map(shots, t, opp, f"{day:%b} {day.day}, {day.year}",
                                   sample=sample, size=size)
            print(f"Saved {style.save(post, f'shotmap_{t}_vs_{opp}_{size}')}")


def main() -> None:
    p = argparse.ArgumentParser(description="Build a branded chart PNG in output/charts/")
    p.add_argument("chart", choices=["standings", "shotmap"])
    p.add_argument("--date", type=date.fromisoformat,
                   default=date.today() - timedelta(days=1), help="for shotmap, YYYY-MM-DD")
    p.add_argument("--team", help="for shotmap, e.g. TOR. Default: every team that played")
    p.add_argument("--size", choices=list(style.SIZES), default="square")
    p.add_argument("--sample", action="store_true",
                   help="use bundled fake data (no internet), stamped SAMPLE DATA")
    args = p.parse_args()

    if args.chart == "standings":
        make_standings(args.sample, args.size)
    else:
        make_shotmap(args.date, args.team, args.sample, args.size)


if __name__ == "__main__":
    main()
