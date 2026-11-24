import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = '/tmp/claude-0/-home-user-enisonoff/672c1244-cc8a-569f-a9ee-237151e2864a/scratchpad'
V = S + '/v14'; W, H = 1080, 1920
F = lambda name, w, s: ImageFont.truetype(f'{S}/fonts/{name}/package/files/{name}-latin-{w}-normal.woff', s)
MONT = lambda w, s: F('montserrat', w, s); ANTON = lambda s: F('anton', 400, s); MARK = lambda s: F('permanent-marker', 400, s); CAV = lambda s: F('caveat', 700, s)
BLUE = (22, 70, 255); YEL = (255, 222, 0); INK = (14, 14, 18); WHITE = (255, 255, 255)
rnd = random.Random(4)

def highlight(d, box, col=YEL):
    """a marker swipe behind text: slightly uneven edges"""
    x0, y0, x1, y1 = box; pts = []
    for i in range(12): pts.append((x0 + (x1 - x0) * i / 11, y0 + rnd.uniform(-4, 4)))
    for i in range(12): pts.append((x1 - (x1 - x0) * i / 11, y1 + rnd.uniform(-4, 4)))
    d.polygon(pts, fill=col)

def stack(im, rows, cx, y):
    """rows: list of (text, font, color, highlight?) centered as one poster"""
    d = ImageDraw.Draw(im)
    for txt, f, col, hl in rows:
        bb = d.textbbox((0, 0), txt, font=f); tw, th = bb[2] - bb[0], bb[3] - bb[1]; x = cx - tw / 2
        if hl: highlight(d, (x - 16, y + bb[1] - 6, x + tw + 16, y + bb[3] + 10))
        d.text((x, y), txt, font=f, fill=col); y += bb[3] + 18
    return y

def caption(im, words, hi):
    d = ImageDraw.Draw(im); f = MONT(800, 54); sp = d.textlength(' ', font=f)
    tw = sum(d.textlength(w, font=f) for w in words) + sp * (len(words) - 1); x = (W - tw) / 2; y = 1380
    for k, w in enumerate(words):
        for dx, dy in [(0, 4), (2, 3), (-2, 3)]: d.text((x + dx, y + dy), w, font=f, fill=(0, 0, 0))
        d.text((x, y), w, font=f, fill=YEL if k == hi else WHITE); x += d.textlength(w, font=f) + sp

def wobbly_circle(d, cx, cy, r, col, width=9, prog=1.0, seed=0):
    rr = random.Random(seed); n = 160; pts = []
    ph = [rr.uniform(0, 6.28) for _ in range(3)]
    for i in range(int(n * prog) + 1):
        a = -math.pi / 2 + 2 * math.pi * 1.04 * i / n            # overshoot a little, like a real marker loop
        rad = r * (1 + 0.025 * math.sin(3 * a + ph[0]) + 0.015 * math.sin(7 * a + ph[1]))
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    if len(pts) > 1: d.line(pts, fill=col, width=width, joint='curve')

def venn(im, prog=1.0, names=True):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    cxl, cxr, cy, r = 420, 660, 415, 150
    wobbly_circle(d, cxl, cy, r, BLUE, prog=min(1, prog * 2), seed=1)
    wobbly_circle(d, cxr, cy, r, (235, 40, 90), prog=max(0, min(1, prog * 2 - 1)), seed=2)
    d.text((cxl - 120, cy - 118), 'winners', font=MARK(40), fill=BLUE)
    d.text((cxr - 10, cy - 118), 'losers', font=MARK(40), fill=(235, 40, 90))
    if names:
        for i, n in enumerate(['jensen', 'nvidia staff', 'coreweave etc', 'the lawyers']): d.text((cxl - 128, cy - 62 + i * 40), n, font=CAV(36), fill=INK)
        for i, n in enumerate(['the board', 'colette kress', 'bessent', 'women']): d.text((cxr + 2, cy - 62 + i * 40), n, font=CAV(36), fill=INK)
        d.text((cxl + 100, cy + 66), 'weird', font=CAV(30), fill=INK); d.text((cxl + 94, cy + 94), 'middle', font=CAV(30), fill=INK)
    sh = lay.filter(ImageFilter.GaussianBlur(3)); im.alpha_composite(Image.eval(sh, lambda v: v), (0, 0)) if False else None
    im.alpha_composite(lay)

frames = []
# 1 · hook: mixed fonts above her head
im = Image.open(V + '/f2.png').convert('RGBA')
stack(im, [('the', MONT(700, 46), INK, False), ('WINNERS', ANTON(150), BLUE, False), ('& losers', MARK(78), INK, True), ('of jensen\'s return', MONT(600, 40), INK, False)], W / 2, 250)
caption(im, ['WINNERS', 'AND', 'LOSERS'], 0); frames.append(('hook: mixed-font poster above your head', im))
# 2 · a number moment
im = Image.open(V + '/f30.png').convert('RGBA')
stack(im, [('nvidia added', MONT(700, 44), INK, False), ('$952B', ANTON(170), BLUE, False), ('in one day', MARK(70), INK, True)], W / 2, 250)
caption(im, ['IN', 'ONE', 'DAY'], 2); frames.append(('big numbers: same poster system', im))
# 3 · the Venn, drawing on
im = Image.open(V + '/f70.png').convert('RGBA'); venn(im, prog=0.6, names=False)
caption(im, ['THE', 'BIGGEST', 'LOSERS'], 1); frames.append(('venn draws itself on (marker style)', im))
# 4 · the Venn, filled in
im = Image.open(V + '/f120.png').convert('RGBA'); venn(im, prog=1.0, names=True)
caption(im, ['THE', 'WEIRD', 'MIDDLE'], 1); frames.append(('venn fills in as you go; overlap = the weird middle', im))

sh = Image.new('RGB', (4 * 410 + 10, 760), (20, 20, 20)); dd = ImageDraw.Draw(sh)
for i, (lab, fr) in enumerate(frames):
    d = ImageDraw.Draw(fr)
    for yy in (250, 1560): d.line((0, yy, W, yy), fill=(255, 0, 0), width=3)
    sh.paste(fr.convert('RGB').resize((400, 711), Image.LANCZOS), (10 + i * 410, 10)); dd.text((14 + i * 410, 728), lab, font=MONT(600, 15), fill=(230, 230, 230))
sh.save(V + '/design_check.png'); print('ok')
