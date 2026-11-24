"""Winners & losers, version E. usage: python3 renderE.py audit | lq | hq"""
import sys, os, json, wave, subprocess
import numpy as np
MODE = sys.argv[1]
exec(open('/tmp/claude-0/-home-user-enisonoff/672c1244-cc8a-569f-a9ee-237151e2864a/scratchpad/v14/sbE.py').read().split("EV = (")[0])
sys.argv = ['x', MODE]

KEEP = [(0.0, 138.95), (140.98, 164.7)]          # drops the repeated "Democrats, also Democrats."
OUT_DUR = sum(b - a for a, b in KEEP)
def o2s(t):
    for a, b in KEEP:
        if t < b - a: return a + t
        t -= b - a
    return KEEP[-1][1]

# ---------- tucked photos: per-frame mask of her ----------
_mc = {}
def mask_src(t):
    fi = int(round(t * 30))
    for k in (0, 1, -1, 2, -2):
        p = f'{V}/mt/{fi + k:05d}.png'
        if os.path.exists(p):
            if p not in _mc: _mc[p] = Image.open(p).convert('L').resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2))
            return _mc[p]
    return None
def card_layer(img_path, w, y, oval=False):
    c = Image.open(img_path).convert('RGB'); c = c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)
    if oval:
        m = Image.new('L', c.size, 0); ImageDraw.Draw(m).ellipse((0, 0, c.width - 1, c.height - 1), fill=255); c = c.convert('RGBA'); c.putalpha(m)
    else: c = rounded_(c, 26)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); drop(lay, c, ((W - w) // 2, y)); return lay
TWO = card_layer(V + '/tj1.jpg', 560, 262); KISS = card_layer(V + '/kisscam.jpg', 520, 262, oval=True)

# ---------- poster layers ----------
def bill_layer():
    b = make_bill(); w = 900; bb = b.resize((w, int(b.height * w / b.width)), Image.LANCZOS).convert('RGBA')
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); drop(lay, bb, ((W - w) // 2, 262)); return lay
def jones_layer():
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); j = cutout(V + '/jones_cut.png', 300); drop(lay, j, (70, 300)); d = ImageDraw.Draw(lay)
    lab = 'technically chairman'; f = MONT(800, 34); x = max(40, 70 + j.width / 2 - (d.textlength(lab, font=f) + 40) / 2)
    d.rounded_rectangle((x, 620, x + d.textlength(lab, font=f) + 40, 680), 30, fill=LIME); d.text((x + 20, 630), lab, font=f, fill=INK); return lay
def kress_layer():
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); k = cutout(V + '/kress_cut.png', 420)
    fine = Image.open(V + '/thisisfine.png').convert('RGB').crop((300, 0, 600, 284)); fine = rounded_(fine.resize((340, int(284 * 340 / 300)), Image.LANCZOS), 22)
    drop(lay, k, (20, 400)); drop(lay, fine, (W - fine.width - 20, 400)); return lay
def trump_layer():
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tc = Image.open(V + '/trump_cut.png').convert('RGBA'); tc.thumbnail((230, 290), Image.LANCZOS)
    drop(lay, tc, (W - tc.width - 20, 500), 110); return lay
def pill_layer(txt):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); f = ISI(92); tw = d.textlength(txt, font=f)
    d.rounded_rectangle(((W - tw) / 2 - 40, 280, (W + tw) / 2 + 40, 400), 60, fill=LIME); d.text(((W - tw) / 2, 290), txt, font=f, fill=INK); return lay

# word-by-word blur-in (the reference reels): each word lands 0.09 s after the previous, blurring into focus over 0.2 s
def word_plan(rows):
    plan = []; y = 270; d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    three = len(rows) == 3
    for txt, kind in rows:
        f = (ISI(66) if three else ISI(84)) if kind == 'i' else ANTON((130 if three else 170) if len(txt) <= 9 else 130)
        col = INK if kind == 'i' else BLUE; ws = txt.split(); sp = d0.textlength(' ', font=f)
        tw = sum(d0.textlength(w, font=f) for w in ws) + sp * (len(ws) - 1); x = (W - tw) / 2
        for w in ws:
            bb = d0.textbbox((0, 0), w, font=f); img = Image.new('RGBA', (int(bb[2]) + 40, int(bb[3]) + 40), (0, 0, 0, 0)); ImageDraw.Draw(img).text((20, 20), w, font=f, fill=col)
            plan.append((img, int(x) - 20, int(y) - 20)); x += d0.textlength(w, font=f) + sp
        y += d0.textbbox((0, 0), txt, font=f)[3] - 2
    return plan
def poster_at(plan, extra, dt):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if extra is not None: lay.alpha_composite(extra)
    for k, (img, x, y) in enumerate(plan):
        q = (dt - k * 0.09) / 0.2
        if q <= 0: continue
        if q < 1:
            im = img.filter(ImageFilter.GaussianBlur(10 * (1 - q))); a = im.split()[3].point(lambda v: int(v * min(1, q * 1.5))); im.putalpha(a); lay.alpha_composite(im, (x, y))
        else: lay.alpha_composite(img, (x, y))
    return lay

def chart_anim(p):
    """the two lines draw in from the origin"""
    im = dotgrid(); d = ImageDraw.Draw(im); t = 'biggest one-day gains ever'; f = MONT(800, 52); d.text(((W - d.textlength(t, font=f)) / 2, 300), t, font=f, fill=INK)
    L, R, T, Bt = 170, 700, 470, 1180
    d.line((L, T, L, Bt), fill=(60, 60, 66), width=4); d.line((L, Bt, R, Bt), fill=(60, 60, 66), width=4)
    for v in (0, 250, 500, 750, 1000):
        y = Bt - (Bt - T) * v / 1000; d.line((L - 10, y, L, y), fill=(60, 60, 66), width=3); lb = f'${v}B'; d.text((L - 20 - d.textlength(lb, font=MONT(600, 28)), y - 16), lb, font=MONT(600, 28), fill=(110, 110, 116))
        if v: d.line((L, y, R, y), fill=(225, 225, 228), width=2)
    for x_, lb in [(L, 'open'), (R, 'close')]: d.text((x_ - d.textlength(lb, font=MONT(700, 30)) / 2, Bt + 18), lb, font=MONT(700, 30), fill=(90, 90, 96))
    d.text((W / 2 - d.textlength('value added during the trading day', font=MONT(600, 28)) / 2, Bt + 62), 'value added during the trading day', font=MONT(600, 28), fill=(120, 120, 126))
    for k, (v, col, name, sub) in enumerate([(450, (120, 120, 130), 'microsoft', 'jul 30, 2026'), (952, (30, 170, 80), 'nvidia', 'nov 23, 2026')]):
        q = ease((p - k * 0.5) / 1.0)
        if q <= 0: continue
        y1 = Bt - (Bt - T) * v / 1000; xe = L + (R - L) * q; ye = Bt + (y1 - Bt) * q; d.line((L, Bt, xe, ye), fill=col, width=12)
        if q >= 1:
            d.ellipse((R - 14, y1 - 14, R + 14, y1 + 14), fill=col); d.text((R + 26, y1 - 40), name, font=MONT(800, 38), fill=col)
            d.text((R + 26, y1 + 2), f'+${v}B', font=ANTON(60), fill=col); d.text((R + 26, y1 + 72), sub, font=MONT(600, 24), fill=(110, 110, 116))
    return im

EV0 = ['jensen', 'nvidia staff', 'ai stocks', 'lawyers']; EV1 = ['the board', 'kress', 'bessent']
TL1 = timeline_quotes(('NOV 17', ['"does not intend to', 'reinstate jensen"'], '— nvidia chair harvey jones', (215, 45, 150)), ('NOV 23', ['voted unanimously', 'to reinstate him'], '— nvidia board', (30, 90, 210)), '6 days later')
TL2 = timeline_quotes(('NOV 15', ['nvidia should "go', 'outside the company"'], '— treasury sec. scott bessent', (215, 45, 150)), ('NOV 22', ['"he\'s on the', 'outside now"'], '— on face the nation', (30, 90, 210)), '7 days later', face=bess_face())
ABC = clip_card('ABC News · Nov 23', "'I made the deal': Trump says he 'convinced' Nvidia board to reinstate Jensen Huang", ['made', 'deal', 'convinced'])
CBS = clip_card('CBS News · Nov 12', 'Nvidia CEO Jensen Huang resigns in wake of affair with woman suspected of spying for China', ['resigns', 'spying'])
RALLY = bars_anim('november 23rd rally', [('IREN', 24), ('CoreWeave', 22), ('Nebius', 20), ('Oracle', 12)], 24, '%')

# (start, end, kind, payload) in SOURCE seconds.  kinds: PA poster(anim), T tucked photo, S slide, A animated slide
B = [
 (0.0, 1.35, 'PA', (word_plan([('we just lived through', 'i'), ('HISTORY', 'B')]), None)),
 (1.4, 3.25, 'S', post_slide()),
 (5.2, 6.62, 'T', TWO),
 (6.62, 11.75, 'S', venn_faces([], [], [], header='JENSEN 2.0')),
 (11.8, 14.75, 'S', venn_faces(['jensen'], [], [])),
 (14.8, 18.1, 'T', KISS),
 (18.1, 21.0, 'S', CBS),
 (25.4, 28.7, 'PA', (word_plan([('friends in', 'i'), ('HIGH PLACES', 'B')]), trump_layer())),
 (28.8, 34.6, 'A', chart_anim),
 (34.7, 38.2, 'PA', ([], bill_layer())),
 (38.3, 42.0, 'S', venn_faces(['jensen', 'nvidia staff'], [], [])),
 (47.1, 54.8, 'A', RALLY),
 (59.3, 65.0, 'PA', ([], pill_layer('lawyers = happy'))),
 (65.1, 68.75, 'S', venn_faces(EV0, ['the board'], [])),
 (68.8, 73.45, 'S', TL1),
 (73.45, 75.5, 'S', ABC),
 (77.5, 80.1, 'PA', ([], jones_layer())),
 (80.2, 88.4, 'PA', ([], kress_layer())),
 (92.5, 99.35, 'S', TL2),
 (104.9, 108.35, 'PA', (word_plan([('corporate governance', 'i'), ('DOWN BAD', 'B')]), None)),
 (108.4, 113.2, 'S', eq_slide()),
 (C0, 117.5, 'A', 'clones'),
 (119.2, 123.55, 'S', venn_faces(EV0, EV1, ['nvidia', 'trump'])),
 (147.6, 160.2, 'PA', (word_plan([('no corporate', 'i'), ('ACCOUNTABILITY', 'B')]), None)),
 (160.3, 166.0, 'S', venn_faces(EV0, EV1 + ['women'], ['nvidia', 'trump', 'democrats'])),
]
# no flicker: close tiny gaps, then snap every boundary onto her own jump cuts (the democrats cut counts as one)
for i in range(len(B) - 1):
    if 0 < B[i + 1][0] - B[i][1] < 0.5: B[i] = (B[i][0], B[i + 1][0]) + B[i][2:]
JUMPS = [float(x) for x in open(V + '/jumpcuts.txt').read().split()] + [138.95, 140.98]
def snap(x):
    near = [j for j in JUMPS if abs(j - x) <= 0.45]
    return min(near, key=lambda j: abs(j - x)) if near else x
B = [(snap(b[0]), snap(b[1])) + b[2:] for b in B]; B = [b for b in B if b[1] - b[0] > 0.3]
for i in range(len(B) - 1):
    if B[i][1] > B[i + 1][0]: B[i] = (B[i][0], B[i + 1][0]) + B[i][2:]
B[-1] = (B[-1][0], 166.0) + B[-1][2:]

def beat_at(t):
    for b in B:
        if b[0] <= t < b[1]: return b
def compose(fr, t):
    b = beat_at(t); wb = False; im = fr.convert('RGBA')
    if b is not None:
        k = b[2]
        if k == 'PA': im.alpha_composite(poster_at(b[3][0], b[3][1], t - b[0]))
        elif k == 'T':
            im.alpha_composite(b[3]); m = mask_src(t)
            if m is not None: im.paste(fr, (0, 0), m)
        elif k == 'S': im = b[3].copy(); wb = True
        else:
            wb = True; im = (frame_at(t).convert('RGBA') if b[3] == 'clones' else b[3](t - b[0]))
    words = chunk_at(t)
    if words: hi = max(range(len(words)), key=lambda k: len(words[k])); (inkcap if wb else caption)(im, words, hi)
    return im.convert('RGB')

def audit():
    n = int(OUT_DUR * FPS); st = []
    for k in range(n):
        t = o2s(k / FPS); b = beat_at(t); sid = 'her' if b is None or b[2] in ('PA', 'T') else 'G%d' % B.index(b)
        if b is not None and b[2] in ('PA', 'T'): sid += '+%d' % B.index(b)
        st.append(sid + ('@' + str(sum(1 for j in JUMPS if j <= t)) if sid.startswith('her') else ''))
    runs = []; s0 = 0
    for k in range(1, n + 1):
        if k == n or st[k] != st[s0]: runs.append((s0, k - s0, st[s0])); s0 = k
    print('short flashes:', [(round(a / FPS, 2), l, s) for a, l, s in runs if l < 8])

def clicks(path):
    sr = 48000; out = np.zeros(int((OUT_DUR + 1) * sr)); rng = np.random.default_rng(2)
    for b in B:
        o = None; acc = 0
        for a_, b_ in KEEP:
            if a_ <= b[0] < b_: o = acc + b[0] - a_
            acc += b_ - a_
        if o is None: continue
        f = 1400 + 900 * rng.random(); n = int(0.035 * sr); tt = np.arange(n) / sr
        s_ = (np.sin(2 * np.pi * f * tt) * 0.6 + rng.standard_normal(n) * 0.25) * np.exp(-tt * 150) * 10 ** (-31 / 20); i = int(o * sr); out[i:i + n] += s_
    w = wave.open(path, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes()); w.close()

if MODE == 'audit': audit(); raise SystemExit
lq = MODE == 'lq'; outf = V + ('/winners-losers-preview-lowq.mp4' if lq else '/winners-losers-v5.mp4'); clicks(V + '/clicksE.wav')
vc = ''.join(f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:flags=lanczos[v{i}];' for i, (a, b) in enumerate(KEEP)) + ''.join(f'[v{i}]' for i in range(len(KEEP))) + f'concat=n={len(KEEP)}:v=1:a=0[vout]'
src = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', V + '/raw.mp4', '-filter_complex', vc, '-map', '[vout]', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
ac = ''.join(f'[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];' for i, (a, b) in enumerate(KEEP)) + ''.join(f'[a{i}]' for i in range(len(KEEP))) + f'concat=n={len(KEEP)}:v=0:a=1[voice];[voice][2:a]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[aout]'
enc = ['-c:v', 'libx264', '-crf', '30', '-preset', 'veryfast', '-vf', 'scale=540:960'] if lq else ['-c:v', 'libx264', '-crf', '16', '-preset', 'slow']
out = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', V + '/raw.mp4', '-i', V + '/clicksE.wav',
                        '-filter_complex', ac, '-map', '0:v', '-map', '[aout]'] + enc + ['-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', outf], stdin=subprocess.PIPE)
i = 0; n = int(OUT_DUR * FPS)
while True:
    b = src.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    out.stdin.write(compose(Image.frombuffer('RGB', (W, H), b), o2s(i / FPS)).tobytes()); i += 1
    if i % 600 == 0: print(f'{100 * i / n:.0f}%', flush=True)
out.stdin.close(); out.wait(); print('done', outf, i)
