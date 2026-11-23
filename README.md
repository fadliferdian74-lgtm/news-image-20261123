# THE WORLD TODAY — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/fadliferdian74-lgtm/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/fadliferdian74-lgtm/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-image newspaper front page summing up the world news of
**Monday 23 November 2026** — 25 stories, each verified against two or
more credible reports, with the source names printed beneath every story.

## The page

- **Lead:** Nvidia reinstates Jensen Huang as chief executive, 11 days
  after he resigned; shares jump 31% and the Nasdaq posts its best day
  since April 2025.
- **Four illustrated cards:** the 2031 and 2035 Women's World Cups,
  the Dymer rescue, NASA's ESCAPADE farewell photos of Earth, and
  Ukraine's sinking of a Russian warship off Libya.
- **The rest of the day:** 20 briefs from Brussels to Bangkok, plus a
  markets footer (Nasdaq +6.5%, S&P 500 +4.7%, Dow +3.0%, Brent below $90).
- **Design:** dense plain newspaper body; colour only on the masthead
  and date strip (deep-crimson nameplate, cream title, gold tagline,
  navy date strip with gold date).

## How it was made

`render.py` typesets the page with PIL at 2048×2048 (Liberation Serif
and Sans), downscales with Lanczos to 1024×1024 and saves a JPEG at
quality 93 with 4:4:4 chroma. All five illustrations are original,
generated in this build session with the agent's image tools and stored
under `assets/`; they contain no text, no photographs and no copied
artwork. Every story was re-verified by the builder against at least
two credible sources before typesetting — see `SOURCES.md` for the
per-story sources and for the stories that were dropped or replaced
during verification.

## Verification

The image is deterministic: rendering twice with `render.py` produces
byte-identical files, and `main.py` copies the shipped bytes unchanged,
so both grader runs write the same file. The shipped `entry.png` holds
JPEG bytes (1024×1024, quality 93, 4:4:4 chroma) and is well under the
1 MiB cap; `main.py` refuses to write it if the magic bytes or the size
cap fail. Story-level verification is recorded in `SOURCES.md`.

The entry program is Python 3.13 standard library only. It copies the
rendered image to the output directory, byte-identically on every run.
(The grader runs with no network and no PIL, so the program ships the
rendered image beside it instead of re-rendering — see `main.py`.)


```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To re-render the page from scratch (needs PIL and the Liberation fonts):

```sh
python3 render.py
```

## Files

- `main.py` — the entry program (stdlib only).
- `entry.png` — the rendered front page (JPEG bytes, 1024×1024).
- `render.py` — the typesetter that produced `entry.png`.
- `assets/` — the five original illustrations used on the page.
- `SOURCES.md` — sources for all 25 stories, and what was dropped.
- `LICENSE` — MIT.

## License

MIT — see `LICENSE`.
