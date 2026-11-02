# First batch of post ideas

Ten concrete posts drawn from the plan's pillars, ordered so the first few only need what the week 1 code already does. Status uses the plan's backlog statuses: Idea, Researching, Drafting, Scheduled, Posted, Dropped.

| # | Post | Pillar | Hook (the one sentence) | Data needed | Ready with week 1 code? | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | Intro post: who you are and what the account does | Build in public | "Every chart here comes with the code that made it." Show the scatter as the example. | None | Yes | Idea |
| 1 | League scatter: goals for vs against per game | State of the league | Which teams are winning with offense, which with defense, and who is in trouble a month in. | NHL API standings | Yes: `make standings` | Idea |
| 2 | Shot map of the biggest game of the weekend | Player spotlights | One team's shots from one game: where the goals came from versus where the volume came from. | NHL API play-by-play | Yes: `make shotmap` | Idea |
| 3 | "How I built this" post on the pipeline | Build in public | Screenshot of the one command that turns last night's games into a chart, plus the repo link. | None | Yes | Idea |
| 4 | Goal differential vs points: who is over-performing | State of the league | Teams with way more points than their goal differential suggests tend to come back down. Name them. | NHL API standings (already pulled) | Small add: one new chart function | Idea |
| 5 | Shot volume vs shot location for a hot scorer | Player spotlights | Is he shooting more, or shooting from better spots? One shot map per month of the season. | Play-by-play for that player's games | Small add: filter shot map by player | Idea |
| 6 | Does a hot start predict the final standings? | Myth busting | Points after 15 games against final points for the last 15 seasons. How much does October really tell you? | NHL API historical standings | Needs a backfill script (week 3 to 4) | Idea |
| 7 | Metric explainer: what is a "shot attempt" (Corsi)? | Methods | Carousel: why counting all shot attempts predicts future goals better than counting goals. | Play-by-play for a week of games | Needs week 2 shots table | Idea |
| 8 | Records watch: this season's leaders vs record pace | Hockey history | Where today's goal and point leaders sit against the single-season record pace, updated weekly. | NHL API skater stats + record values | Small add: new endpoint + line chart | Idea |
| 9 | On this day: a milestone with context | Hockey history | Pick a record set on this date and chart how unusual it was for its era. Easy to schedule ahead. | Hockey-Reference or NHL API history | Needs history backfill | Idea |
| 10 | Shooting percentage regression watch | Myth busting | Teams or players shooting far above their usual percentage, and what happened to similar hot streaks before. | Play-by-play, a few weeks of games | Needs week 2 shots table | Idea |

## Suggested first two weeks

- **Week 1:** #0 intro, #1 league scatter, #3 how I built it.
- **Week 2:** #2 shot map (pick a Saturday game people talked about), #4 goal differential vs points, plus one more scatter update to start the "every Monday" habit.

## Caption template

> **[Finding in one sentence.]** [One sentence of caveat, e.g. "It's 14 games, so expect movement."]
>
> Data: NHL API. Code: link in bio / github.com/yourname/repo
>
> #NHL #HockeyAnalytics #[team tags if one team is the focus]

On X, put the repo link in a reply under the chart rather than in the main post.
