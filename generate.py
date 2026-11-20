#!/usr/bin/env python3
"""Draw the front page for the make.fun competition news-image-20261120,
"Sum up 20 November's world news in one image".

A newspaper-style front page, drawn procedurally with PIL: a huge date
header over six captioned panels covering the defining stories of
Friday 20 November 2026, plus an "also today" ticker along the bottom.

Stories (reported 20 Nov 2026; SCMP, Just Security's Early Edition,
Reuters, Dawn, One Turn News, Saudi Gazette):
  1. The ICJ rules Myanmar committed genocide against the Rohingya --
     the first genocide finding against a state by the world court.
  2. Trump, Xi and Putin end their first three-way summit in Shenzhen
     with a four-point peace declaration.
  3. Anthropic's $81bn Nasdaq debut is the biggest IPO in history, yet
     US stocks fall for a fifth straight day (S&P 500 about -2%).
  4. A Houthi missile hits Riyadh's tallest tower, the PIF Tower --
     the second strike on the financial district this month.
  5. Russian strikes on Kyiv kill six and damage bridges, embassies and
     a cathedral; Ukraine hits the Crimea (Kerch) Bridge a third time.
  6. Kenya discharges its last Ebola patient, 37 days after the first
     case -- the outbreak is over.
Ticker: COP31 draft drops fossil fuels; GTA VI sales top $2.3bn; the
UK and EU agree a youth-mobility reset; the US cyber chief is ousted
after a wave of tech outages; a Van Gogh sells for a record $190.4m.

Writes entry.png (1024x1024) beside this file. Deterministic: the same
bytes on every run.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

NAVY = (14, 22, 44)
GOLD = (233, 186, 82)
PAPER = (244, 240, 230)
INK = (16, 18, 24)
CAP_BG = (9, 13, 26)
CAP_SUB = (196, 205, 224)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, size, max_w):
    """Shrink from `size` until `text` fits within max_w pixels."""
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, size)


def tracked(draw, xy, text, f, fill, tracking=8):
    """Draw text with extra letter spacing, centred on xy's x."""
    total = sum(draw.textlength(ch, font=f) for ch in text) + tracking * (len(text) - 1)
    x = xy[0] - total / 2
    for ch in text:
        draw.text((x, xy[1]), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return total


def vgrad(size, top, bottom):
    """A vertical gradient image of the given size."""
    w, h = size
    img = Image.new("RGB", size, top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=tuple(
            int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img


PW, PH = 478, 232          # panel size
SCENE_H, CAP_H = 152, 80   # scene and caption split inside a panel


def panel(top, bottom, head, sub):
    """One panel: gradient scene area on top, caption bar below."""
    img = vgrad((PW, PH), top, bottom)
    d = ImageDraw.Draw(img)
    d.rectangle([0, SCENE_H, PW, PH], fill=CAP_BG)
    d.line([(0, SCENE_H), (PW, SCENE_H)], fill=GOLD, width=3)
    lines = head.split("\n")
    if len(lines) == 1:
        f = fit_font(d, lines[0], BOLD, 27, PW - 28)
        d.text((14, SCENE_H + 9), lines[0], font=f, fill=(255, 255, 255))
        y = SCENE_H + 44
    else:
        for i, ln in enumerate(lines):
            f = fit_font(d, ln, BOLD, 24, PW - 28)
            d.text((14, SCENE_H + 5 + i * 27), ln, font=f, fill=(255, 255, 255))
        y = SCENE_H + 59
    fs = fit_font(d, sub, REG, 17, PW - 28)
    d.text((14, y), sub, font=fs, fill=CAP_SUB)
    return img


def burst(d, cx, cy, r, fill):
    """An eight-point explosion star."""
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flag_us(d, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe + 1],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.42, y + stripe * 7], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([x + 6 + c * w * 0.078, y + 4 + r * stripe * 1.6,
                       x + 10 + c * w * 0.078, y + 8 + r * stripe * 1.6],
                      fill=(255, 255, 255))


def star(d, cx, cy, r, fill):
    """A filled five-pointed star."""
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(d, x + w * 0.17, y + h * 0.24, 9, (255, 222, 0))
    for dx, dy in ((0.32, 0.10), (0.36, 0.24), (0.36, 0.38), (0.31, 0.50)):
        star(d, x + w * dx, y + h * dy, 4, (255, 222, 0))


def flag_ru(d, x, y, w, h):
    third = h / 3
    d.rectangle([x, y, x + w, y + third + 1], fill=(245, 245, 245))
    d.rectangle([x, y + third, x + w, y + 2 * third + 1], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 43, 30))


def p_court():
    img = panel((198, 208, 220), (150, 162, 182),
                "WORLD COURT: MYANMAR\nCOMMITTED GENOCIDE",
                "First ICJ genocide verdict against a state · Rohingya")
    d = ImageDraw.Draw(img)
    cx = PW // 2
    # courthouse: steps, columns, pediment
    d.rectangle([cx - 150, 128, cx + 150, 140], fill=(226, 228, 232))
    d.rectangle([cx - 138, 116, cx + 138, 128], fill=(214, 216, 222))
    for i, dx in enumerate((-118, -60, 60, 118)):
        d.rectangle([cx + dx - 13, 58, cx + dx + 13, 116], fill=(238, 239, 243))
    d.rectangle([cx - 142, 46, cx + 142, 58], fill=(226, 228, 232))
    d.polygon([(cx - 150, 46), (cx + 150, 46), (cx, 12)], fill=(240, 241, 245))
    d.ellipse([cx - 11, 22, cx + 11, 44], fill=GOLD)
    # scales of justice in front
    d.line([(cx, 66), (cx, 128)], fill=(90, 70, 20), width=5)
    d.line([(cx - 52, 74), (cx + 52, 74)], fill=(90, 70, 20), width=5)
    for sx in (-52, 52):
        d.line([(cx + sx, 74), (cx + sx - 16, 102)], fill=(90, 70, 20), width=3)
        d.line([(cx + sx, 74), (cx + sx + 16, 102)], fill=(90, 70, 20), width=3)
        d.arc([cx + sx - 20, 96, cx + sx + 20, 116], 0, 180, fill=(90, 70, 20), width=4)
    d.ellipse([cx - 8, 58, cx + 8, 74], fill=GOLD)
    return img


def p_summit():
    img = panel((30, 52, 96), (16, 28, 56),
                "TRUMP · XI · PUTIN SIGN\nPEACE DECLARATION",
                "First three-way summit ends in Shenzhen, China")
    d = ImageDraw.Draw(img)
    # sun
    d.ellipse([PW - 128, 16, PW - 64, 80], fill=(250, 205, 92))
    # skyline silhouettes
    towers = [(0, 96, 44, 152), (52, 78, 96, 152), (104, 106, 140, 152),
              (330, 88, 372, 152), (380, 66, 424, 152), (430, 100, 478, 152)]
    for x0, y0, x1, y1 in towers:
        d.rectangle([x0, y0, x1, y1], fill=(10, 16, 32))
        for wy in range(y0 + 8, y1 - 6, 14):
            for wx in range(x0 + 6, x1 - 6, 12):
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(250, 214, 120))
    # three flags on poles
    for i, draw_flag in enumerate((flag_us, flag_cn, flag_ru)):
        x = 128 + i * 78
        d.line([(x, 26), (x, 132)], fill=(210, 214, 224), width=4)
        draw_flag(d, x + 4, 28, 62, 42)
    return img


def p_markets():
    img = panel((10, 26, 22), (6, 16, 14),
                "ANTHROPIC'S $81BN IPO:\nBIGGEST DEBUT IN HISTORY",
                "Closes up 17% — but US stocks fall a fifth straight day")
    d = ImageDraw.Draw(img)
    # rising gold candles (the IPO)
    candles = [(36, 70, 112), (84, 50, 94), (132, 30, 74)]
    for x, top, bot in candles:
        d.line([(x + 13, top - 10), (x + 13, bot + 8)], fill=(64, 199, 116), width=3)
        d.rectangle([x, top, x + 26, bot], fill=(64, 199, 116))
    f = fit_font(d, "+17%", BOLD, 38, 150)
    d.text((168, 100), "+17%", font=f, fill=(64, 199, 116))
    # falling red index line (the wider market)
    pts = [(238, 34), (282, 52), (318, 48), (356, 76), (392, 84), (436, 116)]
    d.line(pts, fill=(235, 84, 74), width=5, joint="curve")
    for x, y in pts:
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(235, 84, 74))
    d.polygon([(436, 116), (420, 112), (430, 100)], fill=(235, 84, 74))
    f2 = fit_font(d, "S&P -2%", BOLD, 34, 170)
    d.text((300, 112), "S&P -2%", font=f2, fill=(235, 84, 74))
    return img


def p_riyadh():
    img = panel((96, 52, 92), (196, 102, 52),
                "HOUTHI MISSILE HITS RIYADH'S\nTALLEST TOWER",
                "Second strike on the financial district this month")
    d = ImageDraw.Draw(img)
    cx = PW // 2
    # the tower, tapered, centre
    d.polygon([(cx - 46, 152), (cx - 26, 18), (cx + 26, 18), (cx + 46, 152)],
              fill=(38, 34, 54))
    for wy in range(30, 146, 13):
        half = 26 + (wy - 18) * 20 // 134
        for wx in range(cx - half + 5, cx + half - 6, 11):
            d.rectangle([wx, wy, wx + 5, wy + 6], fill=(250, 214, 120))
    # neighbouring blocks
    d.rectangle([cx - 128, 92, cx - 62, 152], fill=(30, 27, 44))
    d.rectangle([cx + 66, 104, cx + 126, 152], fill=(30, 27, 44))
    # impact burst at the top floors + missile trail
    burst(d, cx + 6, 40, 30, (255, 176, 66))
    burst(d, cx + 6, 40, 16, (255, 240, 200))
    trail = [(40 + i * 13, 10 + int(30 * (i / 15) ** 1.6)) for i in range(16)]
    d.line(trail, fill=(255, 220, 160), width=3)
    return img


def p_kyiv():
    img = panel((24, 34, 68), (10, 14, 30),
                "KYIV STRUCK AGAIN;\nCRIMEA BRIDGE HIT",
                "Barrage kills six, damages embassies and a cathedral")
    d = ImageDraw.Draw(img)
    # skyline with a cathedral dome
    d.rectangle([0, 96, 150, 132], fill=(8, 10, 20))
    d.rectangle([330, 90, 478, 132], fill=(8, 10, 20))
    d.rectangle([196, 84, 236, 132], fill=(8, 10, 20))
    d.ellipse([198, 58, 234, 92], fill=(12, 14, 26))
    d.polygon([(206, 62), (226, 62), (216, 38)], fill=GOLD)
    for base_x, wdt in ((10, 130), (340, 128)):
        for wy in range(100, 126, 12):
            for wx in range(base_x + 6, base_x + wdt - 8, 16):
                d.rectangle([wx, wy, wx + 6, wy + 7], fill=(250, 214, 120))
    # river
    d.rectangle([0, 132, PW, SCENE_H], fill=(18, 44, 74))
    # bridge: deck, two pylons, cables
    d.rectangle([0, 118, PW, 124], fill=(196, 202, 214))
    for px in (120, 356):
        d.rectangle([px, 66, px + 8, 132], fill=(196, 202, 214))
        for t in range(0, 9):
            d.line([(px + 4, 70), (px + 4 - 60 + t * 15, 118)], fill=(140, 148, 164), width=1)
            d.line([(px + 4, 70), (px + 4 + 60 - t * 15, 118)], fill=(140, 148, 164), width=1)
    # bursts over the city and on the bridge
    burst(d, 84, 44, 22, (255, 150, 60))
    burst(d, 408, 34, 18, (255, 176, 66))
    burst(d, 268, 112, 20, (255, 120, 50))
    burst(d, 268, 112, 10, (255, 236, 190))
    return img


def p_kenya():
    img = panel((250, 176, 92), (246, 226, 170),
                "KENYA EBOLA-FREE: LAST\nPATIENT GOES HOME",
                "Outbreak ends 37 days after the first case")
    d = ImageDraw.Draw(img)
    # rising sun
    d.ellipse([186, 30, 292, 136], fill=(255, 150, 60))
    d.ellipse([204, 48, 274, 118], fill=(255, 196, 92))
    # hills, clipped to the scene area so they stay off the caption
    d.ellipse([-90, 102, 270, 152], fill=(74, 140, 74))
    d.ellipse([230, 106, 580, 152], fill=(58, 122, 62))
    # medical cross in a white roundel
    d.ellipse([56, 44, 140, 128], fill=(255, 255, 255))
    d.rectangle([88, 60, 108, 112], fill=(206, 44, 44))
    d.rectangle([70, 76, 126, 96], fill=(206, 44, 44))
    # acacia tree silhouette
    d.polygon([(392, 128), (400, 128), (398, 92), (396, 92)], fill=(40, 34, 26))
    d.ellipse([344, 66, 452, 96], fill=(46, 92, 44))
    d.line([(397, 92), (368, 76)], fill=(40, 34, 26), width=4)
    d.line([(397, 92), (428, 74)], fill=(40, 34, 26), width=4)
    return img


def build():
    page = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(page)
    # masthead
    tracked(d, (W // 2, 20), "THE WORLD IN ONE PICTURE", font(SERIF, 30), GOLD, 10)
    f_date = fit_font(d, "20 NOVEMBER 2026", BOLD, 104, W - 40)
    tw = d.textlength("20 NOVEMBER 2026", font=f_date)
    d.text(((W - tw) / 2, 56), "20 NOVEMBER 2026", font=f_date, fill=PAPER)
    d.rectangle([26, 172, W - 26, 176], fill=GOLD)
    tracked(d, (W // 2, 182), "FRIDAY · SIX STORIES THAT DEFINED THE DAY",
            font(BOLD, 19), CAP_SUB, 4)
    # panels, 2 x 3
    panels = [p_court(), p_summit(), p_markets(), p_riyadh(), p_kyiv(), p_kenya()]
    for i, p in enumerate(panels):
        x = 26 + (i % 2) * (PW + 16)
        y = 214 + (i // 2) * (PH + 13)
        page.paste(p, (x, y))
    # ticker
    d.rectangle([0, 950, W, H], fill=(122, 24, 32))
    d.rectangle([0, 950, W, 954], fill=GOLD)
    t1 = "ALSO TODAY — COP31 DRAFT DROPS FOSSIL FUELS · GTA VI SALES TOP $2.3BN"
    t2 = "UK–EU YOUTH MOBILITY RESET · US CYBER CHIEF OUSTED · VAN GOGH SELLS FOR $190.4M"
    for j, t in enumerate((t1, t2)):
        f = fit_font(d, t, BOLD, 21, W - 36)
        tw = d.textlength(t, font=f)
        d.text(((W - tw) / 2, 962 + j * 30), t, font=f, fill=(255, 244, 224))
    page.save("entry.png")
    print("wrote entry.png")


if __name__ == "__main__":
    build()
