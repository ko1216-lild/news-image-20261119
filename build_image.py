#!/usr/bin/env python3
"""Build the 'THE WORLD IN A DAY' poster for Thursday 19 November 2026.

Composes a 1024x1024 front-page / infographic poster with PIL and saves it
as entry.png next to this script. Deterministic: same input, same bytes.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/noto"
BLACK = os.path.join(FONT_DIR, "NotoSans-Black.ttf")
BOLD = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")

PAPER = (246, 241, 231)
INK = (20, 22, 26)
WHITE = (255, 255, 255)
RED = (200, 16, 46)
GOLD = (255, 196, 0)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns list of lines."""
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, s, path, start, max_w, min_size=18):
    """Shrink font until the single-line string fits max_w."""
    size = start
    while size > min_size and text_w(draw, s, font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def fit_wrap(draw, s, path, start, max_w, max_lines, min_size=20):
    """Shrink font until the wrapped text fits max_lines lines and every
    line (including single long words) fits max_w."""
    size = start
    while size > min_size:
        f = font(path, size)
        lines = wrap(draw, s, f, max_w)
        if len(lines) <= max_lines and all(text_w(draw, ln, f) <= max_w for ln in lines):
            return f, lines
        size -= 1
    f = font(path, size)
    return f, wrap(draw, s, f, max_w)


# ---------------------------------------------------------------- pictograms

def pic_scales(d, cx, cy, s, col):
    """Scales of justice."""
    d.line([cx, cy - s * 0.85, cx, cy + s * 0.75], fill=col, width=6)
    d.line([cx - s * 0.8, cy - s * 0.62, cx + s * 0.8, cy - s * 0.62], fill=col, width=6)
    d.ellipse([cx - 9, cy - s * 0.95, cx + 9, cy - s * 0.95 + 18], fill=col)
    d.line([cx - s * 0.55, cy + s * 0.85, cx + s * 0.55, cy + s * 0.85], fill=col, width=7)
    for sx in (-0.8, 0.8):
        px = cx + sx * s
        d.line([px, cy - s * 0.62, px - s * 0.26, cy + s * 0.28], fill=col, width=4)
        d.line([px, cy - s * 0.62, px + s * 0.26, cy + s * 0.28], fill=col, width=4)
        d.arc([px - s * 0.3, cy + s * 0.05, px + s * 0.3, cy + s * 0.62],
              start=0, end=180, fill=col, width=6)


def pic_globe(d, cx, cy, s, col):
    r = s * 0.88
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=6)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=col, width=4)
    d.line([cx - r, cy, cx + r, cy], fill=col, width=4)
    d.arc([cx - r, cy - r * 0.95, cx + r, cy + r * 0.35], start=0, end=180, fill=col, width=3)
    d.arc([cx - r, cy - r * 0.35, cx + r, cy + r * 0.95], start=180, end=360, fill=col, width=3)
    # three small flags on top (the three leaders' summit)
    for i, fc in enumerate([(200, 16, 46), (250, 180, 0), (40, 90, 200)]):
        fx = cx - s * 0.52 + i * s * 0.52
        fy = cy - r - 13
        d.line([fx, fy, fx, fy + 22], fill=col, width=4)
        d.polygon([(fx, fy), (fx + 20, fy + 5), (fx, fy + 11)], fill=fc)


def pic_chart(d, cx, cy, s, col):
    x0, y0 = cx - s * 0.78, cy + s * 0.78
    d.line([x0, cy - s * 0.85, x0, y0], fill=col, width=5)
    d.line([x0, y0, cx + s * 0.82, y0], fill=col, width=5)
    for bx in range(3):
        bh = s * (0.26 + bx * 0.26)
        d.rectangle([x0 + 14 + bx * s * 0.42, y0 - bh, x0 + 32 + bx * s * 0.42, y0],
                    fill=(178, 188, 198))
    pts = [(x0 + 4, y0 - s * 0.3), (cx - s * 0.28, y0 - s * 0.52),
           (cx + s * 0.02, y0 - s * 0.46), (cx + s * 0.38, y0 - s * 0.95),
           (cx + s * 0.68, cy - s * 0.78)]
    d.line(pts, fill=(26, 152, 84), width=8, joint="curve")
    ax, ay = pts[-1]
    d.polygon([(ax + 15, ay - 3), (ax - 9, ay - 7), (ax + 1, ay + 13)], fill=(26, 152, 84))


def pic_tanker(d, cx, cy, s, col):
    hull_y = cy + s * 0.3
    d.polygon([(cx - s * 0.95, hull_y), (cx + s * 0.95, hull_y),
               (cx + s * 0.7, hull_y + s * 0.42), (cx - s * 0.6, hull_y + s * 0.42)], fill=col)
    d.rectangle([cx - s * 0.8, hull_y - s * 0.22, cx + s * 0.35, hull_y], fill=col)
    d.rectangle([cx + s * 0.5, hull_y - s * 0.5, cx + s * 0.78, hull_y], fill=col)
    for i in range(4):
        wx = cx - s * 0.9 + i * s * 0.5
        d.arc([wx, hull_y + s * 0.48, wx + s * 0.4, hull_y + s * 0.76], 180, 360,
              fill=(40, 110, 190), width=5)
    fx, fy = cx - s * 0.15, hull_y - s * 0.26
    d.polygon([(fx - 24, fy), (fx, fy - s * 0.8), (fx + 9, fy - s * 0.38),
               (fx + 25, fy - s * 0.58), (fx + 27, fy)], fill=(240, 110, 20))
    d.polygon([(fx - 12, fy), (fx + 2, fy - s * 0.46), (fx + 14, fy)], fill=(255, 190, 30))


def pic_probe(d, cx, cy, s, col):
    for (sx, sy, r) in [(-0.85, -0.8, 4), (-0.4, -0.95, 3), (0.75, -0.7, 4),
                        (0.95, 0.1, 3), (-0.95, 0.25, 3), (0.45, 0.85, 3)]:
        x, y = cx + sx * s, cy + sy * s
        d.polygon([(x, y - r * 2), (x + r, y), (x, y + r * 2), (x - r, y)], fill=(250, 190, 40))
    d.arc([cx - s * 0.62, cy - s * 0.75, cx + s * 0.28, cy + s * 0.15], 300, 130, fill=col, width=8)
    d.line([cx - s * 0.18, cy - s * 0.3, cx + s * 0.3, cy + s * 0.18], fill=col, width=6)
    d.rectangle([cx + s * 0.22, cy + s * 0.1, cx + s * 0.52, cy + s * 0.42], fill=col)
    d.line([cx + s * 0.5, cy + s * 0.25, cx + s * 0.95, cy - s * 0.45], fill=col, width=6)
    d.ellipse([cx + s * 0.82, cy - s * 0.6, cx + s * 1.02, cy - s * 0.4], fill=col)
    for rr in (0.35, 0.55, 0.75):
        d.arc([cx - s * (0.18 + rr), cy - s * (0.3 + rr), cx - s * (0.18 - rr), cy - s * (0.3 - rr)],
              300, 40, fill=(90, 170, 255), width=4)


def pic_cyclone(d, cx, cy, s, col):
    pts = []
    turns = 2.7
    steps = 130
    for i in range(steps + 1):
        t = i / steps
        ang = t * turns * 2 * math.pi
        r = s * (0.14 + 0.82 * t)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.85))
    d.line(pts, fill=col, width=7, joint="curve")
    ex, ey = pts[-1]
    d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=col)
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=(40, 110, 190), width=6)


# ---------------------------------------------------------------- hero scene

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_palm(d, x, base_y, h, lean, col):
    top_x = x + lean
    top_y = base_y - h
    segs = 14
    prev = (x, base_y)
    for i in range(1, segs + 1):
        t = i / segs
        px = x + lean * t * t
        py = base_y - h * t
        d.line([prev, (px, py)], fill=col, width=max(4, int(13 * (1 - t) + 4)))
        prev = (px, py)
    for ang in (-165, -125, -85, -40, -5, 30):
        L = h * 0.52
        ex = top_x + L * math.cos(math.radians(ang))
        ey = top_y + L * math.sin(math.radians(ang)) + L * 0.38
        mx = top_x + L * 0.55 * math.cos(math.radians(ang))
        my = top_y + L * 0.55 * math.sin(math.radians(ang)) - L * 0.12
        d.line([(top_x, top_y), (mx, my), (ex, ey)], fill=col, width=7, joint="curve")


def hero_scene(img, box):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    top = (58, 16, 96)        # deep purple
    mid = (198, 40, 110)      # magenta
    low = (255, 110, 60)      # orange
    hor = (255, 176, 66)      # golden horizon
    horizon = y0 + int((y1 - y0) * 0.62)
    for y in range(y0, horizon):
        t = (y - y0) / max(1, horizon - y0)
        col = lerp(top, mid, t) if t < 0.55 else lerp(mid, low, (t - 0.55) / 0.45)
        d.line([x0, y, x1, y], fill=col)
    for y in range(horizon, y1):
        t = (y - horizon) / max(1, y1 - horizon)
        d.line([x0, y, x1, y], fill=lerp(hor, (30, 14, 54), t))
    # sun (retro disc with stripe cuts near the bottom)
    scx, scy, sr = x0 + int((x1 - x0) * 0.70), horizon - 46, 82
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=(255, 205, 60))
    d.ellipse([scx - sr + 14, scy - sr + 14, scx + sr - 14, scy + sr - 14], fill=(255, 165, 55))
    for i, yy in enumerate(range(scy + 22, scy + sr, 13)):
        d.rectangle([scx - sr, yy, scx + sr, yy + 4 + i], fill=(214, 60, 105))
    # skyline silhouette
    sil = (26, 10, 44)
    bx = x0 + 8
    heights = [54, 82, 44, 100, 62, 74, 38, 88, 50, 70, 104, 46, 78, 58, 94, 42, 68, 54, 86, 48, 76, 64, 52, 92]
    i = 0
    while bx < x1 - 30:
        bw = 30 + (i * 17) % 26
        bh = heights[i % len(heights)]
        d.rectangle([bx, horizon - bh, bx + bw, horizon], fill=sil)
        bx += bw + 5
        i += 1
    # palms
    draw_palm(d, x0 + 92, horizon + 6, 128, 30, sil)
    draw_palm(d, x1 - 70, horizon + 6, 102, -24, sil)
    draw_palm(d, x0 + 205, horizon + 6, 80, 18, sil)


# ---------------------------------------------------------------- layout

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    title = "THE WORLD IN A DAY"
    f_title = fit_font(d, title, BLACK, 84, W - 80)
    tw = text_w(d, title, f_title)
    d.text(((W - tw) / 2, 14), title, font=f_title, fill=INK)
    d.rectangle([24, 112, W - 24, 118], fill=INK)
    date = "THURSDAY · 19 NOVEMBER 2026"
    f_date = font(BOLD, 30)
    dw = text_w(d, date, f_date)
    d.text(((W - dw) / 2, 126), date, font=f_date, fill=RED)
    d.rectangle([24, 166, W - 24, 170], fill=INK)

    # ---- hero panel (GTA VI)
    hx0, hy0, hx1, hy1 = 24, 184, W - 24, 444
    hero_scene(img, (hx0, hy0, hx1, hy1))
    d = ImageDraw.Draw(img, "RGBA")
    # TOP STORY tag
    tag = "TOP STORY"
    f_tag = font(BLACK, 29)
    tagw = text_w(d, tag, f_tag) + 34
    d.rectangle([hx0 + 16, hy0 + 14, hx0 + 16 + tagw, hy0 + 60], fill=RED)
    d.text((hx0 + 33, hy0 + 21), tag, font=f_tag, fill=WHITE)
    # headline band
    band_y = hy1 - 140
    d.rectangle([hx0, band_y, hx1, hy1], fill=(14, 8, 30, 238))
    d.text((hx0 + 24, band_y + 10), "GTA VI IS HERE", font=font(BLACK, 58), fill=WHITE)
    f_sub = font(BOLD, 24)
    sub = "13-year wait ends to rave reviews — the biggest entertainment launch in history"
    for i, ln in enumerate(wrap(d, sub, f_sub, 600)):
        d.text((hx0 + 24, band_y + 82 + i * 28), ln, font=f_sub, fill=(255, 214, 120))
    # stats, right column of the band
    stat = "$1.84B · DAY ONE"
    f_stat = font(BLACK, 38)
    sw = text_w(d, stat, f_stat)
    d.text((hx1 - 24 - sw, band_y + 14), stat, font=f_stat, fill=GOLD)
    stat2 = "~19M COPIES · 2x GTA V"
    f_stat2 = font(BLACK, 24)
    sw2 = text_w(d, stat2, f_stat2)
    d.text((hx1 - 24 - sw2, band_y + 62), stat2, font=f_stat2, fill=WHITE)
    d.rectangle([hx0, hy0, hx1, hy1], outline=INK, width=3)

    # ---- news grid: 3 columns x 2 rows
    panels = [
        ("MYANMAR GUILTY OF GENOCIDE",
         "World Court: first state ever held responsible under the 1948 Genocide Convention — the Rohingya case.",
         (146, 30, 40), pic_scales),
        ("TRUMP–XI–PUTIN SUMMIT",
         "First-ever trilateral summit, in China. Joint “peace declaration”; Ukraine and Iran top the agenda.",
         (30, 70, 140), pic_globe),
        ("ANTHROPIC IPO TOPS $2 TRILLION",
         "First purely AI company to go public, debuting among the world's most valuable firms.",
         (90, 40, 140), pic_chart),
        ("3 TANKERS ABLAZE AT HORMUZ",
         "Ships hit mines east of the strait. Trump signals no more major US strikes on Iran in 2026.",
         (196, 84, 20), pic_tanker),
        ("VOYAGER 1: ONE LIGHT-DAY OUT",
         "NASA's farthest probe is now a full light-day from Earth — a first for any spacecraft.",
         (20, 60, 130), pic_probe),
        ("CYCLONE AKVAN BATTERS INDIA",
         "Hundreds of thousands evacuated in the east as the storm drives flooding inland.",
         (0, 110, 130), pic_cyclone),
    ]
    gx, gy = 24, 458
    cw, chh, gap = 317, 234, 12
    for idx, (head, fact, accent, pic) in enumerate(panels):
        px = gx + (idx % 3) * (cw + gap)
        py = gy + (idx // 3) * (chh + gap)
        d.rectangle([px, py, px + cw, py + chh], fill=WHITE, outline=(190, 182, 165), width=2)
        d.rectangle([px, py, px + cw, py + 10], fill=accent)
        # pictogram, top-left
        pic(d, px + 37, py + 43, 27, accent)
        # category-free headline, full width under the icon row
        f_head, hlines = fit_wrap(d, head, BLACK, 28, cw - 98, 2)
        for i, ln in enumerate(hlines):
            d.text((px + 76, py + 22 + i * 33), ln, font=f_head, fill=INK)
        # fact text
        f_fact = font(BOLD, 20)
        flines = wrap(d, fact, f_fact, cw - 28)
        for i, ln in enumerate(flines[:4]):
            d.text((px + 14, py + 138 + i * 24), ln, font=f_fact, fill=(52, 56, 64))

    # ---- footer ticker
    ty = gy + 2 * chh + gap + 12  # 950
    d.rectangle([0, ty, W, H], fill=INK)
    f_tick_head = font(BLACK, 22)
    d.text((24, ty + 12), "ALSO", font=f_tick_head, fill=GOLD)
    d.text((24, ty + 38), "TODAY", font=f_tick_head, fill=GOLD)
    ticker = ("Houthi attack damages Riyadh's tallest tower (Saudi fund HQ); no injuries  •  "
              "Cambridge Dictionary Word of the Year: “Human”  •  Trump posthumously pardons Pete Rose")
    f_tick = font(BOLD, 20)
    tlines = wrap(d, ticker, f_tick, W - 150)
    for i, ln in enumerate(tlines[:2]):
        d.text((126, ty + 12 + i * 26), ln, font=f_tick, fill=WHITE)

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
