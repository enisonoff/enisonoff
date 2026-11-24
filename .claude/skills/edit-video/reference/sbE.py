import sys
sys.argv = ['x', 'none']
exec(open('/tmp/claude-0/-home-user-enisonoff/672c1244-cc8a-569f-a9ee-237151e2864a/scratchpad/v14/renderD.py').read().split("if sys.argv[1] == 'audit'")[0])
MASKC = {}
def her_mask(t):
    k = f'{t}'
    if k not in MASKC: MASKC[k] = Image.open(f'{V}/bm_{t}.png').convert('L').filter(ImageFilter.GaussianBlur(1.5))
    return MASKC[k]
def cutout(path, h):
    c = Image.open(path).convert('RGBA'); c = c.crop(c.getbbox()); return c.resize((max(1, int(c.width * h / c.height)), h), Image.LANCZOS)
def circle_face(path, d=150, focus=0.35):
    import numpy as np
    c = Image.open(path).convert('RGBA'); c = c.crop(c.getbbox()); al = np.array(c.split()[3]) > 100
    widths = al.sum(1); rows = np.where(widths > 0)[0]; top = rows[0]
    # neck = narrowest row between 35% and 75% of the cutout height (head sits above it)
    lo, hi = int(c.height * 0.35), int(c.height * 0.75); neck = lo + int(np.argmin(widths[lo:hi] + (widths[lo:hi] == 0) * 10 ** 6))
    cols = np.where(al[top:neck].any(0))[0]; hx0, hx1 = cols[0], cols[-1]
    hcx, hcy = (hx0 + hx1) / 2, (top + neck) / 2; side = int(max(neck - top, hx1 - hx0) * 1.6); hcy += side * 0.06
    bg = Image.new('RGBA', (c.width + 2 * side, c.height + 2 * side), (238, 238, 242, 255)); bg.alpha_composite(c, (side, side))
    sq = bg.crop((int(hcx + side - side / 2), int(hcy + side - side / 2), int(hcx + side + side / 2), int(hcy + side + side / 2)))
    sq = sq.resize((d, d), Image.LANCZOS); m = Image.new('L', (d, d), 0); ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
    out = Image.new('RGBA', (d + 12, d + 12), (0, 0, 0, 0)); ImageDraw.Draw(out).ellipse((0, 0, d + 11, d + 11), fill=(255, 255, 255, 255)); out.paste(sq, (6, 6), m); return out
def word_chip(txt, d=150, bg=(30, 30, 36), fg=(255, 255, 255), size=30):
    out = Image.new('RGBA', (d + 12, d + 12), (0, 0, 0, 0)); dd = ImageDraw.Draw(out); dd.ellipse((0, 0, d + 11, d + 11), fill=(255, 255, 255, 255)); dd.ellipse((6, 6, d + 5, d + 5), fill=bg)
    f = MONT(800, size); lines = txt.split('\n'); y = (d + 12 - len(lines) * (size + 4)) / 2
    for ln in lines: dd.text(((d + 12 - dd.textlength(ln, font=f)) / 2, y), ln, font=f, fill=fg); y += size + 4
    return out
def icon_chip(g, d=150):
    out = Image.new('RGBA', (d + 12, d + 12), (0, 0, 0, 0)); dd = ImageDraw.Draw(out); dd.ellipse((0, 0, d + 11, d + 11), fill=(255, 255, 255, 255)); dd.ellipse((6, 6, d + 5, d + 5), fill=(120, 80, 30))
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 92); bb = dd.textbbox((0, 0), g, font=f); dd.text(((d + 12 - bb[2] - bb[0]) / 2, (d + 12 - bb[3] - bb[1]) / 2), g, font=f, fill=(255, 225, 140)); return out
def logo_chip(path, d=150):
    out = Image.new('RGBA', (d + 12, d + 12), (0, 0, 0, 0)); dd = ImageDraw.Draw(out); dd.ellipse((0, 0, d + 11, d + 11), fill=(255, 255, 255, 255)); dd.ellipse((6, 6, d + 5, d + 5), fill=(20, 20, 24))
    lg = Image.open(path).convert('RGBA'); lg = lg.crop(lg.getbbox()); lg.thumbnail((int(d * 0.62), int(d * 0.62)), Image.LANCZOS); out.alpha_composite(lg, ((d + 12 - lg.width) // 2, (d + 12 - lg.height) // 2)); return out
CH_ = {
 'jensen': lambda: circle_face(V + '/jensen_head.png'), 'nvidia staff': lambda: logo_chip(S + '/logos/nvidia.png'), 'ai stocks': lambda: word_chip('AI\nstocks', size=32),
 'lawyers': lambda: icon_chip('⚖'), 'the board': lambda: circle_face(V + '/jones_cut.png'), 'kress': lambda: circle_face(V + '/kress_cut.png'),
 'bessent': lambda: circle_face(V + '/bessent_cut.png'), 'women': lambda: word_chip('women', size=30, bg=(200, 30, 140)), 'nvidia': lambda: logo_chip(S + '/logos/nvidia.png'),
 'trump': lambda: circle_face(V + '/trump_cut.png'), 'democrats': lambda: word_chip('dems', size=34, bg=(30, 70, 200)),
}
LABEL = {'nvidia staff': 'staff', 'the board': 'the board', 'nvidia': 'nvidia'}
def venn_faces(winners, losers, middle, header=None):
    im = venn_clear([], [], None if middle is None else []); d = ImageDraw.Draw(im)
    if middle: d.rectangle((0, 1050, W, 1260), fill=(250, 250, 248))
    cy, r = 720, 300; cxl, cxr = W / 2 - r * 0.72, W / 2 + r * 0.72
    def grid(names, cx, cy0, cols=2, d_=140, gap=18):
        rows = (len(names) + cols - 1) // cols
        for k, n in enumerate(names):
            ch = CH_[n](); ch = ch.resize((d_, d_), Image.LANCZOS); c_ = k % cols; r_ = k // cols
            nc = min(cols, len(names) - r_ * cols); x = cx - (nc * d_ + (nc - 1) * gap) / 2 + c_ * (d_ + gap); y = cy0 + r_ * (d_ + 46)
            im.alpha_composite(ch, (int(x), int(y))); lab = LABEL.get(n, n); f = MONT(700, 22); d.text((x + d_ / 2 - d.textlength(lab, font=f) / 2, y + d_ + 4), lab, font=f, fill=(40, 40, 48))
    def vc(names, d_=140): rows = (len(names) + 1) // 2; return cy - (rows * (d_ + 46) - 46) / 2 + 20
    grid(winners, cxl - r * 0.1, vc(winners)); grid(losers, cxr + r * 0.1, vc(losers))
    if middle:
        cx = W / 2; d.text((cx - d.textlength('the weird middle', font=MONT(800, 40)) / 2, 1080), 'the weird middle', font=MONT(800, 40), fill=(80, 60, 150))
        grid(middle, cx, 1140, cols=3, d_=130)
    if header:
        f = ANTON(150); d.text(((W - d.textlength(header, font=f)) / 2, 270), header, font=f, fill=BLUE)
    return im
def tuck_card(t, img_path, w, y, x=None):
    fr = grabf(t); c = Image.open(img_path).convert('RGB'); c = rounded_(c.resize((w, int(c.height * w / c.width)), Image.LANCZOS), 26)
    lay = fr.copy(); xx = (W - w) // 2 if x is None else x; drop(lay, c, (xx, y)); lay.paste(fr, (0, 0), her_mask(t)); return lay
def sides(t, left, right, lw=330, rw=330, y=420):
    fr = grabf(t); lay = fr.copy(); drop(lay, left, (20, y)); drop(lay, right, (W - right.width - 20, y)); lay.paste(fr, (0, 0), her_mask(t)); return lay
def make_bill():
    import numpy as np
    b = Image.open(V + '/billbase.jpg').convert('RGB'); b = b.crop((296, 296, 2067, 1016))           # just the note
    bw, bh = b.size; cx, cy = bw * 0.5, bh * 0.53; ow, oh = 440, 470
    # clear the eagle with the note's paper tone, then an engraved oval portrait
    d = ImageDraw.Draw(b); d.ellipse((cx - 350, cy - 232, cx + 350, cy + 258), fill=(228, 228, 224))
    p = Image.open(V + '/jensen_portrait.jpg').convert('RGB'); m = Image.open(V + '/jp_mask.png').convert('L')
    box = (390, 90, 1290, 1050); p = p.crop(box); m = m.crop(box)
    g = p.convert('L'); g = Image.eval(g, lambda v: int(30 + v * 0.8)); paper = Image.new('L', g.size, 232); g = Image.composite(g, paper, m)
    tint = Image.merge('RGB', (g.point(lambda v: int(v * 0.92)), g.point(lambda v: int(v * 0.97)), g.point(lambda v: int(v * 0.92))))
    tint = tint.resize((ow, int(ow * tint.height / tint.width)), Image.LANCZOS)
    ov = Image.new('L', (ow, oh), 0); ImageDraw.Draw(ov).ellipse((0, 0, ow - 1, oh - 1), fill=255)
    b.paste(tint.crop((0, 0, ow, oh)), (int(cx - ow / 2), int(cy - oh / 2)), ov)
    d.ellipse((cx - ow / 2, cy - oh / 2, cx + ow / 2, cy + oh / 2), outline=(70, 80, 70), width=8)
    return b
BILL = None
def bill(t):
    global BILL
    if BILL is None: BILL = make_bill()
    fr = grabf(t).copy(); w = 900; bb = BILL.resize((w, int(BILL.height * w / BILL.width)), Image.LANCZOS).convert('RGBA')
    drop(fr, bb, ((W - w) // 2, 262)); return fr
def line_chart():
    im = dotgrid(); d = ImageDraw.Draw(im); t = 'biggest one-day gains ever'; f = MONT(800, 52); d.text(((W - d.textlength(t, font=f)) / 2, 300), t, font=f, fill=INK)
    L, R, T, Bt = 170, 700, 470, 1180
    d.line((L, T, L, Bt), fill=(60, 60, 66), width=4); d.line((L, Bt, R, Bt), fill=(60, 60, 66), width=4)
    for v in (0, 250, 500, 750, 1000):
        y = Bt - (Bt - T) * v / 1000; d.line((L - 10, y, L, y), fill=(60, 60, 66), width=3); lb = f'${v}B'; d.text((L - 20 - d.textlength(lb, font=MONT(600, 28)), y - 16), lb, font=MONT(600, 28), fill=(110, 110, 116))
        if v: d.line((L, y, R, y), fill=(225, 225, 228), width=2)
    for x_, lb in [(L, 'open'), (R, 'close')]: d.text((x_ - d.textlength(lb, font=MONT(700, 30)) / 2, Bt + 18), lb, font=MONT(700, 30), fill=(90, 90, 96))
    d.text((W / 2 - d.textlength('value added during the trading day', font=MONT(600, 28)) / 2, Bt + 62), 'value added during the trading day', font=MONT(600, 28), fill=(120, 120, 126))
    for v, col, name, sub in [(450, (120, 120, 130), 'microsoft', 'jul 30, 2026'), (952, (30, 170, 80), 'nvidia', 'nov 23, 2026')]:
        y1 = Bt - (Bt - T) * v / 1000; d.line((L, Bt, R, y1), fill=col, width=12); d.ellipse((R - 14, y1 - 14, R + 14, y1 + 14), fill=col)
        d.text((R + 26, y1 - 40), name, font=MONT(800, 38), fill=col); d.text((R + 26, y1 + 2), f'+${v}B', font=ANTON(60), fill=col); d.text((R + 26, y1 + 72), sub, font=MONT(600, 24), fill=(110, 110, 116))
    return im
def headline_card():
    return clip_card('source: your screenshot (outlet tbd)', "'I made the deal': Trump says he 'convinced' Nvidia board to reinstate Jensen Huang", ['made', 'deal', 'convinced'])
def jones(t):
    fr = grabf(t).copy(); j = cutout(V + '/jones_cut.png', 300); drop(fr, j, (70, 300)); d = ImageDraw.Draw(fr)
    lab = 'technically chairman'; f = MONT(800, 34); x = max(40, 70 + j.width / 2 - (d.textlength(lab, font=f) + 40) / 2)
    d.rounded_rectangle((x, 620, x + d.textlength(lab, font=f) + 40, 680), 30, fill=LIME); d.text((x + 20, 630), lab, font=f, fill=INK); return fr
def kress_fine(t):
    k = cutout(V + '/kress_cut.png', 420); fine = Image.open(V + '/thisisfine.png').convert('RGB'); fine = fine.crop((300, 0, 600, 284)); fine = rounded_(fine.resize((340, int(284 * 340 / 300)), Image.LANCZOS), 22)
    return sides(t, k, fine, y=400)
def lawyers(t):
    fr = grabf(t).copy(); c = Image.open('/tmp/claude-0/-home-user-enisonoff/672c1244-cc8a-569f-a9ee-237151e2864a/images/77.jpg').convert('RGB'); w = 560
    c = rounded_(c.resize((w, int(c.height * w / c.width)), Image.LANCZOS), 22); drop(fr, c, ((W - w) // 2, 270)); d = ImageDraw.Draw(fr)
    t1 = 'lawyers = happy'; f = MONT(800, 44); x = (W - d.textlength(t1, font=f) - 50) / 2; d.rounded_rectangle((x, 270 + c.height + 20, x + d.textlength(t1, font=f) + 50, 270 + c.height + 90), 34, fill=LIME); d.text((x + 25, 270 + c.height + 32), t1, font=f, fill=INK); return fr
def anim_strip(rows, t, n=4):
    """word-by-word blur reveal like the reference reels"""
    words = []
    for txt, kind in rows: words += [(w, kind) for w in txt.split()]
    out = []
    for step in range(1, n + 1):
        frac = step / n; fr = grabf(t).copy(); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); y = 270
        shown = int(round(len(words) * frac + 0.49)) if step < n else len(words); k = 0
        for txt, kind in rows:
            f = ISI(84) if kind == 'i' else ANTON(170); ws = txt.split(); sp = d.textlength(' ', font=f); tw = sum(d.textlength(w, font=f) for w in ws) + sp * (len(ws) - 1); x = (W - tw) / 2
            for w in ws:
                if k < shown:
                    wl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(wl).text((x, y), w, font=f, fill=INK if kind == 'i' else BLUE)
                    if k == shown - 1 and step < n: wl = wl.filter(ImageFilter.GaussianBlur(9))
                    lay.alpha_composite(wl)
                x += d.textlength(w, font=f) + sp; k += 1
            y += d.textbbox((0, 0), txt, font=f)[3] - 2
        fr.alpha_composite(lay); out.append(fr)
    return out

EV = (['jensen', 'nvidia staff', 'ai stocks', 'lawyers'], ['the board', 'kress', 'bessent'])
BEATS = [
 ('0:05', 'two guys are happy: real photo tucked behind your head', lambda: tuck_card('5.8', V + '/tj1.jpg', 560, 262)),
 ('0:07', 'first venn: JENSEN 2.0 sets the stage', lambda: venn_faces([], [], [], header='JENSEN 2.0')),
 ('0:13', 'venn with faces + logos instead of names', lambda: venn_faces(['jensen'], [], [])),
 ('0:29', 'one simple chart: nvidia vs microsoft record days', line_chart),
 ('0:35', '$33.7B: jensen on a billion-dollar bill', lambda: bill('36.0')),
 ('0:47', 'rally relabeled "nov 23 rally"', lambda: bars_anim('november 23rd rally', [('IREN', 24), ('CoreWeave', 22), ('Nebius', 20), ('Oracle', 12)], 24, '%')(1.0)),
 ('0:59', 'lawyers = happy (your stock photo)', lambda: lawyers('60.5')),
 ('1:05', 'losers venn with faces', lambda: venn_faces(EV[0], ['the board'], [])),
 ('1:13', '"threats from the president": your headline (source tbd)', headline_card),
 ('1:17', 'harvey jones: head + "technically chairman"', lambda: jones('78.5')),
 ('1:20', 'kress + "this is fine" either side of you', lambda: kress_fine('82.0')),
 ('1:25', '"reportedly excluded": FT headline, then back to you', lambda: clip_card('Financial Times', 'Nvidia CFO Colette Kress kept out of secret talks over Jensen Huang\'s return', ['kept', 'out'])),
 ('2:00', 'weird middle with faces', lambda: venn_faces(EV[0], EV[1], ['nvidia', 'trump'])),
 ('2:40', 'ending: full map', lambda: venn_faces(EV[0], EV[1] + ['women'], ['nvidia', 'trump', 'democrats'])),
]
tw, th = 300, 533; cols = 7; rows = (len(BEATS) + cols - 1) // cols
sh = Image.new('RGB', (cols * (tw + 10) + 10, rows * (th + 76) + 10 + 520), (20, 20, 20)); dd = ImageDraw.Draw(sh)
for i, (ts, note, fn) in enumerate(BEATS):
    im = fn(); dr = ImageDraw.Draw(im)
    for yy in (250, 1560): dr.line((0, yy, W, yy), fill=(255, 0, 0), width=3)
    x = 10 + (i % cols) * (tw + 10); y = 10 + (i // cols) * (th + 76); sh.paste(im.convert('RGB').resize((tw, th), Image.LANCZOS), (x, y))
    dd.text((x, y + th + 6), ts, font=MONT(800, 22), fill=(255, 232, 0)); w_ = note.split(); dd.text((x, y + th + 34), ' '.join(w_[:6]), font=MONT(500, 15), fill=(230, 230, 230)); dd.text((x, y + th + 54), ' '.join(w_[6:]), font=MONT(500, 15), fill=(230, 230, 230))
y0 = 10 + rows * (th + 76); dd.text((10, y0), 'HEADER ANIMATION (like the reference reels): words land one at a time, each blurring into focus', font=MONT(800, 22), fill=(255, 232, 0))
for k, im in enumerate(anim_strip([('we just lived through', 'i'), ('HISTORY', 'B')], '0.8')):
    sh.paste(im.convert('RGB').crop((0, 150, W, 1150)).resize((440, 407), Image.LANCZOS), (10 + k * 450, y0 + 40))
sh.save(V + '/storyboard_E.png'); print(sh.size)
