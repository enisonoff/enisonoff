"""SpaceX video v2: full-frame shot, trims, Cleo-style full-screen space cutaways with camera moves + twinkling stars,
captions re-drawn only during cutaways (her burned-in captions are hidden there).
usage: python3 render2.py sb | preview | render
"""
import sys, subprocess, json, random, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = '/tmp/claude-0/-home-user-enisonoff/672c1244-cc8a-569f-a9ee-237151e2864a/scratchpad'
V = S + '/v13'
W, H, FPS = 1080, 1920, 30
MF = lambda w, s: ImageFont.truetype(f'{S}/fonts/montserrat/package/files/montserrat-latin-{w}-normal.woff', s)
KEEP = [(0.0, 173.73)]
DUR = sum(b - a for a, b in KEEP)
def out_to_src(t):
    for a, b in KEEP:
        if t < b - a: return a + t
        t -= b - a
    return KEEP[-1][1]
def src_to_out(t):
    o = 0
    for a, b in KEEP:
        if a <= t <= b: return o + t - a
        o += b - a

# ---------- the space plate: 1200x900 -> big canvas for camera moves ----------
SP = Image.open(V + '/img/space.jpg').convert('RGB')
PLATE = SP.resize((int(SP.width * 2600 / SP.height), 2600), Image.LANCZOS)   # 3467 x 2600
PW, PH = PLATE.size
rnd = random.Random(7)
STARS = [(rnd.uniform(0, 1), rnd.uniform(0, 1), rnd.uniform(1.5, 3.5), rnd.uniform(0, 6.28), rnd.uniform(1.5, 3.5)) for _ in range(140)]

def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)

# camera moves: (cx, cy as fraction of plate, zoom where 1 = window height fills plate height)
MOVES = {
    'A': ((0.22, 0.42, 1.45), (0.63, 0.50, 1.05)),   # station -> earth, gentle pan
    'B': ((0.62, 0.50, 1.00), (0.64, 0.48, 1.55)),   # push into earth
    'B2': ((0.45, 0.32, 1.7), (0.66, 0.46, 2.4)),   # sweep across the satellite web
    'C': ((0.78, 0.36, 2.6), (0.66, 0.44, 1.9)),     # tight on the satellite lattice
    'D': ((0.62, 0.50, 1.5), (0.55, 0.50, 0.98)),    # pull back to wide
}
STATIC = {'B': (0.64, 0.48, 1.35), 'B2': (0.60, 0.42, 2.0), 'C': (0.22, 0.42, 1.55)}
def crop(cx, cy, z):
    wh = PH / z; ww = wh * W / H
    cxp = min(max(cx * PW, ww / 2), PW - ww / 2); cyp = min(max(cy * PH, wh / 2), PH - wh / 2)
    return PLATE.resize((W, H), Image.LANCZOS, box=(cxp - ww / 2, cyp - wh / 2, cxp + ww / 2, cyp + wh / 2))
_static = {}
# full-picture layout for the starship shots: the whole render across the frame, feathered into a star field
FY = 520; FIT = SP.resize((W, int(SP.height * W / SP.width)), Image.LANCZOS)
_m = Image.new('L', FIT.size, 255); _md = ImageDraw.Draw(_m)
for i in range(90): _md.rectangle((0, i, W, i), fill=int(255 * i / 90)); _md.rectangle((0, FIT.height - 1 - i, W, FIT.height - 1 - i), fill=int(255 * i / 90))
WIDE = Image.new('RGB', (W, H), (4, 7, 20)); _wd = ImageDraw.Draw(WIDE)
for _ in range(260):
    x, y, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0.6, 1.8); c = int(rnd.uniform(120, 255)); _wd.ellipse((x - r, y - r, x + r, y + r), fill=(c, c, c))
WIDE.paste(FIT, (0, FY), _m)
def ship_sprite():
    w, h = 40, 230; im = Image.new('RGBA', (w + 40, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im); ox = 20
    for x in range(w):                                     # stainless body with a soft highlight
        v = int(150 + 95 * math.sin(math.pi * (x + 4) / (w + 8)) ** 2); d.line((ox + x, 60, ox + x, h), fill=(v, v, v + 8))
    d.polygon([(ox, 62), (ox + w / 2, 0), (ox + w, 62)], fill=(215, 215, 222)); d.chord((ox, 22, ox + w, 102), 180, 360, fill=(215, 215, 222))
    d.rectangle((ox, 60, ox + 12, h), fill=(40, 40, 46))     # heat-shield side
    d.polygon([(ox, 70), (ox - 16, 96), (ox, 104)], fill=(70, 70, 76)); d.polygon([(ox + w, 70), (ox + w + 16, 96), (ox + w, 104)], fill=(70, 70, 76))
    d.polygon([(ox, h - 50), (ox - 20, h - 8), (ox, h - 8)], fill=(70, 70, 76)); d.polygon([(ox + w, h - 50), (ox + w + 20, h - 8), (ox + w, h - 8)], fill=(70, 70, 76))
    return im
SHIP = ship_sprite()
def flame(n_len, t):
    L = int(n_len * (0.85 + 0.15 * math.sin(t * 40))); im = Image.new('RGBA', (90, L + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(10, 0, -1):
        a = int(255 * (11 - k) / 11); ww = 6 + k * 4; d.ellipse((45 - ww / 2, 0, 45 + ww / 2, L * k / 10 + 10), fill=(255, 150 + k * 9, 60 + k * 15, a // 2))
    d.ellipse((38, 0, 52, L * 0.35), fill=(255, 250, 230, 255)); return im.filter(ImageFilter.GaussianBlur(2))
def bezier(p0, p1, p2, p3, u):
    v = 1 - u; return tuple(v ** 3 * a + 3 * v * v * u * b + 3 * v * u * u * c + u ** 3 * d for a, b, c, d in zip(p0, p1, p2, p3))
PATHS = {'A': ((640, FY + 290), (560, FY - 120), (300, FY - 40), (205, FY + 300)),     # earth -> the station
         'D': ((640, FY + 290), (620, FY - 100), (560, FY - 400), (520, -400))}       # earth -> straight up and out
def ship_frame(move, p, t):
    im = WIDE.copy().convert('RGBA'); P = PATHS[move]
    u = (min(max((p - 0.05) / 0.85, 0), 1)) ** 1.6                               # slow lift-off, then accelerates
    if move == 'A': u = min(u, 1.0)
    trail = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(trail)
    pts = [bezier(*P, max(0, u - k * 0.01)) for k in range(40)]
    for k in range(len(pts) - 1): td.line((pts[k], pts[k + 1]), fill=(255, 200, 140, int(150 * (1 - k / 40))), width=max(1, int(8 * (1 - k / 40))))
    im.alpha_composite(trail.filter(ImageFilter.GaussianBlur(3)))
    x, y = bezier(*P, u); x2, y2 = bezier(*P, min(1, u + 0.01)); ang = math.degrees(math.atan2(x2 - x, -(y2 - y))) if (x2, y2) != (x, y) else 0
    sc = 1.25 - 0.55 * u if move == 'A' else 1.25 + 0.3 * u
    sp = SHIP.resize((int(SHIP.width * sc), int(SHIP.height * sc)), Image.LANCZOS); fl = flame(int(120 * sc), t); fl = fl.resize((int(fl.width * sc), int(fl.height * sc)))
    combo = Image.new('RGBA', (sp.width, sp.height + fl.height), (0, 0, 0, 0)); combo.alpha_composite(fl, ((sp.width - fl.width) // 2, sp.height - int(8 * sc))); combo.alpha_composite(sp, (0, 0))
    combo = combo.rotate(-ang, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(combo, (int(x - combo.width / 2), int(y - combo.height / 2)))
    return im.convert('RGB')
def space_frame(move, p, t=0):
    if move in ('A', 'D'): return ship_frame(move, p, t)
    if move not in _static: _static[move] = crop(*STATIC[move])
    return _static[move].copy()

# ---------- A: camera flies from earth to the data center, riding a beam of light ----------
A0, A1 = 5.54, 10.07
EP, SPT = (0.565, 0.47), (0.17, 0.40)          # beam start on earth / the station, as plate fractions
def cam_at(q):
    """q = seconds into the shot -> (cx, cy, zoom)"""
    hold, fly = 0.45, 1.15
    if q < hold: return (0.60, 0.50, 1.35)
    k = min((q - hold) / fly, 1); e = k * k * (3 - 2 * k)
    cx = 0.60 + (SPT[0] + 0.02 - 0.60) * e; cy = 0.50 + (SPT[1] + 0.02 - 0.50) * e
    z = 1.35 + 0.65 * e + 0.25 * math.sin(math.pi * e)      # a little extra zoom mid-flight for speed
    if q > hold + fly: z += 0.06 * min((q - hold - fly) / 2.5, 1)   # tiny settle drift after arrival
    return cx, cy, z
def plate_to_screen(px, py, cam):
    cx, cy, z = cam; wh = PH / z; ww = wh * W / H
    cxp = min(max(cx * PW, ww / 2), PW - ww / 2); cyp = min(max(cy * PH, wh / 2), PH - wh / 2)
    return ((px * PW - (cxp - ww / 2)) * W / ww, (py * PH - (cyp - wh / 2)) * H / wh)
def a_single(q, t):
    cam = cam_at(q); im = crop(*cam).convert('RGBA')
    head = min(max((q - 0.15) / 1.25, 0), 1); head = 1 - (1 - head) ** 2      # beam shoots out, slightly ahead of the camera
    x0, y0 = plate_to_screen(*EP, cam); x1, y1 = plate_to_screen(EP[0] + (SPT[0] - EP[0]) * head, EP[1] + (SPT[1] - EP[1]) * head, cam)
    beam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(beam)
    if head > 0:
        for wdt, a in [(60, 40), (30, 90), (12, 200), (4, 255)]: bd.line((x0, y0, x1, y1), fill=(140, 215, 255, a), width=wdt)
        beam = beam.filter(ImageFilter.GaussianBlur(5)); bd = ImageDraw.Draw(beam)
        bd.line((x0, y0, x1, y1), fill=(235, 250, 255, 255), width=3)
        o = orb(22, t); beam.alpha_composite(o, (int(x1 - o.width / 2), int(y1 - o.height / 2)))
    im.alpha_composite(beam)
    if head >= 1:                                        # the data center lights up when the beam lands
        arr = q - 1.4; sx, sy = plate_to_screen(*SPT, cam); ring = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(ring)
        for j in range(3):
            rr = 50 + (arr - j * 0.3) * 420
            if rr > 50: rd.ellipse((sx - rr, sy - rr, sx + rr, sy + rr), outline=(140, 215, 255, max(0, int(220 - rr * 0.35))), width=6)
        im.alpha_composite(ring)
    return im.convert('RGB')
def a_frame(t):
    q = t - A0
    if 0.45 < q < 1.6:                                   # motion blur while flying: blend sub-frames
        fr = [a_single(q - k * 0.012, t) for k in range(4)]
        out = fr[0]
        for i, f in enumerate(fr[1:], 2): out = Image.blend(out, f, 1 / i)
        return out
    return a_single(q, t)

# ---------- E: chatbot question -> ball of energy -> space data center ----------
E0, E1 = 64.88, 75.53
Q = 'what should i have for dinner?'
T_TYPE0, T_TYPE1, T_SEND, T_ORB, T_SPACE, T_ARRIVE = 64.95, 67.1, 67.35, 67.95, 68.9, 72.8
def orb(r, t, glow=1.0):
    S_ = int(r * 6); im = Image.new('RGBA', (S_, S_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = S_ / 2
    for k in range(24, 0, -1):
        rr = r * (0.35 + 2.6 * k / 24) * (1 + 0.06 * math.sin(t * 23 + k)); a = int(255 * glow * (1 - k / 25) ** 2.2)
        d.ellipse((c - rr, c - rr, c + rr, c + rr), fill=(90, 200, 255, a))
    d.ellipse((c - r * 0.55, c - r * 0.55, c + r * 0.55, c + r * 0.55), fill=(240, 252, 255, 255))
    return im.filter(ImageFilter.GaussianBlur(max(1, r / 8)))
def chat_ui(t):
    im = Image.new('RGBA', (W, H), (15, 16, 21, 255)); d = ImageDraw.Draw(im)
    d.text((W / 2 - d.textlength('new chat', font=MF(700, 34)) / 2, 300), 'new chat', font=MF(700, 34), fill=(150, 150, 160))
    if t < T_SEND: d.text((W / 2 - d.textlength('how can i help?', font=MF(700, 60)) / 2, 640), 'how can i help?', font=MF(700, 60), fill=(230, 230, 236))
    # input box
    d.rounded_rectangle((70, 1150, W - 70, 1270), 60, fill=(32, 34, 42), outline=(60, 62, 74), width=2)
    n = int(len(Q) * min(max((t - T_TYPE0) / (T_TYPE1 - T_TYPE0), 0), 1)) if t < T_SEND else 0
    typed = Q[:n]; f = MF(500, 44); d.text((120, 1184), typed, font=f, fill=(235, 235, 240))
    if t < T_SEND and int(t * 3) % 2 == 0: cx_ = 122 + d.textlength(typed, font=f); d.line((cx_, 1186, cx_, 1236), fill=(235, 235, 240), width=3)
    pressed = T_SEND - 0.12 <= t < T_SEND + 0.08
    d.ellipse((W - 170, 1170, W - 90, 1250), fill=(255, 255, 255) if n else (70, 72, 84)); d.polygon([(W - 130, 1188), (W - 148, 1214), (W - 112, 1214)], fill=(15, 16, 21))
    if pressed: d.ellipse((W - 176, 1164, W - 84, 1256), outline=(90, 200, 255), width=4)
    return im
def e_frame(t):
    if t < T_SPACE:
        im = chat_ui(t)
        if t >= T_SEND:
            f = MF(600, 40); d0 = ImageDraw.Draw(im); tw = d0.textlength(Q, font=f)
            k = ease((t - T_SEND) / 0.4); m = ease((t - T_ORB) / 0.7)     # bubble floats up, then collapses into an orb
            bx1 = W - 80; bw = (tw + 70) * (1 - m) + 70 * m; bh = 100 * (1 - m) + 70 * m; by = 1150 - 260 * k - 200 * m
            cxb = bx1 - bw / 2 * (1 - m) - (bx1 - W / 2) * m
            layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
            col = (int(40 + 50 * m), int(70 + 130 * m), int(220 + 35 * m), 255)
            ld.rounded_rectangle((cxb - bw / 2, by - bh / 2, cxb + bw / 2, by + bh / 2), int(bh / 2), fill=col)
            if m < 0.6: ld.text((cxb - tw / 2, by - 24), Q, font=f, fill=(255, 255, 255, int(255 * (1 - m / 0.6))))
            im.alpha_composite(layer)
            if m > 0.3:
                o = orb(40 + 30 * m, t, glow=(m - 0.3) / 0.7); im.alpha_composite(o, (int(cxb - o.width / 2), int(by - o.height / 2)))
        return im.convert('RGB')
    # space: the orb rises from earth to the station
    im = WIDE.copy().convert('RGBA'); P = ((600, FY + 300), (560, FY - 160), (280, FY - 60), (170, FY + 300))
    u = ease((t - T_SPACE) / (T_ARRIVE - T_SPACE))
    trail = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(trail)
    pts = [bezier(*P, max(0, u - k * 0.012)) for k in range(30)]
    for k in range(len(pts) - 1): td.line((pts[k], pts[k + 1]), fill=(120, 210, 255, int(170 * (1 - k / 30))), width=max(1, int(12 * (1 - k / 30))))
    im.alpha_composite(trail.filter(ImageFilter.GaussianBlur(4)))
    if t < T_ARRIVE + 0.2:
        x, y = bezier(*P, u); o = orb(26 - 8 * u, t); im.alpha_composite(o, (int(x - o.width / 2), int(y - o.height / 2)))
    if t >= T_ARRIVE:                                     # the data center lights up
        q = (t - T_ARRIVE); ring = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(ring); cx_, cy_ = 170, FY + 300
        for j in range(3):
            rr = 40 + (q - j * 0.35) * 260
            if rr > 40: rd.ellipse((cx_ - rr, cy_ - rr, cx_ + rr, cy_ + rr), outline=(120, 210, 255, max(0, int(200 - rr * 0.6))), width=5)
        glow = orb(70, t, glow=max(0.25, 1 - q * 0.5)); ring.alpha_composite(glow, (int(cx_ - glow.width / 2), int(cy_ - glow.height / 2)))
        im.alpha_composite(ring)
    return im.convert('RGB')

# ---------- G: the guarantee umbrella (procedural motion graphic) ----------
GREEN = (118, 185, 0)
_nv = Image.open(S + '/logos/nvidia.png').convert('RGBA'); _nv = _nv.crop(_nv.getbbox())
NVW = Image.new('RGBA', _nv.size, (255, 255, 255, 255)); NVW.putalpha(_nv.split()[3]); NVW = NVW.resize((150, int(150 * _nv.height / _nv.width)), Image.LANCZOS)
G0, G1 = 110.2, 116.15
DROPS = [(rnd.uniform(140, 940), rnd.uniform(G0 - 1.5, G1), rnd.uniform(650, 900)) for _ in range(170)]
def lerp(a, b, x): return int(round(a + (b - a) * min(max(x, 0), 1)))
def g_frame(t):
    im = Image.new('RGB', (W, H), (8, 10, 22)); d = ImageDraw.Draw(im, 'RGBA')
    for k in range(0, H, 6): d.line((0, k, W, k), fill=(20, 24, 52, int(90 * (1 - k / H))))
    cx, top = W / 2, 720
    u = ease((t - G0) / 0.8) * (1 - 0.88 * ease((t - 118.4) / 0.9))      # open, then fold shut
    R = 400 * u + 30; Hc = 230 * (0.35 + 0.65 * u)
    # who's under the umbrella: openai's ohio campus ($105B) and other ai data centers ($13B)
    oa = Image.open(S + '/logos/openai_full.png').convert('RGBA'); oa = oa.resize((300, int(300 * oa.height / oa.width)), Image.LANCZOS)
    im.paste(oa, (int(390 - oa.width / 2), int(1185 - oa.height / 2)), oa)
    def ctr(txt, x, y, f, col): d.text((x - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=col)
    ctr('ohio campus · $105B', 390, 1268, MF(600, 28), (190, 190, 200))
    x = 730; y = 1120
    for j in range(2):
        xx = x + j * 80; d.rounded_rectangle((xx, y, xx + 64, y + 100), 8, outline=(235, 235, 240), width=4)
        for k in range(3): d.line((xx + 12, y + 22 + k * 26, xx + 52, y + 22 + k * 26), fill=(235, 235, 240), width=3)
    ctr('other ai data', 800, 1240, MF(800, 30), (255, 255, 255)); ctr('centers · $13B', 800, 1284, MF(600, 26), (190, 190, 200))
    # rain of bills
    for x0, t0, v in DROPS:
        if t < t0: continue
        y = 540 + (t - t0) * v
        canopy_y = top + Hc * (1 - ((x0 - cx) / R) ** 2) if abs(x0 - cx) < R else None
        if canopy_y is not None and y >= canopy_y - 10:
            a = int(255 * max(0, 1 - (y - canopy_y) / 60))
            if a > 0: d.text((x0 - 10, canopy_y - 50 - (y - canopy_y) * 0.6), '$', font=MF(800, 48), fill=(255, 220, 90, a))
            continue
        if y > 1100: continue
        d.text((x0 - 10, y), '$', font=MF(800, 48), fill=(255, 220, 90, 230))
    # umbrella: canopy, scallops, handle
    pts = [(cx + R * math.cos(a_), top + Hc - Hc * math.sin(a_) - Hc * 0) for a_ in [math.pi * i / 40 for i in range(41)]]
    pts = [(x, top + Hc - (top + Hc - y)) for x, y in pts]
    canopy = [(cx + R * math.cos(math.pi * i / 40), top + Hc * (1 - math.sin(math.pi * i / 40)) ) for i in range(41)]
    d.polygon(canopy + [(cx - R, top + Hc), (cx + R, top + Hc)], fill=GREEN)
    for i in range(4):
        x0_ = cx - R + i * R / 2; d.ellipse((x0_, top + Hc - 26, x0_ + R / 2, top + Hc + 26), fill=(8, 10, 22))
    d.line((cx, top + Hc - 10, cx, 1110), fill=(220, 220, 225), width=10); d.arc((cx - 60, 1060, cx + 4, 1124), 0, 180, fill=(220, 220, 225), width=10)
    d.line((cx, top - 30, cx, top + 4), fill=(220, 220, 225), width=8)
    if u > 0.5: im.paste(NVW, (int(cx - NVW.width / 2), int(top + Hc * 0.42 - NVW.height / 2)), NVW)
    # headline text
    def center(txt, y, f, col): d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=col)
    if t < 112.6:
        center('GUARANTEE =', 300, MF(800, 46), (190, 190, 200)); center('"we got you covered"', 370, MF(800, 70), GREEN)
    else:
        v = 118 * ease((t - 112.6) / 0.9); center(f'${v:.0f}B', 290, MF(800, 150), GREEN); center('in guarantees', 470, MF(700, 44), (230, 230, 235))
    return im

# ---------- H: the $44B rack (her data center image + a GPU rack that stacks up) ----------
DC = Image.open(V + '/img/dc.webp').convert('RGB'); DC = DC.resize((int(DC.width * 2200 / DC.height), 2200), Image.LANCZOS)
H0, H1 = 16.68, 19.98
NU, UH, RW = 20, 36, 440; RBASE = 1330
def h_frame(t):
    p = (t - H0) / (H1 - H0); z = 1.0 + 0.12 * p
    wh = DC.height / z; ww = wh * W / H; cx = DC.width * 0.42; cy = DC.height * 0.5
    im = DC.resize((W, H), Image.BILINEAR, box=(cx - ww / 2, cy - wh / 2, cx + ww / 2, cy + wh / 2))
    im = Image.blend(im, Image.new('RGB', (W, H), (4, 6, 16)), 0.55).convert('RGBA')
    d = ImageDraw.Draw(im, 'RGBA'); x0 = (W - RW) / 2
    grow = (t - H0) / 0.55                                     # units fly in over ~0.75 s
    shown = []
    for k in range(NU):
        tk = k / NU; a = ease((grow - tk) / 0.12)
        if a <= 0: continue
        y = RBASE - (k + 1) * UH + (1 - a) * 80; shown.append(y)
        d.rectangle((x0 + 14, y + 2, x0 + RW - 14, y + UH - 3), fill=(26, 28, 34, int(255 * a)))
        d.line((x0 + 30, y + UH / 2, x0 + 150, y + UH / 2), fill=(118, 185, 0, int(255 * a)), width=4)
        for j in range(6):
            on = math.sin(t * 9 + k * 1.7 + j) > -0.2
            d.ellipse((x0 + 190 + j * 34, y + UH / 2 - 5, x0 + 200 + j * 34, y + UH / 2 + 5), fill=(80, 170, 255, int((255 if on else 70) * a)))
    if shown:
        top = min(min(shown), RBASE - UH); d.rectangle((x0, top - 10, x0 + RW, RBASE + 10), outline=(150, 155, 170, 255), width=6)
    # the pop
    pp = (t - 17.32) / 0.35
    if pp > 0:
        sc = 0.3 + 0.95 * ease(min(pp, 1)) - 0.25 * max(0, min(pp - 1, 1)) if pp < 2 else 1.0
        sc = min(max(sc, 0.3), 1.25) if pp < 2 else 1.0
        f = MF(800, max(10, int(170 * sc))); txt = '$44B'; tw = d.textlength(txt, font=f)
        for r_, al in [(18, 40), (9, 70)]: d.text(((W - tw) / 2, 270 - r_ / 3), txt, font=f, fill=(118, 185, 0, al))
        d.text(((W - tw) / 2, 270), txt, font=f, fill=(118, 185, 0, 255))
    def sub(txt, t0, y, col=(255, 255, 255)):
        q = (t - t0) / 0.18
        if q > 0:
            sc = 1.0 + 0.25 * max(0, 1 - q) if q < 1 else 1.0; a = min(1, q * 2)
            f = MF(800, int(44 * sc)); tw = d.textlength(txt, font=f); d.text(((W - tw) / 2, y - (sc - 1) * 20), txt, font=f, fill=col + (int(255 * a),))
    sub('in debt for spacex', 18.4, 470)
    return im.convert('RGB')

# cutaways in source time
CUTS = [(A0, A1, 'A'), (H0, H1, 'H'), (E0, E1, 'E'), (84.44, 88.13, 'C'), (G0, G1, 'G')]
WORDS = json.load(open(V + '/words.json'))

CHUNKS = []
_cur = []
for w in WORDS:
    _cur.append(w)
    if len(_cur) == 3 or w['w'][-1:] in '.,?!': CHUNKS.append(_cur); _cur = []
if _cur: CHUNKS.append(_cur)

def caption(im, t, a, b):
    """re-draw captions during cutaways in her style: white caps, longest word yellow; only words inside the cutaway"""
    ch = None
    for k, c in enumerate(CHUNKS):
        nxt = CHUNKS[k + 1][0]['s'] if k + 1 < len(CHUNKS) else 1e9
        if c[0]['s'] <= t < nxt: ch = c; break
    if ch is None: return im
    ch = [w for w in ch if a - 0.15 <= w['s'] < b]
    if not ch: return im
    words = [w['w'].upper().strip(',.?!') for w in ch]
    hi = max(range(len(words)), key=lambda k: len(words[k]))
    d = ImageDraw.Draw(im); f = MF(800, 52); sp = d.textlength(' ', font=f)
    tw = sum(d.textlength(w, font=f) for w in words) + sp * (len(words) - 1); x = (W - tw) / 2; y = 1410
    for k, w in enumerate(words):
        for dx, dy in [(0, 4), (2, 3), (-2, 3)]: d.text((x + dx, y + dy), w, font=f, fill=(0, 0, 0))
        d.text((x, y), w, font=f, fill=(255, 232, 0) if k == hi else (255, 255, 255)); x += d.textlength(w, font=f) + sp
    return im

def punch(im, z, dx=0, dy=0):
    if z <= 1.001 and not dx and not dy: return im
    ww, hh = W / z, H / z; x0 = min(max((W - ww) / 2 - dx, 0), W - ww); y0 = min(max((H - hh) / 2 - dy, 0), H - hh)
    return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + ww, y0 + hh))

def compose(frame, t):
    for a, b, mv in CUTS:
        if a <= t < b:
            base = a_frame(t) if mv == 'A' else e_frame(t) if mv == 'E' else g_frame(t) if mv == 'G' else h_frame(t) if mv == 'H' else space_frame(mv, (t - a) / (b - a), t)
            return caption(base, t, a, b)
    return frame

def grab(t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', V + '/raw.mp4', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombuffer('RGB', (W, H), raw).copy()

def run(outfile, keep):
    # keep each frame's real timestamp (the phone footage is variable frame rate): trim per segment, then resample to a steady 30 fps
    vc = ''.join(f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps={FPS}[v{i}];' for i, (a, b) in enumerate(keep)) + ''.join(f'[v{i}]' for i in range(len(keep))) + f'concat=n={len(keep)}:v=1:a=0[vout]'
    src = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', V + '/raw.mp4', '-filter_complex', vc, '-map', '[vout]', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    af = ''.join(f'[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];' for i, (a, b) in enumerate(keep)) + ''.join(f'[a{i}]' for i in range(len(keep))) + f'concat=n={len(keep)}:v=0:a=1[aout]'
    out = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', V + '/raw.mp4',
                            '-filter_complex', af, '-map', '0:v', '-map', '[aout]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '192k', '-shortest', outfile], stdin=subprocess.PIPE)
    dur = sum(b - a for a, b in keep); n = int(dur * FPS); i = 0
    def o2s(t):
        for a, b in keep:
            if t < b - a: return a + t
            t -= b - a
        return keep[-1][1]
    while True:
        b = src.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        out.stdin.write(compose(Image.frombuffer('RGB', (W, H), b), o2s(i / FPS)).tobytes()); i += 1
        if i % 300 == 0: print(f'{100 * i / n:.0f}%', flush=True)
    out.stdin.close(); out.wait(); print('done', outfile, i)

mode = sys.argv[1]
if mode == 'sb':
    tiles = []
    for a, b, mv in CUTS:
        for p in (0.05, 0.5, 0.95):
            t = a + (b - a) * p; fr = compose(grab(t), t); d = ImageDraw.Draw(fr)
            o = src_to_out(t); d.text((30, 1760), f'{int(o // 60)}:{o % 60:04.1f}  shot {mv}', font=MF(800, 56), fill=(255, 255, 0))
            tiles.append(fr.resize((270, 480), Image.LANCZOS))
    sh = Image.new('RGB', (6 * 280 + 10, 2 * 490 + 10), (20, 20, 20))
    for i, im in enumerate(tiles): sh.paste(im, (10 + (i % 6) * 280, 10 + (i // 6) * 490))
    sh.save(V + '/storyboard2.png'); print('ok')
elif mode == 'preview':
    run(V + '/preview-opening.mp4', [(0.0, 14.5)])
elif mode == 'aclip':
    run(V + '/clip-A.mp4', [(3.8, 11.0)])
elif mode == 'allprev':
    run(V + '/preview-cuts.mp4', [(3.0, 22.0), (62.0, 77.0), (83.0, 89.0), (107.0, 118.0), (166.0, 173.73)])
elif mode == 'hprev':
    run(V + '/preview-44b.mp4', [(13.5, 28.0)])
elif mode == 'gprev':
    run(V + '/preview-guarantee.mp4', [(107.0, 123.0)])
else:
    run(V + '/spacex-v2.mp4', KEEP)
