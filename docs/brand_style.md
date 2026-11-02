# Brand style guide (v1)

The goal: someone scrolling past should recognize a PuckQuant post before reading a word. That comes from doing the same few things every single time, not from fancy design.

## How to make posts: code first, Canva for words

**Charts come from code. Always.** Every chart is made by `src/hockey/viz/style.py` + a chart function. This is the whole brand promise ("analytics you can audit"), it is reproducible next week with fresh data, and it is the part that shows up on your resume. Never rebuild a chart by hand in Canva.

**Text-heavy slides can come from either place.**

| Slide type | Best tool | Why |
| --- | --- | --- |
| Any chart | Python (`hockey.make`) | Reproducible, consistent, linked to code |
| Simple text slide ("how to read this", method summary) | Python (`style.text_slide`) | Matches the charts exactly, zero extra work |
| Carousel cover with a big hook, photo, or mixed layout | Canva (free) | Faster to iterate on wording and layout by eye |
| Profile picture, highlight covers, X header banner | Canva or Figma (free) | One-time design jobs |

**Canva setup (free plan is enough, do it once):**
1. Create a 1080 x 1350 design (Instagram portrait) and a 1080 x 1080 design.
2. Set the background to `#012622`, add the footer line exactly as the charts have it (source left, brand + handle right, 14 px slate gray / mint bold), and save each as a template.
3. Add the colors below to a saved color palette (free plan allows one palette) and use Inter for all text (it is built into Canva).
4. To build a carousel: duplicate the template, drop the chart PNGs from `output/charts/` onto the chart slides, write the cover and closing slides in Canva, export as PNG.

**Figma** (free starter plan) is the better choice if you later want reusable components or pixel-precise layouts. For now Canva is quicker to learn. Pick one and stick with it.

**Free extras that fit:** Google Fonts (Inter), coolors.co for checking palette tweaks, and the Meta Business Suite preview to see crops before posting.

## Colors

| Name | Hex | Use |
| --- | --- | --- |
| Primary (burnt orange) | `#D37F00` | Main data color: dots, bars, goals, the finding |
| Secondary (deep green) | `#012622` | Background, every post |
| Accent 1 (slate gray) | `#7E8287` | Subtitles, axis labels, source line, misses and "everything else" |
| Accent 2 (mint) | `#D3FFF3` | Titles, main text, team labels, a second data series |

Two working shades are derived from the background so the plot area and gridlines read without adding new colors:

| Role | Hex | Use |
| --- | --- | --- |
| Panel | `#0A3530` | Plot area, cards |
| Grid | `#1F4A44` | Gridlines, rink markings, divider line |

### Two themes: green and orange

Every chart can be made in either theme with `--theme green` (the default) or `--theme orange`. The layout, fonts and footer stay identical, so both read as the same brand.

| Role | Green theme | Orange theme |
| --- | --- | --- |
| Background | Deep green `#012622` | Burnt orange `#D37F00` |
| Plot area | `#0A3530` | `#C47600` |
| Gridlines | `#1F4A44` | `#A86500` |
| Titles and labels | Mint `#D3FFF3` | Deep green `#012622` |
| Secondary text | Slate gray `#7E8287` | Dark olive `#3E3A15` (gray disappears on orange) |
| Main data, goals | Burnt orange | Deep green |
| Second series | Mint | Mint |

When to use which:

- **Green** is the everyday look: weekly league charts, shot maps, anything data-dense. It is easier on the eyes and lets orange carry the finding.
- **Orange** is the loud look: carousel covers, big single-number posts, milestones, "on this day" history posts, and anything you want to stop the scroll. Use it for roughly one post in four so it stays special.
- Inside one carousel, a good pattern is an orange cover, green chart slides, and an orange closing slide.
- In the orange theme, mint is only for marks (dots, shapes), never for text. Its contrast on orange is too low to read.

Rule of thumb: mint text on deep green, with orange on the data that matters. When one chart needs a highlight (one team, one player), make that one orange and push the rest to slate gray or faded mint. If everything is highlighted, nothing is.

Contrast check: mint and orange both read clearly on the deep green. Slate gray is softer (about 4:1), so keep it for text 14 pt and up and never for the main finding.

Avoid team colors as the main palette. With 32 teams, half of them clash with the brand and it stops looking like your account.

## Type

- **Font:** Inter (free, Google Fonts). Install it on your computer so matplotlib finds it; otherwise charts fall back to DejaVu Sans, which is fine but less polished.
- **Title:** 38 pt bold, sentence case, says the finding, not the topic. "Boston is winning with defense" beats "Goals for vs against."
- **Subtitle:** 20 pt muted. What the chart shows and the date range.
- **Footer:** 14 pt. Source and code link on the left, brand and handle on the right.
- Minimum text size anywhere on a chart: 12 pt. On a phone, smaller is unreadable.

## Layout grid

All sizes share the same skeleton so a carousel reads as one piece:

From top to bottom:

1. A 65 px safe margin on every side. Nothing important goes outside it.
2. Title, top left, bold.
3. Subtitle directly under it, muted.
4. The chart area fills the middle.
5. A thin divider line, then the footer: source and code link on the left, brand and handle on the right.


| Format | Size | When |
| --- | --- | --- |
| Square | 1080 x 1080 | Default. Single posts on Instagram and X. One PNG works on both. |
| Portrait | 1080 x 1350 | Instagram carousels. Takes more screen space in the feed. |
| Story | 1080 x 1920 | Stories and Reels covers. Keep text away from the top and bottom 250 px. |

## Handle and logo placement

- The brand name and handle sit bottom right on every image, in the same spot. This survives screenshots and reposts, which is how small accounts get found.
- Once you have a logo mark, put it to the left of the brand name in the footer at about 40 px tall. Do not add a big logo in the corner of the chart.
- Never put team logos on charts. Use the three-letter codes. Logos are trademarked and also make charts busy.

## Carousel recipe (Instagram)

1. **Cover:** the finding as a big title, one chart or a teaser crop. This is what stops the scroll.
2. **Chart slides:** one finding per slide, title states it.
3. **Context slide:** why it matters, the caveat (small sample, luck, etc.).
4. **Method slide:** two or three plain sentences on how it was made, plus "Code: github.com/puckquant/puckquant".

On X, post the strongest single chart with the sentence, then reply with the method and the repo link.

## Writing on the graphic

- Title = the finding. Subtitle = what and when. Footer = source.
- Say "about a third" instead of "0.3347."
- Always say how many games the numbers cover early in the season.
