exec(open('/tmp/claude-0/-home-user-enisonoff/672c1244-cc8a-569f-a9ee-237151e2864a/scratchpad/v14/optD.py').read().split("a = optD(EARLY")[0])
V = '/tmp/claude-0/-home-user-enisonoff/672c1244-cc8a-569f-a9ee-237151e2864a/scratchpad/v14'
PINK = (215, 45, 150)
def frame(t): return Image.open(f'{V}/b_{t}.png').convert('RGBA')
def mask(t): return Image.open(f'{V}/bm_{t}.png').convert('L')
def poster(im, rows, y=270): stack(im, rows, W / 2, y); return im
def tuck(t, data):
    fr = frame(t); pw, ph = 900, 760; pap = paper_sheet(pw, ph); pap.alpha_composite(venn_layer((pw, ph), pw / 2, 200, 160, *data), (0, 0))
    sh = Image.new('RGBA', (pw + 80, ph + 80), (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), (40, 50), pap.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(14))
    bg = fr.copy(); bg.alpha_composite(sh, (50, 222)); bg.alpha_composite(pap, (90, 262)); bg.paste(fr, (0, 0), mask(t).filter(ImageFilter.GaussianBlur(1.5))); return bg
def split(t, data, top=None):
    fr = frame(t).convert('RGB'); top_h = 800; im = Image.new('RGBA', (W, H), (238, 236, 232, 255))
    im.alpha_composite(top if top is not None else venn_layer((W, top_h), W / 2, 500, 235, *data, k=1.3), (0, 0))
    im.paste(fr.crop((0, 420, W, 420 + H - top_h)), (0, top_h)); ImageDraw.Draw(im).line((0, top_h, W, top_h), fill=(30, 30, 34), width=4); return im
def wb_venn(data): im = dotgrid(); im.alpha_composite(venn_layer((W, H), W / 2, 860, 265, *data, k=1.4)); return im
def wb_headline(lines, hl, src):
    im = dotgrid(); d = ImageDraw.Draw(im); f = MONT(700, 64); y = 640
    d.text((80, 560), src, font=MONT(700, 26), fill=(150, 150, 156))
    for ln in lines:
        x = 80
        for w in ln.split():
            tw = d.textlength(w + ' ', font=f)
            if w.strip(',.') in hl: d.rectangle((x - 6, y + 6, x + tw - 8, y + 74), fill=LIME)
            d.text((x, y), w, font=f, fill=INK); x += tw
        y += 84
    return im
def pills(names, y, im, big=None):
    d = ImageDraw.Draw(im); f = MONT(800, 44); x = 70; yy = y
    for n in names:
        tw = d.textlength(n, font=f) + 60
        if x + tw > W - 70: x = 70; yy += 110
        d.rounded_rectangle((x, yy, x + tw, yy + 86), 24, fill=(30, 30, 36)); d.text((x + 30, yy + 16), n, font=f, fill=WHITE); x += tw + 24
    if big: f2 = MONT(800, 120); d.text(((W - d.textlength(big, font=f2)) / 2, yy + 150), big, font=f2, fill=(20, 150, 60))
    return im

E0 = ([], [], ['?']); E1 = (['jensen'], [], ['?']); E2 = (['jensen', 'nvidia staff', 'ai stocks'], [], ['?'])
E3 = (['jensen', 'nvidia staff', 'ai stocks'], ['the board'], ['?']); E4 = (['jensen', 'nvidia staff', 'ai stocks'], ['the board', 'kress', 'bessent'], ['weird', 'middle'])
E5 = (['jensen', 'nvidia staff', 'ai stocks'], ['the board', 'kress', 'bessent'], ['nvidia', 'trump'])
HOOK = [('we just lived through', MONT(700, 44), INK, False), ('HISTORY', ANTON(170), BLUE, False)]
BESS = [('a', MONT(700, 44), INK, False), ('NEW OPTION?', ANTON(130), BLUE, False), ('he\'s your ex', MARK(70), INK, True)]
NUM = [('nvidia added', MONT(700, 44), INK, False), ('$952B*', ANTON(170), BLUE, False), ('in one day', MARK(70), INK, True)]
ECO = [('coreweave · nebius · iren · oracle', MONT(700, 36), INK, False), ('+12–24%*', ANTON(150), BLUE, False)]
BEATS = [('0:00', '0.8', 'hook'), ('0:06', '6.8', 'winners & losers + the middle'), ('0:12', '12.6', 'winner #1: jensen'), ('0:30', '30.5', '"$952B in one day"'),
         ('0:48', '48.5', 'ai stocks rallied'), ('1:06', '66', 'losers: the board'), ('1:37', '97', 'bessent breakup line'), ('2:01', '121', 'the weird middle'), ('2:41', '161', 'ending')]
CAPS = {'0.8': ['LIVED', 'THROUGH', 'HISTORY'], '6.8': ['PLUS', 'THE', 'PEOPLE'], '12.6': ['OBVIOUSLY', 'JENSEN'], '30.5': ['IN', 'ONE', 'DAY'], '48.5': ['ALL', 'RALLIED'],
        '66': ['THE', 'BIGGEST', 'LOSERS'], '97': ['YOUR', 'EX'], '121': ['THE', 'WEIRD', 'MIDDLE'], '161': ['FAR', 'FROM', 'OVER']}
def cap(im, t, ink=False):
    w = CAPS[t]; hi = max(range(len(w)), key=lambda k: len(w[k]))
    (inkcap if ink else caption)(im, w, hi); return im

def option_D(t):
    if t == '0.8': return cap(poster(frame(t), HOOK), t)
    if t == '6.8': return cap(wb_venn(E0), t, True)
    if t == '12.6': return cap(wb_venn(E1), t, True)
    if t == '30.5': return cap(wb_headline(['Nvidia adds nearly', '$1 trillion in value', 'as Huang returns'], ['$1', 'trillion'], 'EXAMPLE · real headline screenshot goes here'), t, True)
    if t == '48.5': im = dotgrid(); return cap(pills(['CoreWeave', 'Nebius', 'IREN', 'Oracle'], 560, im, '+12–24%*'), t, True)
    if t == '66': return cap(wb_venn(E3), t, True)
    if t == '97': return cap(poster(frame(t), BESS), t)
    if t == '121': return cap(wb_venn(E4), t, True)
    return cap(wb_venn(E5), t, True)
def option_C(t):
    if t == '0.8': return cap(poster(frame(t), HOOK), t)
    if t == '6.8': return cap(split(t, E0), t)
    if t == '12.6': return cap(split(t, E1), t)
    if t == '30.5': return cap(poster(frame(t), NUM), t)
    if t == '48.5':
        top = Image.new('RGBA', (W, 800), (238, 236, 232, 255)); pills(['CoreWeave', 'Nebius', 'IREN', 'Oracle'], 280, top, '+12–24%*'); return cap(split(t, None, top), t)
    if t == '66': return cap(split(t, E3), t)
    if t == '97': return cap(poster(frame(t), BESS), t)
    if t == '121': return cap(split(t, E4), t)
    return cap(split(t, E5), t)
def option_A(t):
    data = {'0.8': E0, '6.8': E0, '12.6': E1, '30.5': E1, '48.5': E2, '66': E3, '97': E4, '121': E4, '161': E5}[t]
    im = tuck(t, data)
    return cap(im, t)

opts = [('D · WHITEBOARD (Pooja-style): full-screen cutaways for the venn, headlines, logos', option_D),
        ('C · SPLIT SCREEN: venn panel on top only when it changes', option_C),
        ('A · PAPER BEHIND YOUR HEAD: the venn stays up the whole video', option_A)]
tw, th = 250, 444
sh = Image.new('RGB', (9 * (tw + 8) + 12, 3 * (th + 110) + 10), (20, 20, 20)); dd = ImageDraw.Draw(sh)
for r, (lab, fn) in enumerate(opts):
    y0 = 10 + r * (th + 110); dd.text((12, y0), lab, font=MONT(800, 26), fill=(255, 232, 0))
    for c, (ts, t, note) in enumerate(BEATS):
        im = fn(t); d = ImageDraw.Draw(im)
        for yy in (250, 1560): d.line((0, yy, W, yy), fill=(255, 0, 0), width=3)
        x = 12 + c * (tw + 8); sh.paste(im.convert('RGB').resize((tw, th), Image.LANCZOS), (x, y0 + 40))
        dd.text((x, y0 + 46 + th), ts, font=MONT(800, 20), fill=(255, 255, 255)); dd.text((x + 52, y0 + 48 + th), note, font=MONT(500, 15), fill=(200, 200, 200))
sh.save(V + '/storyboard_options.png'); print(sh.size)
