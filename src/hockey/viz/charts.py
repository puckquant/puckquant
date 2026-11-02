"""The first two post templates: a league scatter and a one-game shot map."""

from __future__ import annotations

import pandas as pd
from matplotlib.patches import Arc, Circle, Rectangle

from hockey.viz import style


def team_scatter(standings: pd.DataFrame, sample: bool = False, size: str = "square"):
    """Goals for vs goals against per game, all 32 teams.

    Y axis is flipped so "good" is always top right. Dashed lines are the
    league averages, which split the chart into four labeled quadrants.
    """
    today = pd.Timestamp.today()
    as_of = f"{today:%b} {today.day}"
    post = style.new_post(
        "Who's scoring, who's stopping it",
        f"Goals for and against per game, all 32 teams, through {as_of}",
        source="Data: NHL API  |  Code: github.com/yourname/repo",
        size=size,
        sample=sample,
    )
    ax = post.ax
    df = standings
    ax.scatter(df["gf_per_gp"], df["ga_per_gp"], s=260, color=style.PRIMARY, alpha=0.95,
               edgecolor=style.BG, linewidth=1.5, zorder=3)
    for _, r in df.iterrows():
        ax.annotate(r["team"], (r["gf_per_gp"], r["ga_per_gp"]), xytext=(0, 13),
                    textcoords="offset points", ha="center", fontsize=12,
                    color=style.INK, fontweight="bold", zorder=4)

    gf_avg, ga_avg = df["gf_per_gp"].mean(), df["ga_per_gp"].mean()
    ax.axvline(gf_avg, color=style.MUTED, ls="--", lw=1)
    ax.axhline(ga_avg, color=style.MUTED, ls="--", lw=1)
    ax.invert_yaxis()

    pad_x = (df["gf_per_gp"].max() - df["gf_per_gp"].min()) * 0.12
    pad_y = (df["ga_per_gp"].max() - df["ga_per_gp"].min()) * 0.12
    ax.set_xlim(df["gf_per_gp"].min() - pad_x, df["gf_per_gp"].max() + pad_x)
    ax.set_ylim(df["ga_per_gp"].max() + pad_y, df["ga_per_gp"].min() - pad_y)

    corner = {"fontsize": 14, "color": style.MUTED, "fontstyle": "italic"}
    ax.text(0.98, 0.98, "Good at both", transform=ax.transAxes, ha="right", va="top",
            **{**corner, "color": style.INK, "fontweight": "bold"})
    ax.text(0.02, 0.98, "Defense first", transform=ax.transAxes, ha="left", va="top", **corner)
    ax.text(0.98, 0.02, "Fun to watch", transform=ax.transAxes, ha="right", va="bottom",
            **corner)
    ax.text(0.02, 0.02, "Rough start", transform=ax.transAxes, ha="left", va="bottom",
            **corner)

    ax.set_xlabel("Goals for per game  →")
    ax.set_ylabel("Goals against per game  (fewer is better)  →")
    return post


def draw_half_rink(ax) -> None:
    """Offensive half of an NHL rink in NHL API coordinates (feet, center ice at 0)."""
    c = {"color": style.GRID, "lw": 2, "fill": False}
    ax.add_patch(Rectangle((0, -42.5), 100, 85, **c))           # outline (corners squared off)
    ax.plot([25, 25], [-42.5, 42.5], color=style.ACCENT_2, lw=3, alpha=0.35)   # blue line
    ax.plot([89, 89], [-42.5, 42.5], color=style.PRIMARY, lw=2, alpha=0.6)  # goal line
    ax.add_patch(Arc((89, 0), 12, 12, theta1=90, theta2=270, color=style.PRIMARY, lw=2))  # crease
    ax.add_patch(Rectangle((89, -3), 3.3, 6, color=style.PRIMARY, lw=2, fill=False))      # net
    for y in (22, -22):                                          # faceoff circles
        ax.add_patch(Circle((69, y), 15, **c))
        ax.add_patch(Circle((69, y), 1, color=style.GRID))
    ax.add_patch(Arc((0, 0), 30, 30, theta1=-90, theta2=90, **{k: v for k, v in c.items()
                                                                if k != "fill"}))
    ax.set_xlim(-2, 102)
    ax.set_ylim(-44, 44)
    ax.set_aspect("equal")
    ax.axis("off")


def shot_map(shots: pd.DataFrame, team: str, opponent: str, game_date: str,
             sample: bool = False, size: str = "square"):
    """Every shot attempt by one team in one game. Goals are big and orange."""
    t = shots[shots["team"] == team]
    on_net = t[t["event"].isin(["shot-on-goal", "goal"])]
    goals = t[t["is_goal"]]
    post = style.new_post(
        f"{team} shot map vs {opponent}",
        f"{game_date}  |  {len(t)} attempts, {len(on_net)} on net, {len(goals)} goals",
        size=size,
        sample=sample,
    )
    ax = post.ax
    ax.set_facecolor(style.BG)
    draw_half_rink(ax)

    misses = t[~t["event"].isin(["shot-on-goal", "goal"])]
    saves = t[t["event"] == "shot-on-goal"]
    ax.scatter(misses["x"], misses["y"], s=70, facecolor="none", edgecolor=style.MUTED,
               linewidth=1.5, label="Missed or blocked", zorder=3)
    ax.scatter(saves["x"], saves["y"], s=90, color=style.ACCENT_2, alpha=0.8,
               label="Saved", zorder=4)
    ax.scatter(goals["x"], goals["y"], s=320, color=style.PRIMARY, edgecolor=style.INK,
               linewidth=2, label="Goal", zorder=5)
    leg = ax.legend(loc="lower left", bbox_to_anchor=(0, -0.08), ncol=3, frameon=False,
                    fontsize=14)
    for text in leg.get_texts():
        text.set_color(style.INK)
    return post
