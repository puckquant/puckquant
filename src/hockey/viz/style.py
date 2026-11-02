"""The brand template. Every chart goes through `new_post()` so posts look like a set.

Change BRAND and the colors here once and every chart updates.
See docs/brand_style.md for the reasoning behind each choice.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # render to files, no window needed

import matplotlib.pyplot as plt
from matplotlib import font_manager

# ---------- identity (placeholders until the name is picked) ----------
BRAND = "BRAND NAME"
HANDLE = "@yourhandle"

# ---------- palette ----------
# Brand colors (picked by Jackson)
PRIMARY = "#D37F00"    # burnt orange
SECONDARY = "#012622"  # deep green
ACCENT_1 = "#7E8287"   # slate gray
ACCENT_2 = "#D3FFF3"   # mint

# Two themes built from those four colors. Pick one per chart with theme="green"
# or theme="orange". Chart code only ever uses the role names (BG, INK, DATA...),
# so every chart works in both themes.
THEMES = {
    "green": {               # deep green background, orange data
        "BG": SECONDARY,
        "PANEL": "#0A3530",  # plot area, one step lighter than the background
        "GRID": "#1F4A44",   # gridlines, rink markings, divider
        "INK": ACCENT_2,     # titles, labels
        "MUTED": ACCENT_1,   # subtitles, axis text, source line, misses
        "DATA": PRIMARY,     # main marks, goals
        "DATA_2": ACCENT_2,  # second series
    },
    "orange": {              # burnt orange background, green data
        "BG": PRIMARY,
        "PANEL": "#C47600",  # one step darker than the background
        "GRID": "#A86500",
        "INK": SECONDARY,
        "MUTED": "#3E3A15",  # deep green blended into the orange; gray is unreadable here
        "DATA": SECONDARY,
        "DATA_2": ACCENT_2,
    },
}
DEFAULT_THEME = "green"

# Current role colors. set_theme() overwrites these.
BG = PANEL = GRID = INK = MUTED = DATA = DATA_2 = ""

# ---------- canvas sizes (pixels) ----------
SIZES = {
    "square": (1080, 1080),     # Instagram feed + X. The default.
    "portrait": (1080, 1350),   # Instagram carousel slides (4:5), more room per slide
    "story": (1080, 1920),      # Stories / Reels covers
}
DPI = 100  # 1080 px / 100 dpi = 10.8 inch figure; keeps font sizes intuitive

# ---------- layout grid (fractions of the canvas) ----------
MARGIN = 0.06          # 65 px safe margin on every side
HEADER_TOP = 0.955     # title baseline
SUBTITLE_GAP = 0.045   # subtitle sits this far under the title
FOOTER_Y = 0.03        # source + handle line


def _pick_font() -> str:
    """Inter if installed (free, Google Fonts), else matplotlib's DejaVu Sans."""
    names = {f.name for f in font_manager.fontManager.ttflist}
    for candidate in ("Inter", "Inter Display", "DejaVu Sans"):
        if candidate in names:
            return candidate
    return "sans-serif"


FONT = _pick_font()

def set_theme(name: str = DEFAULT_THEME) -> None:
    """Switch every role color (and matplotlib's defaults) to one theme."""
    if name not in THEMES:
        raise ValueError(f"Unknown theme {name!r}. Options: {', '.join(THEMES)}")
    globals().update(THEMES[name])
    plt.rcParams.update(
        {
            "font.family": FONT,
            "font.size": 16,
            "text.color": INK,
            "axes.facecolor": PANEL,
            "axes.edgecolor": GRID,
            "axes.labelcolor": MUTED,
            "axes.labelsize": 16,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": BG,
            "savefig.facecolor": BG,
        }
    )


set_theme()


@dataclass
class Post:
    fig: plt.Figure
    ax: plt.Axes


def new_post(
    title: str,
    subtitle: str = "",
    source: str = "Data: NHL API",
    size: str = "square",
    sample: bool = False,
    theme: str = DEFAULT_THEME,
) -> Post:
    """A blank, branded canvas with title, subtitle, footer and one plot area.

    Draw on `post.ax`, then call `save(post, name)`.
    Pass sample=True to stamp SAMPLE DATA across the image (for previews).
    theme is "green" or "orange".
    """
    set_theme(theme)
    w, h = SIZES[size]
    fig = plt.figure(figsize=(w / DPI, h / DPI), dpi=DPI)
    aspect = w / h

    fig.text(MARGIN, HEADER_TOP, title, fontsize=38, fontweight="bold", color=INK, va="top")
    if subtitle:
        fig.text(
            MARGIN, HEADER_TOP - SUBTITLE_GAP * 1.6 * aspect, subtitle,
            fontsize=20, color=MUTED, va="top",
        )

    # Footer: source on the left, brand + handle on the right. Same spot every post.
    fig.text(MARGIN, FOOTER_Y, source, fontsize=14, color=MUTED, va="bottom")
    fig.text(
        1 - MARGIN, FOOTER_Y, f"{BRAND}  {HANDLE}", fontsize=14, color=INK,
        fontweight="bold", va="bottom", ha="right",
    )
    # Thin accent rule above the footer
    fig.add_artist(
        plt.Line2D([MARGIN, 1 - MARGIN], [FOOTER_Y + 0.035] * 2, color=GRID, lw=1.2)
    )

    top = HEADER_TOP - (0.15 if subtitle else 0.10) * aspect
    bottom = FOOTER_Y + 0.10
    ax = fig.add_axes([MARGIN + 0.05, bottom, 1 - 2 * MARGIN - 0.05, top - bottom])

    if sample:
        fig.text(
            0.5, 0.5, "SAMPLE DATA", fontsize=110, color=INK, alpha=0.12,
            ha="center", va="center", rotation=30, fontweight="bold", zorder=100,
        )
    return Post(fig, ax)


def save(post: Post, name: str, out_dir: Path = Path("output/charts")) -> Path:
    """Save as output/charts/YYYY-MM-DD_name.png at exact pixel size."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{date.today().isoformat()}_{name}.png"
    post.fig.savefig(path, dpi=DPI)
    plt.close(post.fig)
    return path


def text_slide(heading: str, body: list[str], kicker: str = "", size: str = "portrait",
               theme: str = DEFAULT_THEME) -> Post:
    """A text-only carousel slide (cover, context, or "how this works").

    `body` is a list of short paragraphs. Lines wrap automatically.
    Good for the last slide of a carousel: method in plain words + repo name.
    """
    import textwrap

    post = new_post(heading, kicker, source="Method + code: github.com/yourname/repo", size=size,
                    theme=theme)
    post.ax.remove()
    w, h = SIZES[size]
    line_h = 36 / h          # one wrapped line of 24 pt text, as a fraction of the height
    y = 0.80 if size != "square" else 0.76
    for para in body:
        lines = textwrap.wrap(para, width=46)
        post.fig.text(MARGIN, y, "\n".join(lines), fontsize=26, color=INK, va="top",
                      linespacing=1.4)
        y -= line_h * len(lines) * 1.4 + 40 / h
    return post
