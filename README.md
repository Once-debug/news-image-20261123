# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Once-debug/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Once-debug/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

This entry prints "THE GLOBAL LEDGER", a 1024×1024 one-page broadsheet that
sums up Monday 23 November 2026's world news in a single image. The lead story
is the day's market earthquake: eleven days after resigning in scandal, Jensen
Huang was reinstated as Nvidia's chief executive after President Trump phoned
into the board meeting, and the shares leapt 31% as the Nasdaq jumped 6.5%.
Around it, six panels carry the rest of the day — COP31 ending in Antalya with
no deal at all, Ukraine sinking a Russian warship off Libya, Russian strikes
killing at least 15 around Kyiv, drone strikes on homes and a U.N. building in
Khartoum, a factory fire that killed 24 in Indonesia, and BepiColombo finally
reaching Mercury — with a closing ticker for the day's remaining headlines.
The page is typeset programmatically with Python PIL by `tools/make_image.py`;
the lead story's editorial illustration is committed at
`assets/lead-illustration.webp`, and `main.ts` verifies the finished page
against the competition gate and emits it byte-for-byte deterministically.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=6fmsan4y&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
