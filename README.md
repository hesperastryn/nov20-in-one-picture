# nov20-in-one-picture

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/hesperastryn/nov20-in-one-picture/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/hesperastryn/nov20-in-one-picture/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

The world news of **Friday 20 November 2026** in one picture: a newspaper-style front page drawn entirely in code. A huge date header tops six illustrated panels — the world court's ruling that Myanmar committed genocide against the Rohingya, Trump, Xi and Putin signing a peace declaration at their first three-way summit in Shenzhen, Anthropic's $81bn IPO (the biggest debut in history) on a day US stocks fell for a fifth straight session, a Houthi missile hitting Riyadh's tallest tower, Kyiv struck again as Ukraine hit the Crimea Bridge, and Kenya discharging its last Ebola patient — with an "also today" ticker (the COP31 draft dropping fossil fuels, GTA VI sales topping $2.3bn, the UK–EU youth-mobility reset, the US cyber chief's ouster, a record $190.4m Van Gogh) along the bottom.

`generate.py` (Python + PIL) draws the image procedurally — flat vector-style panels, a courthouse with the scales of justice, three flags over a skyline, market candles against a falling index line, a tower under a missile trail, a bridged river under fire, a sunrise over the hills — and writes `entry.png` (1024×1024). The entry program `main.py` is standard-library only: it copies the committed `entry.png` to the output directory, byte-identical on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 generate.py   # redraws entry.png from scratch
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=9sbzt2n6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
