"""Neon timeline building blocks (Bloomberg Business explainer style), 1080x1920, PIL only.

Import it and build frames:
    import sys; sys.path.insert(0, '.claude/skills/bloomberg-style/scripts'); import neon as N
    N.FONT_DIR = '<dir with fontsource inter package>'   # .../fonts/inter/package/files
    im = N.timeline_scene(t, stops, active=1)         # camera pans down the spine to stop 1
    im = N.chart_scene(t, [238, 205, 164, 126, 165, 149], ['Oct', 'Nov', 'Wed'], '$149', 'Nvidia', 'last 7 weeks')
    im = N.framed_media(N.bg(), photo, (120, 330, 960, 900), t, credit='Nvidia')
    N.caption(im, 'then it fell 6% on Tuesday')
Run this file directly for a demo sheet: python3 neon.py FONT_DIR PHOTO OUT.png
"""
import math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FONT_DIR = ''
SPINE_X = 300
CYAN = (20, 160, 255)            # glow color; swap for a brand color if asked
CORE = (170, 235, 255)           # bright core of every glowing line
MINT = (60, 240, 210)            # chart line
NAVY0, NAVY1 = (2, 6, 14), (10, 24, 44)
WHITE, GREY, DIM, RED = (236, 240, 248), (165, 175, 190), (120, 130, 150), (255, 90, 80)

def font(size, weight=800):
    return ImageFont.truetype(f'{FONT_DIR}/inter-latin-{weight}-normal.woff', size)

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

# ---------- background ----------
_bg_cache = {}
def bg(seed=1, drift=0.0):
    """near-black navy, vignette, faint falling streaks. drift (px) moves the streaks down for motion."""
    key = (seed, int(drift) % H)
    if key in _bg_cache: return _bg_cache[key].copy()
    ys = np.linspace(0, 1, H)[:, None]; xs = np.linspace(-1, 1, W)[None, :]
    v = np.clip(1 - (xs ** 2 * 0.6 + (ys - 0.45) ** 2 * 1.2), 0, 1)
    a = np.array(NAVY0) + (np.array(NAVY1) - np.array(NAVY0)) * v[..., None]
    im = Image.fromarray(a.astype(np.uint8)).convert('RGBA')
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = random.Random(seed)
    for _ in range(140):
        x, y, L = r.uniform(0, W), (r.uniform(0, H) + drift) % H, r.uniform(10, 40)
        d.line([(x, y), (x - L * 0.25, y + L)], fill=(170, 200, 230, r.randint(25, 70)), width=2)
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.2)))
    _bg_cache[key] = im
    return im.copy()

# ---------- glow ----------
def glow_line(im, pts, width=4, col=None):
    col = col or CYAN
    for w_, blur, n in ((width * 6, 28, 2), (width * 2, 8, 2)):
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).line(pts, fill=col + (255,), width=w_)
        g = lay.filter(ImageFilter.GaussianBlur(blur))
        for _ in range(n): im.alpha_composite(g)
    ImageDraw.Draw(im).line(pts, fill=CORE, width=width)

def glow_rect(im, box, width=4, col=None):
    x0, y0, x1, y1 = box
    glow_line(im, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], width, col)

# ---------- media ----------
def duotone(img, size):
    """blue-gray duotone, cover-cropped to size (favoring the top third, where faces are)."""
    p = img.convert('L'); tw, th = size
    s = max(tw / p.width, th / p.height); p = p.resize((int(p.width * s) + 1, int(p.height * s) + 1), Image.LANCZOS)
    p = p.crop(((p.width - tw) // 2, (p.height - th) // 4, (p.width - tw) // 2 + tw, (p.height - th) // 4 + th))
    a = np.array(p, np.float32)[..., None] / 255
    dark, light = np.array([8, 22, 40]), np.array([215, 232, 245])
    return Image.fromarray((dark + (light - dark) * a).astype(np.uint8)).convert('RGBA')

def framed_media(im, img, box, t=1.0, credit=None, slide=120):
    """photo or video frame in a neon box; slides up and fades in over 0.4 s."""
    k = ease(t / 0.4); dy = int(slide * (1 - k))
    x0, y0, x1, y1 = box; b = (x0, y0 + dy, x1, y1 + dy)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); glow_rect(lay, b)
    lay.alpha_composite(duotone(img, (x1 - x0 - 8, y1 - y0 - 8)), (x0 + 4, y0 + 4 + dy))
    if credit: ImageDraw.Draw(lay).text((x0, y1 + dy + 14), f'Credit: {credit}', font=font(28, 600), fill=DIM)
    if k < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * k)))
    im.alpha_composite(lay)
    return im

# ---------- timeline ----------
def stop(im, y, day, month, lines, t=1.0):
    """one date stop: dot on the spine, dotted rule, huge day number, month, gray summary lines."""
    d = ImageDraw.Draw(im); k = ease(t / 0.35)
    d.ellipse([SPINE_X - 11, y - 11, SPINE_X + 11, y + 11], fill=WHITE)
    for x in range(SPINE_X + 20, int(SPINE_X + 20 + (W - 80 - SPINE_X) * k), 14): d.line([(x, y), (x + 7, y)], fill=(120, 170, 210), width=2)
    f = font(210); d.text((SPINE_X - 30 - d.textlength(day, font=f), y - 20 + 30 * (1 - k)), day, font=f, fill=WHITE)
    d.text((SPINE_X + 30, y + 22), month, font=font(56), fill=WHITE)
    for i, line in enumerate(lines):
        if t > 0.25 + 0.15 * i: d.text((SPINE_X + 30, y + 98 + i * 52), line, font=font(42, 600), fill=GREY)

def timeline_scene(t, stops, active, pan=0.6, gap=1500):
    """stops: [dict(day, month, lines, media=PIL.Image|None, credit)]. The camera sits on `active`;
    for the first `pan` seconds it travels down from the previous stop. Each stop is `gap` px apart."""
    k = ease(t / pan) if active > 0 else 1.0
    cam = (active - 1 + k) * gap if active > 0 else 0
    im = bg(drift=cam * 0.3); glow_line(im, [(SPINE_X, 0), (SPINE_X, H)], 4)
    for i, s in enumerate(stops):
        oy = int(i * gap - cam)
        if -H < oy < H:
            if s.get('media') is not None:
                framed_media(im, s['media'], (120, 330 + oy, 960, 900 + oy), t if i == active else 1.0, s.get('credit'))
            stop(im, 1040 + oy, s['day'], s['month'], s['lines'], (t - pan * 0.6) if i == active else 1.0)
    return im

# ---------- chart ----------
def chart_scene(t, values, xlabels, end_label, title, subtitle, draw=1.2):
    im = bg(2); d = ImageDraw.Draw(im)
    tw = d.textlength(title, font=font(110)); d.text(((W - tw) / 2, 300), title, font=font(110), fill=WHITE)
    sw = d.textlength(subtitle, font=font(50, 600)); d.text(((W - sw) / 2, 430), subtitle, font=font(50, 600), fill=GREY)
    lo, hi = min(values) * 0.9, max(values) * 1.05
    x0, x1, yb, yt = 130, 900, 1250, 620
    X = lambda i: x0 + (x1 - x0) * i / (len(values) - 1); Y = lambda v: yb - (yb - yt) * (v - lo) / (hi - lo)
    step = 10 ** math.floor(math.log10((hi - lo) / 3)); step *= 2 if (hi - lo) / step > 6 else 1
    v = math.ceil(lo / step) * step
    while v < hi:
        d.line([(x0, Y(v)), (x1, Y(v))], fill=(40, 60, 85), width=2); d.text((x1 + 20, Y(v) - 22), f'${v:g}', font=font(36, 600), fill=GREY); v += step
    n = (len(values) - 1) * ease(t / draw); pts = [(X(i), Y(values[i])) for i in range(int(n) + 1)]
    if n < len(values) - 1:
        i = int(n); f = n - i; pts.append((X(i) + (X(i + 1) - X(i)) * f, Y(values[i]) + (Y(values[i + 1]) - Y(values[i])) * f))
    if len(pts) > 1: glow_line(im, pts, 6, MINT)
    d = ImageDraw.Draw(im)
    for j, lab in enumerate(xlabels):
        i = round(j * (len(values) - 1) / max(1, len(xlabels) - 1)); d.text((X(i) - 30, yb + 24), lab, font=font(38, 600), fill=GREY)
    if t >= draw:
        ex, ey = X(len(values) - 1), Y(values[-1])
        d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(255, 255, 255)); d.text((ex - d.textlength(end_label, font=font(64)) - 30, ey + 30), end_label, font=font(64), fill=WHITE)
    return im

# ---------- captions ----------
def caption(im, text, y=1420):
    """white, bold, sentence case, centered, up to 2 lines, no box."""
    d = ImageDraw.Draw(im); f = font(54, 700); words = text.split(); lines = ['']
    for w_ in words:
        if d.textlength((lines[-1] + ' ' + w_).strip(), font=f) > 900: lines.append('')
        lines[-1] = (lines[-1] + ' ' + w_).strip()
    for i, l in enumerate(lines[:2]): d.text(((W - d.textlength(l, font=f)) / 2, y + i * 66), l, font=f, fill=(255, 255, 255))
    return im

if __name__ == '__main__':
    FONT_DIR, photo, out = sys.argv[1], sys.argv[2], sys.argv[3]
    ph = Image.open(photo)
    stops = [dict(day='12', month='November', lines=['Huang quits.', 'Nvidia falls 23%.'], media=ph, credit='Nvidia'),
             dict(day='23', month='November', lines=['Board brings him back.', 'Nvidia +31%.'], media=ph, credit='Nvidia')]
    frames = [timeline_scene(1.2, stops, 0), timeline_scene(0.3, stops, 1), timeline_scene(1.2, stops, 1),
              chart_scene(2.0, [238, 225, 205, 190, 164, 126, 165, 155, 149], ['Oct', 'Nov', 'Wed'], '$149', 'Nvidia', 'last 7 weeks')]
    for f_, c in zip(frames, ['On November 12th, he quit.', 'But come November 23rd,', 'the board does a complete 180.', 'and the stock took a dive.']): caption(f_, c)
    sh = Image.new('RGB', (4 * 370 + 10, 660), (24, 24, 24))
    for i, f_ in enumerate(frames): sh.paste(f_.convert('RGB').resize((360, 640), Image.LANCZOS), (10 + i * 370, 10))
    sh.save(out); print('ok', out)
