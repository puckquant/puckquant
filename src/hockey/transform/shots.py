"""Turn raw NHL play-by-play JSON into tidy tables."""

from __future__ import annotations

import pandas as pd

SHOT_EVENTS = {"goal", "shot-on-goal", "missed-shot", "blocked-shot"}


def _name(spot: dict) -> str:
    first = spot.get("firstName", {}).get("default", "")
    last = spot.get("lastName", {}).get("default", "")
    return f"{first} {last}".strip()


def _should_flip(play: dict, team: str | None, home: str, x: float) -> bool:
    """True if this shot needs mirroring so the shooting team attacks toward +x.

    The API says which side the home team defends each period. If it is
    missing, fall back to assuming the shot came from the offensive half.
    """
    side = play.get("homeTeamDefendingSide")
    if side not in {"left", "right"}:
        return x < 0
    home_attacks_right = side == "left"
    attacks_right = home_attacks_right if team == home else not home_attacks_right
    return not attacks_right


def shots_from_pbp(pbp: dict) -> pd.DataFrame:
    """One row per shot attempt (Corsi event) in a game.

    Coordinates are flipped so every team attacks toward +x (the right side
    of the rink). That lets you draw all of a team's shots on one half-rink.
    """
    team_abbrev = {
        pbp["homeTeam"]["id"]: pbp["homeTeam"]["abbrev"],
        pbp["awayTeam"]["id"]: pbp["awayTeam"]["abbrev"],
    }
    players = {s["playerId"]: _name(s) for s in pbp.get("rosterSpots", [])}

    rows = []
    for play in pbp.get("plays", []):
        event = play.get("typeDescKey")
        if event not in SHOT_EVENTS:
            continue
        d = play.get("details", {})
        x, y = d.get("xCoord"), d.get("yCoord")
        if x is None or y is None:
            continue
        shooter_id = d.get("scoringPlayerId") or d.get("shootingPlayerId")
        team_id = d.get("eventOwnerTeamId")
        # Blocked shots are owned by the blocking team in this API, so the
        # shooter's team is the other one.
        if event == "blocked-shot":
            team_id = next((t for t in team_abbrev if t != team_id), team_id)
        flip = _should_flip(play, team_abbrev.get(team_id), pbp["homeTeam"]["abbrev"], x)
        rows.append(
            {
                "game_id": pbp["id"],
                "event_id": play.get("eventId"),
                "period": play.get("periodDescriptor", {}).get("number"),
                "time_in_period": play.get("timeInPeriod"),
                "event": event,
                "is_goal": event == "goal",
                "team": team_abbrev.get(team_id, str(team_id)),
                "shooter": players.get(shooter_id, ""),
                "shot_type": d.get("shotType"),
                "situation_code": play.get("situationCode"),
                "x": -x if flip else x,
                "y": -y if flip else y,
            }
        )
    return pd.DataFrame(rows)


def standings_table(raw: dict) -> pd.DataFrame:
    """Flatten the standings JSON into one row per team."""
    rows = []
    for t in raw.get("standings", []):
        rows.append(
            {
                "team": t["teamAbbrev"]["default"],
                "team_name": t.get("teamName", {}).get("default", ""),
                "conference": t.get("conferenceName"),
                "division": t.get("divisionName"),
                "gp": t.get("gamesPlayed"),
                "w": t.get("wins"),
                "l": t.get("losses"),
                "otl": t.get("otLosses"),
                "points": t.get("points"),
                "point_pct": t.get("pointPctg"),
                "gf": t.get("goalFor"),
                "ga": t.get("goalAgainst"),
                "goal_diff": t.get("goalDifferential"),
            }
        )
    df = pd.DataFrame(rows)
    if not df.empty:
        df["gf_per_gp"] = df["gf"] / df["gp"]
        df["ga_per_gp"] = df["ga"] / df["gp"]
    return df
