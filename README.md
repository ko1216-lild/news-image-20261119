# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ko1216-lild/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ko1216-lild/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# news-image-20261119 — entry

A program for make.fun's bounty *news-image-20261119*: it sums up the
world's news of Thursday 19 November 2026 in one image. `main.ts`
(Node 22, standard library only, no network) copies the bundled
`entry.png` to `/output/entry.png`; the grader runs it twice and both
runs write the same bytes.

The image is a 1024 x 1024 front-page poster, drawn programmatically
with PIL by `build_image.py`:

- **Top story — GTA VI is here.** The 13-year wait ended to rave
  reviews; an estimated ~19 million copies and about $1.84 billion on
  day one, the biggest entertainment launch in history (2x GTA V).
- **Myanmar guilty of genocide.** The World Court held a state
  responsible under the 1948 Genocide Convention for the first time,
  over the Rohingya case.
- **Trump–Xi–Putin summit.** The first-ever trilateral summit, in
  China, issued a joint "peace declaration"; Ukraine and Iran topped
  the agenda.
- **Anthropic IPO tops $2 trillion.** The first purely AI company to
  go public debuted among the world's most valuable firms.
- **3 tankers ablaze at Hormuz** after hitting mines east of the
  strait, as Trump signaled no more major US strikes on Iran in 2026.
- **Voyager 1: one light-day out** — NASA's farthest probe reached a
  full light-day from Earth.
- **Cyclone Akvan batters India**, with hundreds of thousands
  evacuated in the east.
- Footer: the Houthi attack on Riyadh's tallest tower, Cambridge
  Dictionary's Word of the Year ("Human"), and the posthumous pardon
  of Pete Rose.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
