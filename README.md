# BRAND NAME: hockey analytics you can audit

Every chart posted by **BRAND NAME** ([Instagram](https://instagram.com/yourhandle) · [X](https://x.com/yourhandle)) is built from the code in this repo, using free public NHL data. If you want to know how a number was made, the answer is here.

Built by Your Name. Week 1 of the project: data pulls from the NHL API, a branded chart template, and the first two post types (a league-wide scatter and a single-game shot map). Models, a database, and a daily automated pipeline come in the following weeks.

---

## Setup (about 10 minutes, one time)

You need Python and one helper tool called **uv**, which installs everything else. Everything is free.

1. **Install uv.** Open a terminal (Mac: Terminal app. Windows: PowerShell) and paste one line:
   - Mac or Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

   Close the terminal and open a new one so it picks up the install.

2. **Get the code.** Either `git clone https://github.com/yourname/REPO.git` or download the zip and unzip it. Then move into the folder:
   ```
   cd REPO
   ```

3. **Install the project.** This creates a private Python environment in `.venv/` and installs Python 3.12 too if you do not have it:
   ```
   uv sync
   ```

4. **Check it works without internet** (uses bundled fake data, stamped SAMPLE DATA so it never gets posted by mistake):
   ```
   uv run python -m hockey.make standings --sample
   ```
   A PNG appears in `output/charts/`. Open it.

5. **Run the tests:**
   ```
   uv run pytest
   ```

`uv run` means "run this inside the project's environment". You never need to activate anything.

## Everyday commands

| What you want | Command |
| --- | --- |
| League scatter from today's standings | `uv run python -m hockey.make standings` |
| Same chart sized for an Instagram carousel (1080 x 1350) | `uv run python -m hockey.make standings --size portrait` |
| Shot maps for every game last night | `uv run python -m hockey.make shotmap` |
| Shot map for one team on one date | `uv run python -m hockey.make shotmap --date 2026-11-01 --team TOR` |
| Just save raw standings JSON | `uv run python -m hockey.ingest.nhl_api standings` |
| Save raw play-by-play for a date and print shot counts | `uv run python -m hockey.ingest.nhl_api games --date 2026-11-01` |
| Check code style | `uv run ruff check .` |

Charts land in `output/charts/` named `YYYY-MM-DD_chartname.png`. Raw API responses land in `data/raw/` and are never overwritten, so you can re-parse old games without calling the API again.

## Before your first real post

1. Open `src/hockey/viz/style.py` and set `BRAND` and `HANDLE` at the top.
2. Search the repo for `yourname/repo` and replace it with your real GitHub path.
3. Read `docs/brand_style.md` for the visual rules and the Canva/Figma workflow.

## Layout

```
src/hockey/
  ingest/nhl_api.py      # talks to api-web.nhle.com, saves raw JSON
  transform/shots.py     # play-by-play -> tidy shots table; standings -> one row per team
  viz/style.py           # THE brand template: colors, fonts, sizes, header, footer
  viz/charts.py          # team scatter, shot map, half-rink drawing
  make.py                # one command per post
  sample_data/           # small fake files for offline testing
tests/                   # pytest; runs offline
docs/
  brand_style.md         # visual identity and how to design posts
  post_ideas.md          # first batch of post ideas
  methods.md             # how each number is computed (link this from posts)
data/raw/                # API responses (git-ignored)
output/charts/           # PNGs (git-ignored)
```

## About the data

The NHL API at `api-web.nhle.com` is public and needs no key, but it is unofficial and undocumented, so fields occasionally change. If a command suddenly fails, the raw JSON in `data/raw/` is the first place to look. The code waits between requests to stay polite. NHL team names and logos are trademarks; charts use three-letter team codes only.

## Known limitations (week 1)

- Shot coordinates for blocked shots are where the block happened, not where the shot started.
- Team labels on the scatter can overlap when two teams have nearly identical numbers. Nudge them by hand for a post if needed.
- No expected goals yet. That arrives in week 3 (MoneyPuck) and week 4 (our own model).
