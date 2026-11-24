"""Winners & losers video, option D. usage: python3 renderD.py sb | render"""
import sys, json, math, wave, subprocess
import numpy as np
exec(open('/tmp/claude-0/-home-user-enisonoff/672c1244-cc8a-569f-a9ee-237151e2864a/scratchpad/v14/sbD.py').read().split("E0 = ([], [], ['?']);")[0])
exec(open(V + '/clones_anim.py').read().split('# storyboard strip')[0].split('\n', 1)[1])   # clones frame_at()
FF = lambda n, w, st, s: ImageFont.truetype(f'{S}/fonts/{n}/package/files/{n}-latin-{w}-{st}.woff', s)
ISI = lambda s: FF('instrument-serif', 400, 'italic', s)
FPS = 30
def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)

# ---------- poster style: instrument serif italic + tall blue caps, left-aligned, tight ----------
def poster_layer(rows):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); x, y = 90, 270
    for txt, kind in rows:
        three = len(rows) == 3
        f = (ISI(66) if three else ISI(84)) if kind == 'i' else ANTON((130 if three else 170) if len(txt) <= 9 else 130)
        col = INK if kind == 'i' else BLUE
        bb = d.textbbox((0, 0), txt, font=f); d.text(((W - bb[2]) / 2, y), txt, font=f, fill=col); y += bb[3] - 2
    return lay

def eq_slide():
    im = dotgrid(); d = ImageDraw.Draw(im)
    c = JC.copy(); c.thumbnail((470, 560), Image.LANCZOS); im.alpha_composite(c, (30, 560))
    lt = '1 jensen huang'; d.text((30 + c.width / 2 - d.textlength(lt, font=MONT(800, 40)) / 2, 560 + c.height + 20), lt, font=MONT(800, 40), fill=INK)
    d.text((500, 720), '=', font=ANTON(200), fill=INK); d.text((620, 700), '$1T', font=ANTON(230), fill=BLUE)
    d.rounded_rectangle((620, 990, 1010, 1060), 30, fill=LIME); d.text((650, 1000), 'in market value', font=MONT(800, 40), fill=INK)
    d.text((80, 380), 'what replacing jensen was priced at', font=MONT(700, 44), fill=(110, 110, 116)); return im

def bars_anim(title, items, maxv, unit):
    """returns f(p) -> image with bars grown to fraction p"""
    base = dotgrid(); _d = ImageDraw.Draw(base); _d.text(((W - _d.textlength(title, font=MONT(800, 50))) / 2, 470), title, font=MONT(800, 50), fill=INK)
    def f(p):
        im = base.copy(); d = ImageDraw.Draw(im); y = 600
        for k, (name, v) in enumerate(items):
            q = ease(min(max((p - k * 0.12) / 0.6, 0), 1))
            d.text((80, y), name, font=MONT(700, 40), fill=INK); bw = max(74, int(820 * v / maxv * q))
            d.rounded_rectangle((80, y + 56, 80 + bw, y + 130), 37, fill=LIME)
            if q > 0.85:
                tip = min(150, bw); d.rounded_rectangle((80 + bw - tip, y + 56, 80 + bw, y + 130), 37, fill=(230, 60, 60))
                lab = f'+{v:g}%' if unit == '%' else f'${v:g}B'; d.text((80 + bw - tip + 18, y + 70), lab, font=MONT(800, 38), fill=WHITE)
            y += 190
        return im
    return f

W_ALL = ['jensen', 'nvidia staff', 'ai stocks', 'lawyers']
L_ALL = ['the board', 'kress', 'bessent', 'governance']
# (start, end, kind, payload): kind 'P' poster over her, 'S' static slide, 'A' animated slide f(t)
B = [
 (0.0, 1.35, 'P', [('we just lived through', 'i'), ('HISTORY', 'B')]),
 (1.4, 3.25, 'S', 'POST'),
 (5.2, 6.62, 'P', 'TWO'),
 (6.62, 9.4, 'S', venn_clear([], [], None)),
 (9.4, 11.75, 'S', venn_clear([], [], [])),
 (11.8, 14.75, 'S', venn_clear(['jensen'], [], [])),
 (14.8, 21.0, 'S', clip_card('CBS News · Nov 12', 'Nvidia CEO Jensen Huang resigns in wake of affair with woman suspected of spying for China', ['resigns', 'spying'])),
 (25.4, 28.7, 'P', [('friends in', 'i'), ('HIGH PLACES', 'B')]),
 (28.8, 34.6, 'A', ('bars', bars_anim('biggest one-day gains ever', [('nvidia · nov 23', 952), ('old record · microsoft', 450)], 952, 'B'))),
 (34.7, 38.2, 'P', [('jensen got back', 'i'), ('$33.7B', 'B'), ('not bad for a monday', 'i')]),
 (38.3, 42.0, 'S', venn_clear(['jensen', 'nvidia staff'], [], [])),
 (47.1, 54.8, 'A', ('bars', bars_anim('monday\'s rally', [('IREN', 24), ('CoreWeave', 22), ('Nebius', 20), ('Oracle', 12)], 24, '%'))),
 (59.3, 65.0, 'P', [('BILLABLE', 'B'), ('hours', 'i')]),
 (65.1, 68.75, 'S', venn_clear(W_ALL, ['the board'], [])),
 (68.8, 75.5, 'S', timeline_quotes(('NOV 17', ['"does not intend to', 'reinstate jensen"'], '— nvidia chair harvey jones', (215, 45, 150)), ('NOV 23', ['voted unanimously', 'to reinstate him'], '— nvidia board', (30, 90, 210)), '6 days later')),
 (77.5, 80.1, 'P', [('harvey jones:', 'i'), ('DECORATIVE', 'B')]),
 (80.2, 88.4, 'S', clip_card('Financial Times', 'Nvidia CFO Colette Kress kept out of secret talks over Jensen Huang\'s return', ['kept', 'out'])),
 (88.5, 92.4, 'P', [('your old boss is', 'i'), ('BACK', 'B'), ('at your desk', 'i')]),
 (92.5, 99.35, 'S', timeline_quotes(('NOV 15', ['nvidia should "go', 'outside the company"'], '— treasury sec. scott bessent', (215, 45, 150)), ('NOV 22', ['"he\'s on the', 'outside now"'], '— on face the nation', (30, 90, 210)), '7 days later', face=bess_face())),
 (99.4, 104.85, 'P', [('a', 'i'), ('NEW OPTION?', 'B'), ('he\'s your ex', 'i')]),
 (104.9, 108.35, 'P', [('corporate governance', 'i'), ('DOWN BAD', 'B')]),
 (108.4, 113.2, 'S', eq_slide()),
 (C0, 117.5, 'A', ('clones', None)),
 (119.2, 123.55, 'S', venn_clear(W_ALL, L_ALL, ['nvidia', 'trump'])),
 (147.6, 160.2, 'P', [('no corporate', 'i'), ('ACCOUNTABILITY', 'B')]),
 (160.3, 165.0, 'S', venn_clear(W_ALL, ['the board', 'kress', 'bessent', 'women'], ['nvidia', 'trump', 'democrats'])),
]
def rounded_(im, r=28):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255); im = im.convert('RGBA'); im.putalpha(m); return im
def drop(cv, c, xy, a=120):
    s_ = Image.new('RGBA', (c.width + 80, c.height + 80), (0, 0, 0, 0)); s_.paste((0, 0, 0, a), (40, 52), c.split()[3]); cv.alpha_composite(s_.filter(ImageFilter.GaussianBlur(14)), (xy[0] - 40, xy[1] - 40)); cv.alpha_composite(c, xy)
def post_slide():
    im = dotgrid(); d = ImageDraw.Draw(im); t = 'the president posted this'; d.text(((W - d.textlength(t, font=ISI(80))) / 2, 290), t, font=ISI(80), fill=INK)
    p_ = Image.open(V + '/truthpost.webp').convert('RGBA'); p_ = p_.resize((700, int(p_.height * 700 / p_.width)), Image.LANCZOS); drop(im, rounded_(p_), ((W - 700) // 2, 410)); return im
def two_guys():
    lay = poster_layer([('two guys are', 'i'), ('HAPPY', 'B')])
    j = JC.copy(); j.thumbnail((250, 290), Image.LANCZOS); t_ = Image.open(V + '/trump_cut.png').convert('RGBA'); t_.thumbnail((230, 290), Image.LANCZOS)
    drop(lay, j, (30, 500), 100); drop(lay, t_, (W - t_.width - 30, 500), 100); return lay
for i, b in enumerate(B):
    if b[3] == 'POST': B[i] = (b[0], b[1], 'S', post_slide())
    elif b[3] == 'TWO': B[i] = (b[0], b[1], 'P', two_guys())
    elif b[2] == 'P': B[i] = (b[0], b[1], 'P', poster_layer(b[3]))
# line graphics up with her own jump cuts so two cuts never land a few frames apart
JUMPS = [float(x) for x in open(V + '/jumpcuts.txt').read().split()]
for i, b in enumerate(B):
    st, en = b[0], b[1]
    for j in JUMPS:
        if en < j <= en + 0.45: en = j
        if st - 0.45 <= j < st and (i == 0 or j >= B[i - 1][1]): st = j
    B[i] = (st, en) + b[2:]
# trump pops up beside "friends in high places"
_tc = Image.open(V + '/trump_cut.png').convert('RGBA'); _tc.thumbnail((230, 290), Image.LANCZOS)
for i, b in enumerate(B):
    if b[0] == 25.4:
        lay = b[3].copy(); sh = Image.new('RGBA', (_tc.width + 60, _tc.height + 60), (0, 0, 0, 0)); sh.paste((0, 0, 0, 110), (30, 40), _tc.split()[3])
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (W - _tc.width - 50, 470)); lay.alpha_composite(_tc, (W - _tc.width - 20, 500)); B[i] = (b[0], b[1], 'P', lay)
# no flicker: if two graphics are less than half a second apart, hold the first until the second starts
for i in range(len(B) - 1):
    if 0 < B[i + 1][0] - B[i][1] < 0.5: B[i] = (B[i][0], B[i + 1][0]) + B[i][2:]

# ---------- captions ----------
FIX = {'Nebbius,': 'Nebius,', 'Iron,': 'IREN,', 'Besant': 'Bessent', 'Wong': 'Huang', 'anti': 'anti-'}
WS = json.load(open(V + '/words.json'))
for w in WS: w['w'] = FIX.get(w['w'], w['w'])
CH, cur = [], []
for w in WS:
    cur.append(w)
    if len(cur) == 3 or w['w'][-1:] in '.,?!': CH.append(cur); cur = []
if cur: CH.append(cur)
def chunk_at(t):
    for k, c in enumerate(CH):
        end = min(CH[k + 1][0]['s'] if k + 1 < len(CH) else 1e9, c[-1]['e'] + 0.25)
        if c[0]['s'] <= t < end: return [x['w'].upper().strip(',.?!').replace('ANTI- ', 'ANTI-') for x in c]

def beat_at(t):
    for b in B:
        if b[0] <= t < b[1]: return b

def compose(fr, t):
    b = beat_at(t); wb = False
    if b is None: im = fr.convert('RGBA')
    elif b[2] == 'P': im = fr.convert('RGBA'); im.alpha_composite(b[3])
    elif b[2] == 'S': im = b[3].copy(); wb = True
    else:
        kind, f = b[3]; wb = True
        im = (frame_at(t).convert('RGBA') if kind == 'clones' else f((t - b[0]) / 1.0))
    words = chunk_at(t)
    if words:
        hi = max(range(len(words)), key=lambda k: len(words[k])); (inkcap if wb else caption)(im, words, hi)
    return im.convert('RGB')

def clicks():
    sr = 48000; dur = 165.0; out = np.zeros(int(dur * sr) + sr); rng = np.random.default_rng(2)
    for k, b in enumerate(B):
        f = 1400 + 900 * rng.random(); n = int(0.035 * sr); tt = np.arange(n) / sr
        s = (np.sin(2 * np.pi * f * tt) * 0.6 + rng.standard_normal(n) * 0.25) * np.exp(-tt * 150) * 10 ** (-31 / 20)
        i = int(b[0] * sr); out[i:i + n] += s
    w = wave.open(V + '/clicks.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes()); w.close()

def grab(t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', V + '/raw.mp4', '-frames:v', '1', '-vf', f'scale={W}:{H}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombuffer('RGB', (W, H), raw).copy()

# final pass (after gap-closing): snap every graphic boundary within 0.45 s of one of her jump cuts onto that cut
def snap(x):
    near = [j for j in JUMPS if abs(j - x) <= 0.45]
    return min(near, key=lambda j: abs(j - x)) if near else x
B = [(snap(b[0]), snap(b[1])) + b[2:] for b in B]
B = [b for b in B if b[1] - b[0] > 0.3]
B[-1] = (B[-1][0], 166.0) + B[-1][2:]   # ending holds to the very last frame
for i in range(len(B) - 1):
    if B[i][1] > B[i + 1][0]: B[i] = (B[i][0], B[i + 1][0]) + B[i][2:]
def audit():
    # every on-screen state (her shot, or which graphic) and her own jump cuts; flag anything shorter than 8 frames
    n = int(164.7 * FPS); states = []
    for k in range(n):
        t = k / FPS; b = beat_at(t); sid = 'her' if b is None else ('her+P%d' % B.index(b) if b[2] == 'P' else 'G%d' % B.index(b))
        if b is None or b[2] == 'P': sid += '@' + str(sum(1 for j in JUMPS if j <= t))
        states.append(sid)
    runs = []; st = 0
    for k in range(1, n + 1):
        if k == n or states[k] != states[st]: runs.append((st, k - st, states[st])); st = k
    bad = [(round(a / FPS, 2), l, sid) for a, l, sid in runs if l < 8]
    print('short flashes (start s, frames, state):', bad)
if sys.argv[1] == 'audit': audit(); raise SystemExit
if sys.argv[1] == 'sb':
    tiles = []
    for b in B:
        t = b[0] + min(1.2, (b[1] - b[0]) * 0.6); im = compose(grab(t), t)
        d = ImageDraw.Draw(im); d.text((30, 1720), f'{int(t // 60)}:{t % 60:04.1f}', font=MONT(800, 60), fill=(255, 0, 140))
        tiles.append(im.resize((216, 384), Image.LANCZOS))
    cols = 8; rows = (len(tiles) + cols - 1) // cols; sh = Image.new('RGB', (cols * 222 + 6, rows * 390 + 6), (20, 20, 20))
    for i, im in enumerate(tiles): sh.paste(im, (6 + (i % cols) * 222, 6 + (i // cols) * 390))
    sh.save(V + '/final_check.png'); print('ok', len(B))
else:
    clicks()
    src = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', V + '/raw.mp4', '-vf', f'fps={FPS},scale={W}:{H}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    out = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', V + '/raw.mp4', '-i', V + '/clicks.wav',
                            '-filter_complex', '[1:a][2:a]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]', '-map', '0:v', '-map', '[a]',
                            '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', V + '/winners-losers-v4.mp4'], stdin=subprocess.PIPE)
    i = 0; n = int(164.7 * FPS)
    while True:
        b = src.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        out.stdin.write(compose(Image.frombuffer('RGB', (W, H), b), i / FPS).tobytes()); i += 1
        if i % 300 == 0: print(f'{100 * i / n:.0f}%', flush=True)
    out.stdin.close(); out.wait(); print('done', i)
