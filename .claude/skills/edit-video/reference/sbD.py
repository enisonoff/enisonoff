exec(open('/tmp/claude-0/-home-user-enisonoff/672c1244-cc8a-569f-a9ee-237151e2864a/scratchpad/v14/sb_options.py').read().split("E0 = (")[0])
import subprocess, os
def grabf(t):
    p = f'{V}/b_{t}.png'
    if not os.path.exists(p): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', V + '/raw.mp4', '-frames:v', '1', '-vf', 'scale=1080:1920:flags=lanczos', p])
    return Image.open(p).convert('RGBA')
def clip_card(outlet, head, hl, y=560, size=60):
    im = dotgrid(); d = ImageDraw.Draw(im); f = MONT(700, size); words = head.split(); lines = ['']
    for w in words:
        t = (lines[-1] + ' ' + w).strip()
        if d.textlength(t, font=f) > 900: lines.append(w)
        else: lines[-1] = t
    d.rounded_rectangle((50, y - 60, W - 50, y + 80 + len(lines) * (size + 22)), 18, fill=(255, 255, 255), outline=(220, 220, 220), width=2)
    d.text((80, y - 30), outline_txt := outlet.upper(), font=MONT(800, 26), fill=(120, 120, 126)); yy = y + 20
    for ln in lines:
        x = 80
        for w in ln.split():
            tw = d.textlength(w + ' ', font=f)
            if any(h in w for h in hl): d.rectangle((x - 6, yy + 6, x + tw - 8, yy + size + 10), fill=LIME)
            d.text((x, yy), w, font=f, fill=INK); x += tw
        yy += size + 22
    return im
def bars(title, items, maxv, unit='%', note=None):
    im = dotgrid(); d = ImageDraw.Draw(im); d.text((80, 470), title, font=MONT(800, 50), fill=INK); y = 600
    for name, v in items:
        d.text((80, y), name, font=MONT(700, 40), fill=INK); bw = int(820 * v / maxv)
        d.rectangle((80, y + 56, 80 + bw, y + 126), fill=LIME); d.rectangle((80 + bw - 110, y + 56, 80 + bw, y + 126), fill=(230, 60, 60))
        lab = f'+{v:g}{unit}' if unit == '%' else f'${v:g}B'; d.text((80 + bw - 100, y + 66), lab, font=MONT(800, 38), fill=WHITE); y += 190
    if note: d.text((80, y + 10), note, font=MONT(500, 28), fill=(120, 120, 126))
    return im
def two_quotes(a, b):
    im = dotgrid(); d = ImageDraw.Draw(im); y = 480
    for date, q, who, col in (a, b):
        d.rounded_rectangle((60, y, W - 60, y + 330), 20, fill=(255, 255, 255), outline=(220, 220, 220), width=2)
        d.text((100, y + 30), date, font=MONT(800, 30), fill=col); ff = MONT(700, 54); yy = y + 90
        for ln in q: d.text((100, yy), ln, font=ff, fill=INK); yy += 66
        d.text((100, yy + 10), who, font=MONT(500, 28), fill=(120, 120, 126)); y += 400
    return im
def wb_num(top, big, sub, col=BLUE):
    im = dotgrid(); d = ImageDraw.Draw(im)
    for txt, f, c, y in [(top, MONT(700, 48), INK, 560), (big, ANTON(260), col, 640), (sub, MONT(700, 48), INK, 960)]:
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=c)
    return im

def clip_placeholder():
    im = Image.new('RGBA', (W, H), (18, 18, 22, 255)); d = ImageDraw.Draw(im)
    d.rectangle((60, 560, W - 60, 1180), outline=(90, 90, 100), width=4)
    for txt, f, y in [('YOUR CLIP', MONT(800, 60), 760), ('trump: "sex sells"', MONT(700, 50), 850), ('full screen, ~1.5 s', MONT(500, 34), 930)]:
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=(230, 230, 236))
    return im

def venn_clear(winners, losers, middle_list, cy=720, r=300):
    im = dotgrid(); size = (W, H); cx = W / 2
    a = Image.new('RGB', size, (255, 255, 255)); b = Image.new('RGB', size, (255, 255, 255)); cxl, cxr = cx - r * 0.72, cx + r * 0.72
    ImageDraw.Draw(a).ellipse((cxl - r, cy - r, cxl + r, cy + r), fill=LB); ImageDraw.Draw(b).ellipse((cxr - r, cy - r, cxr + r, cy + r), fill=LP)
    fill = ImageChops.multiply(a, b); m = Image.new('L', size, 0); md = ImageDraw.Draw(m)
    md.ellipse((cxl - r, cy - r, cxl + r, cy + r), fill=235); md.ellipse((cxr - r, cy - r, cxr + r, cy + r), fill=235)
    im.paste(fill, (0, 0), m); d = ImageDraw.Draw(im)
    d.ellipse((cxl - r, cy - r, cxl + r, cy + r), outline=(110, 170, 250), width=4); d.ellipse((cxr - r, cy - r, cxr + r, cy + r), outline=(245, 120, 210), width=4)
    def ct(sx, y, txt, f, col): d.text((sx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=col)
    lx, rx = cxl - r * 0.12, cxr + r * 0.12           # centered in each circle
    ct(lx, cy - r * 0.66, 'winners', MONT(800, 50), (25, 80, 205)); ct(rx, cy - r * 0.66, 'losers', MONT(800, 50), (200, 30, 140))
    nf = MONT(700, 46); n = max(len(winners), len(losers), 1); y0 = cy - (len(winners) * 56) / 2 + 10
    for i, w in enumerate(winners): ct(lx, cy - len(winners) * 28 + 20 + i * 56, w, nf, (25, 25, 32))
    for i, w in enumerate(losers): ct(rx, cy - len(losers) * 28 + 20 + i * 56, w, nf, (25, 25, 32))
    if middle_list is not None:
        # arrow from the overlap down to a roomy list underneath
        ay0, ay1 = cy + r * 0.35, cy + r + 70
        d.line((cx, ay0, cx, ay1), fill=(80, 60, 150), width=6); d.polygon([(cx - 18, ay1 - 6), (cx + 18, ay1 - 6), (cx, ay1 + 22)], fill=(80, 60, 150))
        if middle_list:
            ct(cx, ay1 + 40, 'the weird middle', MONT(800, 46), (80, 60, 150))
            ct(cx, ay1 + 104, '  ·  '.join(middle_list), MONT(700, 44), (25, 25, 32))
        else: ct(cx, ay1 + 40, '?', MONT(800, 60), (80, 60, 150))
    return im
def bars(title, items, maxv, unit='%', note=None):
    im = dotgrid(); d = ImageDraw.Draw(im); d.text((80, 470), title, font=MONT(800, 50), fill=INK); y = 600
    for name, v in items:
        d.text((80, y), name, font=MONT(700, 40), fill=INK); bw = int(820 * v / maxv)
        d.rounded_rectangle((80, y + 56, 80 + bw, y + 130), 37, fill=LIME)
        tip = min(150, bw); d.rounded_rectangle((80 + bw - tip, y + 56, 80 + bw, y + 130), 37, fill=(230, 60, 60))
        lab = f'+{v:g}{unit}' if unit == '%' else f'${v:g}B'; d.text((80 + bw - tip + 18, y + 70), lab, font=MONT(800, 38), fill=WHITE); y += 190
    if note: d.text((80, y + 10), note, font=MONT(500, 28), fill=(120, 120, 126))
    return im
def timeline_quotes(a, b, gap_label, face=None):
    im = dotgrid(); d = ImageDraw.Draw(im); ys = [430, 900]
    for (date, q, who, col), y in zip((a, b), ys):
        d.rounded_rectangle((60, y, W - 60, y + 300), 22, fill=(255, 255, 255), outline=(220, 220, 220), width=2)
        d.text((110, y + 28), date, font=MONT(800, 32), fill=col); ff = MONT(700, 52); yy = y + 86
        for ln in q: d.text((110, yy), ln, font=ff, fill=INK); yy += 64
        d.text((110, yy + 8), who, font=MONT(500, 28), fill=(120, 120, 126))
    # connector: a dotted spine from card to card with the gap label beside it
    x = 150; y0, y1 = ys[0] + 300, ys[1]
    for yy in range(int(y0) + 8, int(y1) - 4, 18): d.ellipse((x - 5, yy - 5, x + 5, yy + 5), fill=(80, 60, 150))
    d.ellipse((x - 14, y0 - 14, x + 14, y0 + 14), fill=(215, 45, 150)); d.ellipse((x - 14, y1 - 14, x + 14, y1 + 14), fill=(30, 90, 210))
    d.rounded_rectangle((x + 34, (y0 + y1) / 2 - 34, x + 34 + d.textlength(gap_label, font=MONT(800, 40)) + 40, (y0 + y1) / 2 + 34), 34, fill=LIME)
    d.text((x + 54, (y0 + y1) / 2 - 26), gap_label, font=MONT(800, 40), fill=INK)
    if face is not None:
        f_ = face.copy(); f_.thumbnail((330, 380), Image.LANCZOS); fx, fy = W - f_.width - 30, ys[1] + 300 - 230
        sh = Image.new('RGBA', (f_.width + 60, f_.height + 60), (0, 0, 0, 0)); sh.paste((0, 0, 0, 120), (30, 40), f_.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(12))
        im.alpha_composite(sh, (fx - 30, fy - 30)); im.alpha_composite(f_, (fx, fy))
    return im
def face_or_placeholder(path):
    if os.path.exists(path):
        return Image.open(path).convert('RGBA')
    ph = Image.new('RGBA', (360, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(ph); d.ellipse((60, 20, 300, 260), fill=(200, 200, 206)); d.rounded_rectangle((20, 250, 340, 460), 80, fill=(200, 200, 206))
    d.text((70, 120), 'BESSENT', font=MONT(800, 40), fill=(120, 120, 126)); d.text((95, 170), '(photo)', font=MONT(600, 30), fill=(120, 120, 126)); return ph
def bess_face():
    p = V + '/bessent_cut.png'
    return face_or_placeholder(p)
JC = Image.open(V + '/jensen_cut.png').convert('RGBA'); JC = JC.crop(JC.getbbox())
def clones(n=9):
    im = dotgrid(); d = ImageDraw.Draw(im)
    t = 'CLONING?'; f = ANTON(150); d.text(((W - d.textlength(t, font=f)) / 2, 290), t, font=f, fill=BLUE)
    c = JC.copy(); c.thumbnail((300, 380), Image.LANCZOS)
    pos = [(60, 520), (390, 500), (720, 520), (60, 890), (390, 870), (720, 890)][:n]
    for x, y in pos:
        sh = Image.new('RGBA', (c.width + 40, c.height + 40), (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), (20, 28), c.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(9))
        im.alpha_composite(sh, (x - 20, y - 20)); im.alpha_composite(c, (x, y))
    return im
def austin_placeholder():
    im = Image.new('RGBA', (W, H), (18, 18, 22, 255)); d = ImageDraw.Draw(im); d.rectangle((60, 560, W - 60, 1180), outline=(90, 90, 100), width=4)
    for txt, f, y in [('ALT: YOUR CLIP', MONT(800, 56), 760), ('austin powers unfreezing', MONT(700, 46), 850)]:
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=(230, 230, 236))
    return im

E0 = ([], [], ['?']); E1 = (['jensen'], [], ['?']); E2 = (['jensen', 'nvidia staff'], [], ['?']); E2b = (['jensen', 'nvidia staff', 'ai stocks'], [], ['?'])
E3 = (['jensen', 'nvidia staff', 'ai stocks'], ['the board'], ['?']); E3b = (['jensen', 'staff · stocks', 'the lawyers'], ['the board', 'kress', 'bessent'], ['?'])
E4 = (['jensen', 'staff · stocks', 'the lawyers'], ['the board', 'kress', 'bessent'], ['nvidia', 'trump']); E5 = (['jensen', 'staff · stocks', 'the lawyers'], ['board · kress', 'bessent', 'women'], ['nvidia', 'trump', 'dems'])

BEATS = [
 (0.8, 'ON', 'hook poster', lambda t: poster(grabf(t), [('we just lived through', MONT(700, 44), INK, False), ('HISTORY', ANTON(170), BLUE, False)]), ['LIVED', 'THROUGH', 'HISTORY']),
 (2.0, 'CLIP', 'trump "sex sells" clip (you\'re sending it)', lambda t: clip_placeholder(), ['SEX', 'SELLS']),
 (3.4, 'ON', '"back in a jacket"', lambda t: poster(grabf(t), [('jensen is back', MONT(700, 44), INK, False), ('IN A JACKET', ANTON(140), BLUE, False)]), ['BACK', 'IN', 'A', 'JACKET']),
 (7.2, 'WB', 'venn draws on, empty', lambda t: venn_clear([], [], None), ['WINNERS', 'AND', 'LOSERS']),
 (10.4, 'WB', '"people in the middle" ? pops in', lambda t: venn_clear([], [], []), ['IN', 'THE', 'MIDDLE']),
 (13.0, 'WB', 'jensen written into winners', lambda t: venn_clear(['jensen'], [], []), ['OBVIOUSLY', 'JENSEN']),
 (16.5, 'WB', 'he resigned: CBS headline clip', lambda t: clip_card('CBS News · Nov 12', 'Nvidia CEO Jensen Huang resigns in wake of affair with woman suspected of spying for China', ['resigns', 'spying']), ['ALLEGED', 'SPY']),
 (26.5, 'ON', '"friends in high places"', lambda t: poster(grabf(t), [('friends in', MONT(700, 46), INK, False), ('HIGH PLACES', ANTON(140), BLUE, False)]), ['HIGHEST', 'OF', 'PLACES']),
 (30.5, 'WB', '$952B: biggest one-day gain ever (bar vs old record)', lambda t: bars('biggest one-day gains ever', [('nvidia · nov 23', 952), ('old record · microsoft', 450)], 952, unit='B', note='market value added in a single day'), ['IN', 'ONE', 'DAY']),
 (35.5, 'ON', '"not bad for a monday"', lambda t: poster(grabf(t), [('jensen got back', MONT(700, 44), INK, False), ('$33.7B', ANTON(170), BLUE, False), ('not bad for a monday', MARK(56), INK, True)]), ['NOT', 'BAD']),
 (39.2, 'WB', 'nvidia staff into winners (+31.5%)', lambda t: venn_clear(['jensen', 'nvidia staff'], [], []), ['EMPLOYEES', 'WIN']),
 (49.5, 'WB', 'ai stocks rallied: animated bars', lambda t: bars('monday\'s rally', [('IREN', 24), ('CoreWeave', 22), ('Nebius', 20), ('Oracle', 12)], 24, note=None), ['ALL', 'RALLIED']),
 (55.5, 'ON', '"the anchor"', lambda t: poster(grabf(t), [('nvidia is', MONT(700, 44), INK, False), ('THE ANCHOR', ANTON(150), BLUE, False)]), ['THE', 'ANCHOR']),
 (60.5, 'ON', 'lawyers: "billable hours"', lambda t: poster(grabf(t), [('BILLABLE', ANTON(150), BLUE, False), ('hours', MARK(80), INK, True)]), ['BILLABLE', 'HOURS']),
 (66.0, 'WB', 'losers circle: the board', lambda t: venn_clear(['jensen', 'nvidia staff', 'ai stocks', 'lawyers'], ['the board'], []), ['BIGGEST', 'LOSERS']),
 (68.8, 'WB', 'board: said no → voted yes', lambda t: timeline_quotes(('NOV 17', ['"does not intend to', 'reinstate jensen"'], '— nvidia chair harvey jones', (215, 45, 150)), ('NOV 23', ['voted unanimously', 'to reinstate him'], '— nvidia board', (30, 90, 210)), '6 days later'), ['UNANIMOUSLY', 'RESTORED']),
 (77.8, 'ON', '"purely decorative"', lambda t: poster(grabf(t), [('harvey jones:', MONT(700, 44), INK, False), ('DECORATIVE', ANTON(140), BLUE, False)]), ['PURELY', 'DECORATIVE']),
 (84.0, 'WB', 'kress: FT headline clip', lambda t: clip_card('Financial Times', 'Nvidia CFO Colette Kress kept out of secret talks over Jensen Huang\'s return', ['kept', 'out']), ['EXCLUDED']),
 (89.5, 'ON', '"your old boss at your desk"', lambda t: poster(grabf(t), [('your old boss is', MONT(700, 44), INK, False), ('BACK', ANTON(170), BLUE, False), ('at your desk', MARK(64), INK, True)]), ['YOUR', 'DESK']),
 (95.0, 'WB', 'bessent: outside → "on the outside now"', lambda t: timeline_quotes(('NOV 15', ['nvidia should "go', 'outside the company"'], '— treasury sec. scott bessent', (215, 45, 150)), ('NOV 22', ['"he\'s on the', 'outside now"'], '— on face the nation', (30, 90, 210)), '7 days later', face=bess_face()), ['OUTSIDE', 'NOW']),
 (101.0, 'ON', 'breakup line poster', lambda t: poster(grabf(t), [('a', MONT(700, 44), INK, False), ('NEW OPTION?', ANTON(130), BLUE, False), ('he\'s your ex', MARK(70), INK, True)]), ['YOUR', 'EX']),
 (105.5, 'ON', '"down bad"', lambda t: poster(grabf(t), [('corporate governance', MONT(700, 42), INK, False), ('DOWN BAD', ANTON(160), BLUE, False)]), ['DOWN', 'BAD']),
 (111.5, 'WB', 'next CEO: replacing jensen ≈ $1T', lambda t: wb_num('replacing jensen was priced at', '~$1T', 'roughly'), ['TRILLION', 'DOLLARS']),
 (114.0, 'WB', 'cloning: jensens pop up one by one', lambda t: clones(), ['CLONING']),
 (116.0, 'CLIP', 'or: austin powers unfreezing (your clip)', lambda t: austin_placeholder(), ['CRYOGENIC', 'CHAMBERS']),
 (120.5, 'WB', 'the weird middle fills: nvidia + trump', lambda t: venn_clear(['jensen', 'nvidia staff', 'ai stocks', 'lawyers'], ['the board', 'kress', 'bessent', 'governance'], ['nvidia', 'trump']), ['WEIRD', 'MIDDLE']),
 (123.5, 'ON', '"no succession plan"', lambda t: poster(grabf(t), [('NO SUCCESSION', ANTON(120), BLUE, False), ('plan', MARK(80), INK, True)]), ['SUCCESSION', 'PLAN']),
 (141.0, 'WB', 'democrats into the middle', lambda t: venn_clear(['jensen', 'nvidia staff', 'ai stocks', 'lawyers'], ['the board', 'kress', 'bessent', 'governance'], ['nvidia', 'trump', 'democrats']), ['JUICY', 'HEARINGS']),
 (149.5, 'ON', 'women: plain and serious, no jokes', lambda t: poster(grabf(t), [('no corporate', MONT(700, 52), INK, False), ('accountability', MONT(800, 72), INK, False)]), ['CORPORATE', 'ACCOUNTABILITY']),
 (161.5, 'WB', 'ending: full venn', lambda t: venn_clear(['jensen', 'nvidia staff', 'ai stocks', 'lawyers'], ['the board', 'kress', 'bessent', 'women'], ['nvidia', 'trump', 'democrats']), ['FAR', 'FROM', 'OVER']),
]
tw, th = 300, 533; cols = 7; rows = (len(BEATS) + cols - 1) // cols
sh = Image.new('RGB', (cols * (tw + 10) + 10, rows * (th + 92) + 10), (20, 20, 20)); dd = ImageDraw.Draw(sh)
for i, (t, kind, note, fn, capw) in enumerate(BEATS):
    im = fn(t); hi = max(range(len(capw)), key=lambda k: len(capw[k]))
    (inkcap if kind == 'WB' else caption)(im, capw, hi); d = ImageDraw.Draw(im)
    for yy in (250, 1560): d.line((0, yy, W, yy), fill=(255, 0, 0), width=3)
    x = 10 + (i % cols) * (tw + 10); y = 10 + (i // cols) * (th + 92); sh.paste(im.convert('RGB').resize((tw, th), Image.LANCZOS), (x, y))
    mm, ss = int(t // 60), t % 60
    dd.text((x, y + th + 6), f'{mm}:{ss:04.1f}', font=MONT(800, 22), fill=(255, 232, 0)); dd.text((x + 78, y + th + 9), {'WB': 'whiteboard', 'ON': 'on camera', 'CLIP': 'your clip'}[kind], font=MONT(600, 16), fill=(150, 200, 255) if kind == 'WB' else (200, 200, 200))
    words = note.split(); l1 = ' '.join(words[:6]); l2 = ' '.join(words[6:])
    dd.text((x, y + th + 36), l1, font=MONT(500, 16), fill=(230, 230, 230)); dd.text((x, y + th + 58), l2, font=MONT(500, 16), fill=(230, 230, 230))
sh.save(V + '/storyboard_D.png'); print(sh.size, len(BEATS))
