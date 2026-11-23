#!/usr/bin/env python3
"""Render the front page of THE WORLD TODAY for Monday 23 November 2026.

Build tool (run in-session with PIL). It typesets the page at 2048x2048,
downscales with Lanczos to 1024x1024 and saves a JPEG (quality 93,
4:4:4 chroma) as entry.png beside this file. The entry program (main.py)
is a stdlib-only copier: the grader sandbox has no network and no PIL,
so main.py ships the rendered image byte-identically to /output/entry.png,
exactly the pattern the kit's starter documents.

Every story below was re-verified by the builder against at least two
credible sources for 23 November 2026; see SOURCES.md for the per-story
sources and for the stories dropped or replaced during verification.
"""

import hashlib
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

W = H = 2048
MARGIN = 48
RIGHT = W - MARGIN

PAPER = (246, 241, 230)
INK = (25, 23, 19)
CRIMSON = (126, 20, 20)
CRIMSON_DARK = (104, 15, 15)
GOLD = (217, 164, 65)
GOLD_LIGHT = (232, 190, 110)
NAVY = (21, 38, 75)
GREY = (107, 101, 90)
RULE = (185, 175, 156)
CREAM = (248, 243, 231)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            if text_w(draw, cur + " " + w, f) <= width:
                cur += " " + w
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, f, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def crop_fill(path, tw, th):
    """Centre-crop an image to fill a tw x th box (no distortion)."""
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = (im.height - th) // 2
    return im.crop((x, y, x + tw, y + th))


def rule(draw, x0, x1, y, width=3, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
LEAD = {
    "kicker": "THE COMEBACK",
    "headline": "HUANG IS BACK \u2014 AND WALL STREET ROARS",
    "deck": ("Nvidia reinstates Jensen Huang as chief executive 11 days after "
             "he resigned. Shares jump 31% and the Nasdaq posts its best day "
             "since April 2025, up 6.5%."),
    "sources": "Reuters, CNN",
    "image": "media-generation-lead-nvidia-0-d8b8374f-a3ba-4bb5-876d-33c2d5ea6c75.webp",
}

CARDS = [
    {
        "kicker": "FOOTBALL",
        "headline": "WORLD CUPS: USA 2031, BRITAIN 2035",
        "body": ("FIFA confirms a four-nation 2031 finals, the first "
                 "with 48 teams."),
        "sources": "FIFA, AP",
        "image": "media-generation-card-fifa-0-a27d138e-52c0-4f8a-8397-73c8923ebb56.webp",
    },
    {
        "kicker": "UKRAINE",
        "headline": "PULLED ALIVE AFTER 22 HOURS",
        "body": ("Valentyna, 79, freed alive; Davyd, 7, survives 14 hours. "
                 "Toll: 11."),
        "sources": "Reuters, AP",
        "image": "media-generation-card-dymer-0-c32cb622-d530-4904-a449-e51745367796.webp",
    },
    {
        "kicker": "SPACE",
        "headline": "EARTH'S FAREWELL PHOTO",
        "body": ("NASA shares Earth\u2019s farewell photos as twin probes "
                 "head for Mars."),
        "sources": "NASA, Reuters",
        "image": "media-generation-card-escapade-0-2d91f848-e7ac-43e7-952d-04e217ac331a.webp",
    },
    {
        "kicker": "THE WAR AT SEA",
        "headline": "UKRAINE SINKS WARSHIP OFF LIBYA",
        "body": ("Zelenskyy says sea drones sank the corvette Merkury "
                 "at Benghazi."),
        "sources": "AP, CNN",
        "image": "media-generation-card-libya-0-4479bdc3-cd50-4dd2-8e32-46aac5da0f14.webp",
    },
]

# (headline, one-line summary, sources) -- exactly 20 briefs.
BRIEFS = [
    ("CrowdStrike to buy Zscaler for $43.9bn",
     "All-stock deal unites two cyber giants; combined revenue tops $10bn a year.",
     "Reuters, WSJ"),
    ("Puigdemont free to return to Spain",
     "Court closes the case over the 2017 referendum, six days before the election.",
     "Reuters, AFP"),
    ("India gives Nepal $1.62bn after floods",
     "Modi announces the package after talks with PM Balendra Shah in New Delhi.",
     "Reuters, AP"),
    ("Brussels strike grounds flights",
     "Air traffic halts as 50,000 march; De Wever sets a 31 Dec budget deadline.",
     "Reuters, AFP"),
    ("Merz warns Moscow over Poland missiles",
     "Chancellor calls the missiles that fell in Poland \u201cdangerous provocations\u201d.",
     "Reuters, dpa"),
    ("Russia threatens Estonia with \u201copen war\u201d",
     "Moscow warns of moves \u201con the verge of open war\u201d over border closure.",
     "Reuters, DW"),
    ("Houthis say 17 killed in Yemen strike",
     "Houthi officials say the strike on telecoms buildings in Hodeida killed 17.",
     "AFP, Reuters"),
    ("Congo halts all cobalt exports",
     "Top producer suspends all shipments from 30 Nov until further notice.",
     "Reuters, Bloomberg"),
    ("UN worker killed at Gaza water well",
     "Adel Al-Helo is killed at a water well in Jabalia; three colleagues hurt.",
     "Reuters, UNRWA"),
    ("US hits Iran\u2019s shadow banks",
     "Treasury blacklists two dozen exchange houses; FinCEN flags $15bn.",
     "Reuters, AP"),
    ("Taiwan warns of Chinese meddling",
     "Taipei warns of Chinese meddling, some of it AI-driven, before Saturday\u2019s vote.",
     "Focus Taiwan, Reuters"),
    ("Samsung breach hits 8,241 clients",
     "Files from its complaints system exposed account and licence numbers.",
     "Yonhap, Reuters"),
    ("Trump halts Iowa explosives blast",
     "Army must pause the blast of 9,500 lb of lead azide until a court agrees.",
     "Reuters, CNN"),
    ("Bomb threats hit 450 schools",
     "Hoax emailed threats reach schools in Germany and Denmark; no danger seen.",
     "Reuters, Bild"),
    ("Offshore IIT campus for Nepal",
     "India will open an offshore IIT campus, plus a start-up incubator, in Nepal.",
     "PIB, Reuters"),
    ("Brent slides below $90 a barrel",
     "Oil falls over 3% as Middle East flows recover; OPEC+ meets on 29 Nov.",
     "Reuters, Invezz"),
    ("Thai MP\u2019s jail term halved to 3 years",
     "Appeal court cuts Rukchanok Srinork\u2019s term from six years to three.",
     "Reuters, AP"),
    ("Platforms not liable for Buffalo killings",
     "Top court, 4\u20133, says platforms are not liable for the 2022 massacre.",
     "Reuters, AP"),
    ("Factory fire: 24 dead, 30 missing",
     "24 dead confirmed; about 30 still missing as rescuers search the ruins.",
     "Reuters, AP"),
    ("Iran flogs singer 74 times",
     "Parastoo Ahmadi and four of her team are lashed over a 2024 concert.",
     "Reuters, Hengaw"),
]

MARKETS = ("MARKETS \u2014 Nasdaq +6.5%  \u00b7  S&P 500 +4.7%  \u00b7  "
           "Dow +3.0%  \u00b7  Brent below $90")


def render():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---------------------------------------------------------- masthead
    d.rectangle([0, 36, W, 192], fill=CRIMSON)
    d.rectangle([0, 36, W, 42], fill=CRIMSON_DARK)
    d.rectangle([0, 186, W, 192], fill=GOLD)
    title = font(F_SERIF_B, 104)
    tw = text_w(d, "THE WORLD TODAY", title)
    d.text(((W - tw) / 2, 46), "THE WORLD TODAY", font=title, fill=CREAM)
    tag = font(F_SANS, 28)
    tg = "ALL THE NEWS OF THE WORLD \u2014 IN ONE PAGE"
    tw = text_w(d, tg, tag)
    d.text(((W - tw) / 2, 154), tg, font=tag, fill=GOLD_LIGHT)

    # --------------------------------------------------------- date strip
    d.rectangle([0, 200, W, 244], fill=NAVY)
    df = font(F_SANS_B, 28)
    d.text((MARGIN, 208), "MONDAY 23 NOVEMBER 2026", font=df, fill=GOLD)
    right = "ONE DAY  \u00b7  ONE PAGE  \u00b7  25 STORIES"
    tw = text_w(d, right, df)
    d.text((RIGHT - tw, 208), right, font=df, fill=CREAM)

    # -------------------------------------------------------------- lead
    y = 262
    kick = font(F_SANS_B, 28)
    d.text((MARGIN, y), LEAD["kicker"], font=kick, fill=CRIMSON)
    y += 40
    hf = font(F_SERIF_B, 70)
    lines = wrap(d, LEAD["headline"], hf, 1100)
    assert len(lines) <= 2, f"lead headline wraps to {len(lines)} lines"
    y = draw_lines(d, lines, MARGIN, y, hf, INK, 78)
    y += 12
    deckf = font(F_SERIF, 32)
    lines = wrap(d, LEAD["deck"], deckf, 1100)
    assert len(lines) <= 3, f"lead deck wraps to {len(lines)} lines"
    y = draw_lines(d, lines, MARGIN, y, deckf, INK, 42)
    y += 14
    srcf = font(F_SERIF_I, 24)
    d.text((MARGIN, y), "Sources: " + LEAD["sources"], font=srcf, fill=GREY)

    lead_img = crop_fill(ASSETS / LEAD["image"], 800, 380)
    page.paste(lead_img, (1200, 262))
    d.rectangle([1200, 262, 2000, 642], outline=INK, width=3)
    capf = font(F_SANS_I, 22)
    cap = "Nvidia\u2019s chip, back on its pedestal \u2014 and the market cheers."
    d.text((1200, 650), cap, font=capf, fill=GREY)

    rule(d, MARGIN, RIGHT, 668, width=3)

    # -------------------------------------------------------------- cards
    cy = 684
    cw, gap = 467, 24
    img_h = 190
    card_bottom = 0
    for i, card in enumerate(CARDS):
        x = MARGIN + i * (cw + gap)
        img = crop_fill(ASSETS / card["image"], cw, img_h)
        page.paste(img, (x, cy))
        d.rectangle([x, cy, x + cw, cy + img_h], outline=INK, width=2)
        yy = cy + img_h + 8
        kf = font(F_SANS_B, 24)
        d.text((x, yy), card["kicker"], font=kf, fill=CRIMSON)
        yy += 28
        chf = font(F_SERIF_B, 36)
        lines = wrap(d, card["headline"], chf, cw)
        assert len(lines) <= 2, f"card {i} headline wraps to {len(lines)}"
        yy = draw_lines(d, lines, x, yy, chf, INK, 38)
        yy += 4
        bf = font(F_SERIF, 25)
        lines = wrap(d, card["body"], bf, cw)
        assert len(lines) <= 2, f"card {i} body wraps to {len(lines)}"
        yy = draw_lines(d, lines, x, yy, bf, INK, 30)
        yy += 5
        sf = font(F_SERIF_I, 22)
        d.text((x, yy), "Sources: " + card["sources"], font=sf, fill=GREY)
        card_bottom = max(card_bottom, yy + 22)
    assert card_bottom <= 1090, f"cards overflow to {card_bottom}"

    rule(d, MARGIN, RIGHT, 1092, width=3)

    # ------------------------------------------------------ briefs header
    bhf = font(F_SANS_B, 30)
    d.text((MARGIN, 1104), "THE REST OF THE DAY", font=bhf, fill=CRIMSON)
    rule(d, MARGIN, RIGHT, 1148, width=2)

    # ------------------------------------------------------------- briefs
    assert len(BRIEFS) == 20, f"expected 20 briefs, got {len(BRIEFS)}"
    col_w = 952
    col_x = [MARGIN, MARGIN + col_w + 48]
    top = 1168
    bottom = 1928
    row_h = (bottom - top) // 10
    assert row_h >= 74, f"brief rows too short: {row_h}"
    hf = font(F_SANS_B, 26)
    bf = font(F_SANS, 22)
    sf = font(F_SERIF_I, 18)
    for idx, (head, summ, srcs) in enumerate(BRIEFS):
        col = idx // 10
        row = idx % 10
        x = col_x[col]
        y = top + row * row_h
        hlines = wrap(d, head, hf, col_w)
        assert len(hlines) == 1, f"brief {idx} headline wraps: {head!r}"
        d.text((x, y), hlines[0], font=hf, fill=INK)
        slines = wrap(d, summ, bf, col_w)
        assert len(slines) == 1, f"brief {idx} summary wraps: {summ!r}"
        d.text((x, y + 30), slines[0], font=bf, fill=(60, 56, 48))
        d.text((x, y + 56), "Sources: " + srcs, font=sf, fill=GREY)

    # ------------------------------------------------------------- footer
    d.rectangle([0, 1944, W, 2008], fill=NAVY)
    mf = font(F_SANS_B, 28)
    tw = text_w(d, MARKETS, mf)
    d.text(((W - tw) / 2, 1962), MARKETS, font=mf, fill=GOLD)
    ff = font(F_SANS, 20)
    foot = "THE WORLD TODAY  \u00b7  MONDAY 23 NOVEMBER 2026  \u00b7  EVERY STORY VERIFIED AGAINST TWO OR MORE REPORTS"
    tw = text_w(d, foot, ff)
    d.text(((W - tw) / 2, 2018), foot, font=ff, fill=GREY)

    # ------------------------------------------- downscale + save (JPEG)
    small = page.resize((1024, 1024), Image.LANCZOS)
    out = HERE / "entry.png"
    small.save(out, "JPEG", quality=93, subsampling=0, optimize=False)
    data = out.read_bytes()
    assert len(data) <= 1048576, f"entry too large: {len(data)} bytes"
    assert small.size == (1024, 1024)
    print(f"wrote {out}  {len(data)} bytes  "
          f"sha256={hashlib.sha256(data).hexdigest()}")
    return out


if __name__ == "__main__":
    render()
