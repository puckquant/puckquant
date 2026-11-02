import json
from importlib import resources

from hockey.transform.shots import shots_from_pbp, standings_table


def _sample(name):
    return json.loads(resources.files("hockey.sample_data").joinpath(name).read_text())


def test_shots_only_shot_events():
    shots = shots_from_pbp(_sample("pbp_sample.json"))
    assert len(shots) > 0
    assert set(shots["event"]) <= {"goal", "shot-on-goal", "missed-shot", "blocked-shot"}


def test_shots_all_attack_right():
    # After flipping, every attempt in the sample is in the offensive half.
    shots = shots_from_pbp(_sample("pbp_sample.json"))
    assert (shots["x"] > 0).all()


def test_blocked_shot_credited_to_shooting_team():
    pbp = _sample("pbp_sample.json")
    shots = shots_from_pbp(pbp)
    blocked = shots[shots["event"] == "blocked-shot"]
    roster = {s["playerId"]: s["teamId"] for s in pbp["rosterSpots"]}
    abbrev = {pbp["homeTeam"]["id"]: "HOM", pbp["awayTeam"]["id"]: "AWY"}
    for play in pbp["plays"]:
        if play["typeDescKey"] == "blocked-shot":
            row = blocked[blocked["event_id"] == play["eventId"]].iloc[0]
            assert row["team"] == abbrev[roster[play["details"]["shootingPlayerId"]]]


def test_standings_table_has_32_teams_and_rates():
    df = standings_table(_sample("standings_sample.json"))
    assert len(df) == 32
    assert (df["gf_per_gp"] > 0).all()
