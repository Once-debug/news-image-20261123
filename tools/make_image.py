#!/usr/bin/env python3
"""Compose THE GLOBAL LEDGER — a single-page broadsheet that sums up
Monday 23 November 2026 in one 1024x1024 image.

Structure, top to bottom:
  navy utility band -> serif masthead -> red date line -> lead story
  (kicker, headline, deck, hero illustration, caption, stat chips)
  -> six story panels in a 3x2 grid -> navy closing ticker.

Every word of copy lives in this file. The hero art is the committed
editorial illustration at assets/lead-illustration.webp, centre-cropped
to its band. Output: entry.png next to this repo's root.
"""

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGE = 1024
EDGE = 40
SPAN = PAGE - 2 * EDGE            # 944 px of live column

PAPER = (247, 243, 235)
NAVY = (18, 28, 64)
NAVY_SOFT = (38, 52, 102)
INK = (24, 24, 26)
ACCENT = (176, 24, 38)
GREEN = (22, 128, 57)
MUTE = (104, 99, 90)
LINE = (52, 50, 46)
PALE = (203, 196, 182)
CHIP_BG = (233, 226, 210)

FD = "/usr/share/fonts/truetype/liberation"
SERIF = f"{FD}/LiberationSerif-Regular.ttf"
SERIF_B = f"{FD}/LiberationSerif-Bold.ttf"
SERIF_I = f"{FD}/LiberationSerif-Italic.ttf"
SANS = f"{FD}/LiberationSans-Regular.ttf"
SANS_B = f"{FD}/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def spread(draw, cx, y, text, fnt, fill, gap=2):
    """Centred text with manual letter tracking; returns its height."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + gap
    asc, desc = fnt.getmetrics()
    return asc + desc


def lines_for(draw, text, fnt, width):
    """Greedy word wrap; returns the list of lines."""
    out, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(draw, x, y, text, fnt, fill, width, leading):
    for ln in lines_for(draw, text, fnt, width):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, y, x0=EDGE, x1=PAGE - EDGE, fill=LINE, thick=2):
    draw.rectangle([x0, y, x1, y + thick - 1], fill=fill)


# ---------------------------------------------------------------- icons
# Small geometric glyphs, one per panel, drawn in a ringed disc.

def disc(draw, cx, cy, r, ring, glyph):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ring, width=3)
    glyph(cx, cy, r)


def g_ship(draw, cx, cy, r, col):
    s = r / 26
    w = max(2, int(3 * s))
    # hull
    draw.line([cx - 17 * s, cy + 3 * s, cx + 17 * s, cy + 3 * s], fill=col, width=w)
    draw.line([cx - 17 * s, cy + 3 * s, cx - 11 * s, cy + 11 * s], fill=col, width=w)
    draw.line([cx + 17 * s, cy + 3 * s, cx + 11 * s, cy + 11 * s], fill=col, width=w)
    draw.line([cx - 11 * s, cy + 11 * s, cx + 11 * s, cy + 11 * s], fill=col, width=w)
    # mast and sail
    draw.line([cx, cy + 3 * s, cx, cy - 15 * s], fill=col, width=w)
    draw.polygon([(cx + 2 * s, cy - 14 * s), (cx + 2 * s, cy + 1 * s), (cx + 12 * s, cy + 1 * s)], fill=col)
    draw.polygon([(cx - 2 * s, cy - 11 * s), (cx - 2 * s, cy + 1 * s), (cx - 10 * s, cy + 1 * s)], fill=col)
    # waves
    for dx in (-12, 2):
        draw.arc([cx + dx * s - 5 * s, cy + 12 * s, cx + dx * s + 5 * s, cy + 20 * s],
                 180, 360, fill=col, width=max(2, int(2 * s)))


def g_globe(draw, cx, cy, r, col):
    s = r / 26
    draw.ellipse([cx - 14 * s, cy - 14 * s, cx + 14 * s, cy + 14 * s], outline=col, width=max(2, int(3 * s)))
    draw.line([cx - 14 * s, cy, cx + 14 * s, cy], fill=col, width=max(2, int(2 * s)))
    draw.arc([cx - 7 * s, cy - 14 * s, cx + 7 * s, cy + 14 * s], 0, 360, fill=col, width=max(2, int(2 * s)))
    draw.line([cx - 20 * s, cy + 19 * s, cx + 20 * s, cy + 19 * s], fill=col, width=max(2, int(3 * s)))


def g_house(draw, cx, cy, r, col):
    s = r / 26
    draw.polygon([(cx - 16 * s, cy - 2 * s), (cx, cy - 16 * s), (cx + 16 * s, cy - 2 * s)], fill=col)
    draw.rectangle([cx - 12 * s, cy - 2 * s, cx + 12 * s, cy + 14 * s], outline=col, width=max(2, int(3 * s)))
    draw.rectangle([cx - 3 * s, cy + 4 * s, cx + 3 * s, cy + 14 * s], fill=col)
    draw.line([cx - 20 * s, cy - 12 * s, cx - 8 * s, cy + 2 * s], fill=col, width=max(2, int(3 * s)))


def g_building(draw, cx, cy, r, col):
    s = r / 26
    draw.rectangle([cx - 13 * s, cy - 15 * s, cx + 13 * s, cy + 15 * s], outline=col, width=max(2, int(3 * s)))
    for ry in (-9, -2, 5):
        for rx in (-7, 0, 7):
            draw.rectangle([cx + rx * s - 2 * s, cy + ry * s - 2 * s,
                            cx + rx * s + 2 * s, cy + ry * s + 2 * s], fill=col)
    draw.line([cx - 18 * s, cy + 15 * s, cx + 18 * s, cy + 15 * s], fill=col, width=max(2, int(3 * s)))


def g_factory(draw, cx, cy, r, col):
    s = r / 26
    draw.rectangle([cx - 16 * s, cy + 2 * s, cx + 16 * s, cy + 15 * s], fill=col)
    draw.polygon([(cx - 16 * s, cy + 2 * s), (cx - 4 * s, cy - 6 * s),
                  (cx - 4 * s, cy + 2 * s)], fill=col)
    draw.polygon([(cx - 4 * s, cy + 2 * s), (cx + 8 * s, cy - 6 * s),
                  (cx + 8 * s, cy + 2 * s)], fill=col)
    draw.rectangle([cx + 10 * s, cy - 14 * s, cx + 15 * s, cy + 2 * s], fill=col)
    draw.ellipse([cx + 9 * s, cy - 20 * s, cx + 16 * s, cy - 13 * s], fill=col)


def g_planet(draw, cx, cy, r, col):
    s = r / 26
    draw.ellipse([cx - 10 * s, cy - 10 * s, cx + 10 * s, cy + 10 * s], outline=col, width=max(2, int(3 * s)))
    draw.arc([cx - 20 * s, cy - 6 * s, cx + 20 * s, cy + 12 * s], 10, 170, fill=col, width=max(2, int(2 * s)))
    draw.ellipse([cx + 13 * s, cy - 17 * s, cx + 17 * s, cy - 13 * s], fill=col)
    draw.line([cx - 10 * s, cy - 2 * s, cx + 10 * s, cy - 2 * s], fill=col, width=max(2, int(2 * s)))


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)
    cx = PAGE // 2

    # utility band
    d.rectangle([0, 0, PAGE, 40], fill=NAVY)
    d.text((EDGE, 11), "ONE IMAGE · ONE DAY · ONE PAGE", font=F(SANS_B, 15), fill=(255, 255, 255))
    right = "No. 23 — MONDAY EDITION"
    d.text((PAGE - EDGE - d.textlength(right, font=F(SANS_B, 15)), 11), right,
           font=F(SANS_B, 15), fill=(255, 255, 255))

    # masthead
    spread(d, cx, 50, "THE GLOBAL LEDGER", F(SERIF_B, 56), NAVY, gap=3)
    hrule(d, 124, thick=3)
    hrule(d, 131, thick=1)

    # date line — the day, named loud and clear
    spread(d, cx, 141, "MONDAY 23 NOVEMBER 2026", F(SANS_B, 27), ACCENT, gap=2)
    hrule(d, 182, thick=1)

    # ---- lead story
    y = 192
    spread(d, cx, y, "MARKETS · THE COMEBACK", F(SANS_B, 16), NAVY_SOFT, gap=2)
    y += 26
    spread(d, cx, y, "HUANG IS BACK AT NVIDIA", F(SERIF_B, 50), INK, gap=1)
    y += 68
    deck = ("Eleven days after resigning in scandal, Jensen Huang is reinstated as chief "
            "executive after President Trump phoned into the board meeting — and Wall Street "
            "answers with one of the wildest rallies in its history.")
    for ln in lines_for(d, deck, F(SERIF_I, 20), SPAN - 60):
        w = d.textlength(ln, font=F(SERIF_I, 20))
        d.text((cx - w / 2, y), ln, font=F(SERIF_I, 20), fill=MUTE)
        y += 25
    y += 4

    # hero illustration band
    art = Image.open(os.path.join(ROOT, "assets", "lead-illustration.webp")).convert("RGB")
    band_h = 200
    scale = max(SPAN / art.width, band_h / art.height)
    art = art.resize((round(art.width * scale), round(art.height * scale)))
    ox = (art.width - SPAN) // 2
    oy = (art.height - band_h) // 2
    img.paste(art.crop((ox, oy, ox + SPAN, oy + band_h)), (EDGE, y))
    d.rectangle([EDGE, y, PAGE - EDGE, y + band_h], outline=NAVY, width=2)
    y += band_h + 8
    cap = "The chip at the centre of the AI age, and the chart that followed its king home."
    w = d.textlength(cap, font=F(SERIF_I, 15))
    d.text((cx - w / 2, y), cap, font=F(SERIF_I, 15), fill=MUTE)
    y += 22

    # stat chips
    chips = [("NVIDIA", "+31%"), ("NASDAQ", "+6.5%"), ("S&P 500", "+4.7%")]
    cw = (SPAN - 2 * 14) // 3
    for i, (label, val) in enumerate(chips):
        x0 = EDGE + i * (cw + 14)
        d.rectangle([x0, y, x0 + cw, y + 42], fill=CHIP_BG)
        d.rectangle([x0, y, x0 + cw, y + 3], fill=GREEN)
        t = f"{label}  "
        tw = d.textlength(t, font=F(SANS_B, 17)) + d.textlength(val, font=F(SANS_B, 24))
        d.text((x0 + (cw - tw) / 2, y + 11), t, font=F(SANS_B, 17), fill=INK)
        d.text((x0 + (cw - tw) / 2 + d.textlength(t, font=F(SANS_B, 17)), y + 6),
               val, font=F(SANS_B, 24), fill=GREEN)
    y += 50
    hrule(d, y, thick=2)
    y += 12

    # ---- story panels, 3 x 2
    panels = [
        ("CLIMATE · ANTALYA", "COP31 ENDS WITH NO DEAL AT ALL",
         "The longest climate summit ever closes after two days of overtime: no fossil-fuel "
         "phase-out, no agreed text, delegates sent home empty-handed.", g_globe, ACCENT),
        ("WAR AT SEA · LIBYA", "UKRAINE SINKS RUSSIAN WARSHIP",
         "Zelenskyy confirms seven naval drones sank a Russian warship in Benghazi port — "
         "the war reaches across the Mediterranean.", g_ship, NAVY),
        ("UKRAINE · KYIV REGION", "STRIKES KILL AT LEAST 15",
         "An overnight Russian bombardment flattens homes around the capital; rescuers "
         "pull a young boy alive from the rubble.", g_house, NAVY),
        ("SUDAN · KHARTOUM", "DRONES HIT HOMES AND U.N. HQ",
         "Drone strikes tear into residential blocks and a United Nations building in "
         "Sudan's battered capital.", g_building, NAVY),
        ("INDONESIA · DISASTER", "FACTORY FIRE KILLS 24 PEOPLE",
         "A blaze sweeps a sweets factory: at least 24 workers dead and some 30 still "
         "missing as search teams comb the ruins.", g_factory, ACCENT),
        ("SCIENCE · DEEP SPACE", "MERCURY, AT LAST: PROBES ARRIVE",
         "Europe and Japan's BepiColombo slips into orbit around Mercury, ending an "
         "eight-year chase across the inner solar system.", g_planet, GREEN),
    ]
    gap = 18
    pw = (SPAN - 2 * gap) // 3
    ph = 134
    for i, (tag, head, body, glyph, col) in enumerate(panels):
        x0 = EDGE + (i % 3) * (pw + gap)
        y0 = y + (i // 3) * (ph + 10)
        if i % 3:
            d.line([x0 - gap // 2, y0 + 4, x0 - gap // 2, y0 + ph - 4], fill=PALE, width=1)
        if i >= 3:
            d.line([x0, y0 - 6, x0 + pw, y0 - 6], fill=PALE, width=1)
        disc(d, x0 + 27, y0 + 27, 25, col, lambda a, b, r, g=glyph, c=col: g(d, a, b, r, c))
        tx = x0 + 62
        d.text((tx, y0 + 4), tag, font=F(SANS_B, 12), fill=col)
        hy = para(d, tx, y0 + 24, head, F(SANS_B, 16), INK, pw - 62, 20)
        para(d, x0, max(hy + 4, y0 + 60), body, F(SANS, 13), (58, 56, 52), pw, 16)
    y += 2 * ph + 10 + 8

    # ---- closing ticker
    d.rectangle([0, y, PAGE, PAGE], fill=NAVY)
    spread(d, cx, y + 10, "ALSO ON MONDAY", F(SANS_B, 14), (240, 200, 90), gap=3)
    ticker = ("CrowdStrike buys Zscaler for $43.9bn · NATO sends early-warning jets to Poland · "
              "Anthropic claims an AI proof of the Riemann hypothesis · US, Mexico, Costa Rica and "
              "Jamaica to host the 2031 Women's World Cup · Euro-area inflation rises to 4.0%")
    ty = y + 34
    for ln in lines_for(d, ticker, F(SANS, 14), SPAN - 30):
        w = d.textlength(ln, font=F(SANS, 14))
        d.text((cx - w / 2, ty), ln, font=F(SANS, 14), fill=(235, 235, 240))
        ty += 19

    out = os.path.join(ROOT, "entry.png")
    img.save(out, optimize=True)
    return out


if __name__ == "__main__":
    p = build()
    print(p, os.path.getsize(p))
