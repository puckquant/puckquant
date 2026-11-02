# Methods

How every number on a BRAND NAME chart is computed. Link this page from posts. Add a section each time a new metric appears.

## Data source

All week 1 numbers come from the public NHL API at `api-web.nhle.com/v1` (no key). Raw responses are saved unchanged under `data/raw/` before any processing.

- Standings: `/standings/now`
- Games on a date: `/schedule/{YYYY-MM-DD}`
- Play-by-play: `/gamecenter/{gameId}/play-by-play`

## Goals for and against per game

`goals for / games played` and `goals against / games played`, straight from the standings endpoint. Shootout goals are not included in these totals by the NHL. Dashed lines on the scatter are the simple average across the 32 teams.

## Shot attempts (shot maps)

A shot attempt is any of these play-by-play events: `goal`, `shot-on-goal`, `missed-shot`, `blocked-shot`. Together they are what analysts call Corsi.

- **On net** means `goal` or `shot-on-goal`.
- **Blocked shots** are credited to the shooting team. The API lists the blocking team as the event owner, so the code switches it.
- **Coordinates** are in feet with center ice at (0, 0). The net is at about x = 89. Each shot is mirrored when needed (using the API's `homeTeamDefendingSide` for that period) so every team attacks toward the right, which lets a full game fit on one half-rink.
- Blocked shot locations are where the block happened, not where the shooter stood.
- All game strengths (even strength, power play, empty net) are included in week 1 maps.
