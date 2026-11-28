"""Elena's default reel look (approved on the outage video, Nov 2026). See SKILL.md.
Film grade every frame (per-frame rembg masks in m/), big Anton words behind her, Dosis secondary lines,
black grain cards, split screens for the explanation, bottom lowercase subtitles, every text item jumps on.
usage: REEL_DIR=... REEL_SRC=... REEL_WORDS=... REEL_BEATS=... python3 reel_style.py START END OUT.mp4"""
import sys, json, subprocess, os, importlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.environ['REEL_DIR']                                   # work folder: m/ masks, broll/ stills, transcript json
F = os.environ.get('REEL_FONTS', os.path.join(os.path.dirname(V), 'fonts'))   # fontsource packages (anton, dosis, inter, inter-tight, libre-baskerville, archivo-black)
W, H, FPS = 1080, 1920, 30
SRC = os.environ['REEL_SRC']                                 # rough cut (push-ins + loudnorm already applied)
if os.environ.get('REEL_TMAP'):                              # optional: beats timed on an older cut, mapped to this one
    sys.path.insert(0, os.path.dirname(os.environ['REEL_TMAP'])); tmap = importlib.import_module(os.path.basename(os.environ['REEL_TMAP'])[:-3])
else:
    class tmap:
        new_to_old_frame = staticmethod(lambda f: f)
sys.path.insert(0, HERE)
K = 1.25   # kinetic text scale (she asked +25%)
ANTON = lambda n: ImageFont.truetype(f'{F}/anton/package/files/anton-latin-400-normal.woff', int(n * K))
SOFT = lambda n: ImageFont.truetype(f'{F}/dosis/package/files/dosis-latin-500-normal.woff', int(n * K))   # Softedge stand-in
SUB = lambda n: ImageFont.truetype(f'{F}/inter/package/files/inter-latin-600-normal.woff', n)
RED = (232, 40, 44); WHITE = (250, 247, 240); INK = (10, 10, 10)
WORDS = json.load(open(os.environ['REEL_WORDS']))         # transcript of SRC (clean-cut takes.py output)

# ---------- grade ----------
yy, xx = np.mgrid[0:H, 0:W]
VIG = np.clip(1 - 0.45 * (((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H * 0.42) / (H * 0.62)) ** 2), 0.4, 1)[..., None].astype(np.float32)
del yy, xx
def load_mask(fi):
    p = f'{V}/m/{fi:05d}.png'
    while not os.path.exists(p) and fi > 0: fi -= 1; p = f'{V}/m/{fi:05d}.png'
    return Image.open(p).convert('L')
def grade(img, small_mask, fi):
    gm = small_mask.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)
    a = np.asarray(img, np.float32) / 255; m = (np.asarray(gm, np.float32) / 255)[..., None]
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32); lum = lum[..., None]
    a = a * (1 - 0.35 * (1 - m)) + lum * 0.35 * (1 - m)
    a = a * (1 - 0.12 * (1 - m))
    a = 0.5 + (a - 0.5) * 1.15
    sh = np.clip(1 - lum * 2.2, 0, 1); mid = np.clip(1 - np.abs(lum - 0.55) * 2.5, 0, 1)
    a = a + sh * np.array([-0.035, 0.03, 0.03], np.float32) + mid * np.array([0.05, 0.015, -0.04], np.float32)
    a = 0.045 + a * 0.93
    hi = np.clip((lum - 0.7) * 3, 0, 1)
    glow = Image.fromarray((np.clip(a * hi, 0, 1) * 255).astype(np.uint8)).resize((W // 4, H // 4)).filter(ImageFilter.GaussianBlur(3.5)).resize((W, H), Image.BILINEAR)
    a = a + np.asarray(glow, np.float32) / 255 * 0.35
    a = a * VIG + np.random.default_rng(fi).normal(0, 0.02, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
def cutout(small_mask):   # tight mask for words behind her
    return small_mask.resize((W, H), Image.BILINEAR).filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(3))

GRAIN = [Image.fromarray((np.clip(np.random.default_rng(k).normal(0.045, 0.02, (H // 2, W // 2)), 0, 1) * 255).astype(np.uint8)).resize((W, H)).convert('RGBA') for k in range(6)]

# ---------- text sprites that jump on ----------
def fit(fontf, text, maxw, size):
    maxw = max(maxw, 1040); f = fontf(size)
    while f.getlength(text) > maxw: size -= 4; f = fontf(size)
    return f
class Item:
    """one line of text: drawn once into a sprite, jumps on at time t0"""
    def __init__(self, t0, text, font, col, y, x=None, shadow='soft', brk=None):
        self.t0 = t0; self.brk = brk; bb = font.getbbox(text); pad = 40
        w, h = bb[2] + pad * 2, bb[3] + pad * 2
        self.x = (W - font.getlength(text)) / 2 if x is None else x; self.y = y
        spr = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0))
        if shadow:
            sd = Image.new('RGBA', spr.size, (0, 0, 0, 0))
            if shadow == 'soft': ImageDraw.Draw(sd).text((pad + 3, pad + 7), text, font=font, fill=(0, 0, 0, 150)); spr.alpha_composite(sd.filter(ImageFilter.GaussianBlur(9)))
            else: ImageDraw.Draw(sd).text((pad, pad), text, font=font, fill=(0, 0, 0, 210)); spr.alpha_composite(sd.filter(ImageFilter.GaussianBlur(6)))
        ImageDraw.Draw(spr).text((pad, pad), text, font=font, fill=col + (255,)); self.spr = spr; self.pad = pad
        self.cx = self.x - pad + w / 2; self.cy = y - pad + h / 2 + bb[1] / 2
        if brk is not None: self.pieces = self._cut(text, font, pad)
    def _cut(self, text, font, pad):
        # each word cracks in half along a jagged line through its middle -> 2 pieces per word
        bb = font.getbbox(text); mid = pad + (bb[1] + bb[3]) / 2; W_, H_ = self.spr.size
        xs = [0]; acc = pad
        for wd in text.split(' ')[:-1]: acc += font.getlength(wd + ' '); xs.append(int(acc - font.getlength(' ') / 2))
        xs.append(W_); rng = np.random.default_rng(7); out = []
        for i in range(len(xs) - 1):
            a, b = xs[i], xs[i + 1]; pts = []; x = a
            while x < b: pts.append((x, mid + rng.uniform(-18, 18))); x += 26
            pts.append((b, mid + rng.uniform(-18, 18)))
            for top in (True, False):
                m = Image.new('L', (W_, H_), 0); poly = [(a, 0), (b, 0)] if top else [(a, H_), (b, H_)]
                ImageDraw.Draw(m).polygon(poly[:1] + pts + poly[1:] if top else poly[:1] + pts + poly[1:], fill=255)
                pc = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); pc.paste(self.spr, (0, 0), m)
                side = -1 if i == 0 else 1; out.append((pc.crop((a, 0, b, H_)), a, top, side))
        return out
    def draw(self, canvas, t):
        u = t - self.t0 + 0.05          # start 1.5 frames early so it lands on the word
        if u < 0: return
        if self.brk is not None and t >= self.brk:
            k = (t - self.brk) / 0.5
            if k >= 1: return
            ox = self.cx - self.spr.width / 2; oy = self.cy - self.spr.height / 2
            for pc, a, top, side in self.pieces:
                rot = (-7 if top else 10) * side * k; dx = side * 30 * k; dy = (-45 * k) if top else (160 * k * k)
                p = pc.rotate(rot, resample=Image.BICUBIC, expand=True)
                if k > 0.35: p.putalpha(p.getchannel('A').point(lambda v, f=1 - (k - 0.35) / 0.65: int(v * f)))
                canvas.alpha_composite(p, (int(ox + a + pc.width / 2 - p.width / 2 + dx), int(oy + pc.height / 2 - p.height / 2 + dy)))
            return
        # snap: 4 frames, scale 0.8 -> 1.06 -> 1.0, 24 px rise
        if u < 0.133:
            k = u / 0.133
            s = 0.8 + 0.26 * min(k / 0.6, 1) if k < 0.6 else 1.06 - 0.06 * (k - 0.6) / 0.4
            dy = 24 * (1 - min(k / 0.6, 1)); al = min(u / 0.06, 1)
            sp = self.spr.resize((max(1, int(self.spr.width * s)), max(1, int(self.spr.height * s))), Image.BILINEAR)
            if al < 1: sp.putalpha(sp.getchannel('A').point(lambda v: int(v * al)))
        else: sp, dy = self.spr, 0
        canvas.alpha_composite(sp, (int(self.cx - sp.width / 2), int(self.cy - sp.height / 2 + dy)))

def head_top(a, b):
    top = 1920
    for fi in range(int(a * 30), int(b * 30), 3):
        p = f'{V}/m/{fi:05d}.png'
        if not os.path.exists(p): continue
        m = np.asarray(Image.open(p).convert('L'))[:, 100:260] > 128; rows = np.where(m.any(1))[0]
        if len(rows): top = min(top, rows[0] * 3)
    return top
def behind_set(t_small, small, t_big, big, col, y=300, t_below=None, below=None, brk=None, span=None):
    # words behind her head stay at the width they had: bigger only meant more of each word hidden behind her
    f = ImageFont.truetype(f'{F}/anton/package/files/anton-latin-400-normal.woff', 330)
    while f.getlength(big) > 960: f = ImageFont.truetype(f'{F}/anton/package/files/anton-latin-400-normal.woff', f.size - 4)
    if y == 'auto':      # bottom of the letters 70 px into her hair, top kept below 150 px for the IG header
        ht = head_top(*span); bb = f.getbbox(big)
        while ht + 25 - (bb[3] - bb[1]) < 150 and f.size > 150:
            f = ImageFont.truetype(f'{F}/anton/package/files/anton-latin-400-normal.woff', f.size - 6); bb = f.getbbox(big)
        y = ht + 25 - bb[3]
    x = (W - f.getlength(big)) / 2; sf = SOFT(70)
    back = [Item(t_big, big, f, col, y, brk=brk)]
    front = [Item(t_small, small, sf, WHITE, y - 62, x + 6, shadow=True, brk=brk)] if small else []
    for it in front: it.pieces = []          # the small line just clears when the big words break
    if below: front.append(Item(t_below, below, sf, WHITE, y + f.size * 1.24, x + f.getlength(below and big) - sf.getlength(below), shadow=True))
    return back, front


# ---------- headline clippings (sourced, outlet + date as plain text) ----------
HEAD = lambda n: ImageFont.truetype(f'{F}/libre-baskerville/package/files/libre-baskerville-latin-700-normal.woff', n)
def wrap(text, font, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if font.getlength(t) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]
def clipping(outlet, date, headline, hl, width=900, size=50):
    f = HEAD(size); meta = SUB(26); lines = wrap(headline, f, width - 80); lh = int(size * 1.32)
    h = 40 + 40 + len(lines) * lh + 34; im = Image.new('RGBA', (width, h), (246, 243, 236, 255)); d = ImageDraw.Draw(im)
    d.text((40, 30), f'{outlet.upper()}  ·  {date}', font=meta, fill=(110, 110, 110))
    y = 80; hw = set(hl.lower().split())
    for ln in lines:
        x = 40; ws = ln.split()
        for j, w in enumerate(ws):
            wl = f.getlength(w); key = w.lower().strip(',.:"')
            nxt = j + 1 < len(ws) and ws[j + 1].lower().strip(',.:"') in hw
            if key in hw: d.rectangle([x - 6, y + 4, x + wl + (f.getlength(' ') if nxt else 6), y + lh - 6], fill=RED)
            d.text((x, y), w, font=f, fill=(255, 255, 255) if key in hw else (15, 15, 15)); x += wl + f.getlength(' ')
        y += lh
    sh = Image.new('RGBA', (width + 60, h + 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([30, 38, width + 30, h + 38], fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(12)); sh.alpha_composite(im, (30, 30)); return sh
class Counter(Item):
    """big number that snaps on at t0, then rolls down to `to` at t1 and turns red"""
    def __init__(self, t0, a, t1, b, font, y):
        self.t0, self.a, self.t1, self.b, self.font, self.y = t0, a, t1, b, font, y; self.brk = None; self._c = {}
    def draw(self, canvas, t):
        if t < self.t0 - 0.05: return
        k = min(max((t - self.t1) / 0.5, 0), 1); k = 1 - (1 - k) ** 3; v = round(self.a + (self.b - self.a) * k)
        col = RED if t >= self.t1 + 0.5 else WHITE
        key = (v, col)
        if key not in self._c: self._c[key] = Item(self.t0, str(v), self.font, col, self.y)
        it = self._c[key]; it.t0 = self.t0 if t < self.t1 else -99; it.draw(canvas, t)
class Flag(Item):
    def __init__(self, t0, which, cx, cy, h=230):
        self.t0 = t0; self.brk = None; self.which = which; self.cx = cx; self.cy = cy; self.h = h
    def draw(self, canvas, t):
        u = t - self.t0 + 0.05
        if u < 0: return
        base = (_flags.us if self.which == 'us' else _flags.cn)(self.h)
        sp = _flags.wave(base, 10, t * 5 + (0 if self.which == 'us' else 1))
        sh = Image.new('RGBA', (sp.width + 40, sp.height + 40), (0, 0, 0, 0)); m = sp.getchannel('A').point(lambda v: int(v * 0.55))
        sh.paste(Image.new('RGBA', sp.size, (0, 0, 0, 255)), (24, 30), m); sh = sh.filter(ImageFilter.GaussianBlur(10)); sh.alpha_composite(sp, (20, 20))
        if u < 0.133:
            k = u / 0.133; s = 0.8 + 0.26 * min(k / 0.6, 1) if k < 0.6 else 1.06 - 0.06 * (k - 0.6) / 0.4
            sh = sh.resize((max(1, int(sh.width * s)), max(1, int(sh.height * s))), Image.BILINEAR)
        canvas.alpha_composite(sh, (int(self.cx - sh.width / 2), int(self.cy - sh.height / 2)))
class Clip(Item):
    def __init__(self, t0, spr, cx, cy, rot=0):
        self.t0 = t0; self.brk = None; self.spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True); self.cx = cx; self.cy = cy

# ---------- the timeline (cut time, seconds) ----------
A = lambda n: ANTON(n); SF = lambda n: SOFT(n)
SCENES = []   # (start, end, kind, back_items, front_items)
def behind(a, b, *args, **kw):
    if kw.get('auto'): kw.pop('auto'); args = list(args); args[5] = 'auto'; kw['span'] = (a, b)
    bk, fr = behind_set(*args, **kw); SCENES.append((a, b, 'behind', bk, fr))
def card(a, b, items): SCENES.append((a, b, 'card', items, []))
def split(a, b, items, bg=None, panel=None): SCENES.append((a, b, 'split', items, [bg, panel]))
def over(a, b, items): SCENES.append((a, b, 'over', items, []))
BR = {}
def broll_img(name):
    if name not in BR:
        im = Image.open(f'{V}/broll/{name}.png').convert('L'); a = np.asarray(im, np.float32) / 255
        a = np.clip(0.5 + (a - 0.5) * 1.2, 0, 1) * 0.92 + 0.03; BR[name] = Image.fromarray((a * 255).astype(np.uint8)).convert('RGBA').resize((1080 + 120, int(1344 * 1200 / 752)), Image.LANCZOS)
    return BR[name]
def broll_frame(name, t, a, b, h=H):
    if callable(name): return name(t, a, b, h)
    im = broll_img(name); k = (t - a) / max(b - a, 0.1); s = 1 + 0.08 * k     # slow push-in
    w2, h2 = int(im.width * s), int(im.height * s); z = im.resize((w2, h2), Image.BILINEAR)
    x0 = (w2 - W) // 2; y0 = max(0, (h2 - h) // 2); fr = z.crop((x0, y0, x0 + W, y0 + h))
    return fr
import flags as _flags
def broll(a, b, name, items=()): SCENES.append((a, b, 'broll', list(items), [name]))

exec(open(os.environ['REEL_BEATS']).read())             # the per-video beat list (see reference/outage_beats.py)

for _sc in SCENES:
    for _it in _sc[3]:
        if getattr(_it, 'brk', None) and not hasattr(_it, 'pieces'): _it.pieces = []
def scene_at(t):
    for sc in SCENES:
        if sc[0] <= t < sc[1]: return sc
    return None

CAP = ImageFont.truetype(f'{F}/inter-tight/package/files/inter-tight-latin-700-normal.woff', 74)
TRACK = -2.2
def phrases():
    out, cur = [], []
    for k, w in enumerate(WORDS):
        cur.append(k); txt = ' '.join(WORDS[j]['w'].strip() for j in cur)
        nxt_gap = WORDS[k + 1]['s'] - w['e'] if k + 1 < len(WORDS) else 9
        if w['w'].strip()[-1:] in '.?!' or nxt_gap > 0.35 or len(cur) >= 6 or len(txt) >= 28 or (w['w'].strip()[-1:] == ',' and len(cur) >= 3):
            out.append(cur); cur = []
    if cur: out.append(cur)
    merged = []
    for p in out:      # no one-word leftovers: fold them into the phrase before when they belong to it
        if merged and len(p) == 1 and WORDS[p[0]]['s'] - WORDS[merged[-1][-1]]['e'] < 0.35 and len(' '.join(WORDS[j]['w'].strip() for j in merged[-1] + p)) <= 36:
            merged[-1] = merged[-1] + p
        else: merged.append(p)
    return merged
PH = phrases()
def tw(t): return sum(CAP.getlength(c) + TRACK for c in t)
def lines_of(text):
    if tw(text) <= 620: return [text]
    ws = text.split(); best = None
    for i in range(1, len(ws)):
        a, b = ' '.join(ws[:i]), ' '.join(ws[i:]); sc = max(tw(a), tw(b))
        if best is None or sc < best[0]: best = (sc, [a, b])
    return best[1]
_cap = {}
def cap_sprite(text):
    if text in _cap: return _cap[text]
    ls = lines_of(text); lh = 92; w = int(max(tw(l) for l in ls) + 60); h = lh * len(ls) + 50
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i, l in enumerate(ls):
        x = (w - tw(l)) / 2
        for c in l: d.text((x + 2, 20 + i * lh + 5), c, font=CAP, fill=(0, 0, 0, 150)); x += CAP.getlength(c) + TRACK
    spr = lay.filter(ImageFilter.GaussianBlur(8)); d = ImageDraw.Draw(spr)
    for i, l in enumerate(ls):
        x = (w - tw(l)) / 2
        for c in l: d.text((x, 20 + i * lh), c, font=CAP, fill=(255, 255, 255)); x += CAP.getlength(c) + TRACK
    _cap[text] = spr; return spr
def clean(ws):
    t = ' '.join(WORDS[k]['w'].strip() for k in ws).replace(' ,', ',').strip()
    return t.rstrip('.,') if not t.endswith('?') else t
def subtitle(im, t, y):
    cur = None
    for i, c in enumerate(PH):
        start = WORDS[c[0]]['s'] - 0.05
        stop = min(WORDS[c[-1]]['e'] + 0.3, PH[i + 1] and WORDS[PH[i + 1][0]]['s'] - 0.05) if i + 1 < len(PH) else WORDS[c[-1]]['e'] + 0.6
        if start <= t < stop: cur = (c, start); break
    if cur is None: return
    sp = cap_sprite(clean(cur[0])); u = t - cur[1]
    if u < 0.133:      # the whole phrase pops in once: 0.92 -> 1.03 -> 1.0 over 4 frames
        k = u / 0.133; s_ = 0.92 + 0.11 * min(k / 0.6, 1) if k < 0.6 else 1.03 - 0.03 * (k - 0.6) / 0.4
        sp = sp.resize((max(1, int(sp.width * s_)), max(1, int(sp.height * s_))), Image.BILINEAR)
    cy = y + 85 if y > 1000 else y + 40
    im.alpha_composite(sp, (int((W - sp.width) / 2), int(cy - sp.height / 2 + 20)))

def compose(frame, fi, t, tn=None):
    sc = scene_at(t); tn = t if tn is None else tn
    if sc and sc[2] == 'broll':
        im = broll_frame(sc[4][0], t, sc[0], sc[1]).copy()
        for it in sc[3]: it.draw(im, t)
        subtitle(im, tn, 1380)
    elif sc and sc[2] == 'card':
        im = GRAIN[fi % 6].copy()
        for it in sc[3]: it.draw(im, t)
        subtitle(im, tn, 1380)
    else:
        sm = load_mask(fi); g0 = grade(frame, sm, fi); g = g0.copy()
        if sc and sc[2] == 'over':
            for it in sc[3]: it.draw(g, t)
            subtitle(g, tn, 1380); im = g; return im
        if sc and sc[2] == 'behind':
            for it in sc[3]: it.draw(g, t)
            g0.putalpha(cutout(sm)); g.alpha_composite(g0)
            for it in sc[4]: it.draw(g, t)
            subtitle(g, tn, 1380); im = g
        elif sc and sc[2] == 'split':
            im = GRAIN[fi % 6].copy()
            if len(sc[4]) > 1 and sc[4][1]: im.alpha_composite(sc[4][1](t), (0, 0))
            if sc[4][0]:
                bgi = broll_frame(sc[4][0], t, sc[0], sc[1], 960); bgi = Image.blend(bgi, Image.new('RGBA', bgi.size, (0, 0, 0, 255)), 0.6); im.alpha_composite(bgi, (0, 0))
            for it in sc[3]: it.draw(im, t)
            im = im.crop((0, 0, W, 960)); full = Image.new('RGBA', (W, H), INK + (255,)); full.alpha_composite(im, (0, 0))
            full.alpha_composite(g.crop((0, 300, W, 1260)), (0, 960)); ImageDraw.Draw(full).line([(0, 960), (W, 960)], fill=RED, width=4)
            subtitle(full, tn, 880); im = full
        else:
            subtitle(g, tn, 1380); im = g

    return im

def render(t0, t1, out):
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS)); fs = W * H * 3
    src = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-i', SRC, '-t', f'{t1 - t0:.3f}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-ss', f'{t0:.3f}', '-t', f'{t1 - t0:.3f}', '-i', SRC, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium',
                            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        raw = src.stdout.read(fs)
        if len(raw) < fs: break
        fo = tmap.new_to_old_frame(fi); im = compose(Image.frombuffer('RGB', (W, H), raw), fo, fo / FPS, fi / FPS)
        enc.stdin.write(im.convert('RGB').tobytes())
        if fi % 300 == 0: print('frame', fi, flush=True)
    enc.stdin.close(); enc.wait(); src.kill(); print('wrote', out)

if __name__ == '__main__':
    a = float(sys.argv[1]) if len(sys.argv) > 2 else 0; b = float(sys.argv[2])
    render(a, b, sys.argv[3])
