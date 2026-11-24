exec(open('mock.py').read().split('frames = []')[0])
from PIL import ImageChops, ImageOps
exec(open('paper.py').read().split('def paper_venn')[0].split("exec(open('mock.py')")[1].split('\n',1)[1])  # paper_sheet()
LB, LP = (196, 222, 255), (255, 200, 240)
def venn_layer(size, cx, cy, r, winners, losers, middle, k=1.0):
    w, h = size; a = Image.new('RGB', size, (255, 255, 255)); b = Image.new('RGB', size, (255, 255, 255))
    cxl, cxr = cx - r * 0.79, cx + r * 0.79
    ImageDraw.Draw(a).ellipse((cxl - r, cy - r, cxl + r, cy + r), fill=LB); ImageDraw.Draw(b).ellipse((cxr - r, cy - r, cxr + r, cy + r), fill=LP)
    fill = ImageChops.multiply(a, b); m = Image.new('L', size, 0); md = ImageDraw.Draw(m)
    md.ellipse((cxl - r, cy - r, cxl + r, cy + r), fill=230); md.ellipse((cxr - r, cy - r, cxr + r, cy + r), fill=230)
    lay = Image.new('RGBA', size, (0, 0, 0, 0)); lay.paste(fill, (0, 0), m); d = ImageDraw.Draw(lay)
    d.ellipse((cxl - r, cy - r, cxl + r, cy + r), outline=(110, 170, 250), width=3); d.ellipse((cxr - r, cy - r, cxr + r, cy + r), outline=(245, 120, 210), width=3)
    def ct(s, x, y, f, col=(40, 40, 48)): d.text((x - d.textlength(s, font=f) / 2, y), s, font=f, fill=col)
    ct('winners', cxl - r * 0.2, cy - r * 0.8, MONT(800, int(40 * k)), (30, 90, 210)); ct('losers', cxr + r * 0.2, cy - r * 0.8, MONT(800, int(40 * k)), (210, 40, 150))
    nf = MONT(600, int(36 * k)); lh = int(50 * k)
    for i, n in enumerate(winners): ct(n, cxl - r * 0.3, cy - r * 0.42 + i * lh, nf)
    for i, n in enumerate(losers): ct(n, cxr + r * 0.3, cy - r * 0.42 + i * lh, nf)
    for i, n in enumerate(middle): ct(n, cx, cy + r * 0.15 + i * int(38 * k), MONT(700, int(30 * k)))
    return lay
EARLY = (['jensen', 'nvidia staff', 'ai stocks'], [], ['?']); FULL = (['jensen', 'nvidia staff', 'ai stocks'], ['the board', 'kress', 'bessent'], ['weird', 'middle'])

def opt_tuck(t, data):
    fr = Image.open(f'f{t}.png').convert('RGBA'); mask = Image.open(f'm{t}.png').convert('L')
    pw, ph = 900, 760; pap = paper_sheet(pw, ph); pap.alpha_composite(venn_layer((pw, ph), pw / 2, 200, 160, *data), (0, 0))
    sh = Image.new('RGBA', (pw + 80, ph + 80), (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), (40, 50), pap.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(14))
    bg = fr.copy(); bg.alpha_composite(sh, (90 - 40, 262 - 40)); bg.alpha_composite(pap, (90, 262))
    soft = mask.filter(ImageFilter.GaussianBlur(1.5)); bg.paste(fr, (0, 0), soft)   # her on top: the paper tucks behind her head
    return bg
def opt_zoom(t, data):
    fr = Image.open(f'f{t}.png').convert('RGB'); sc = 0.76; vw, vh = int(W * sc), int(H * sc)
    bg = fr.resize((27, 48)).filter(ImageFilter.GaussianBlur(8)).resize((W, H), Image.BICUBIC)
    top = fr.crop((0, 0, W, 60)).resize((W, H - vh + 60), Image.BILINEAR)              # extend the plain wall upward
    bg.paste(top, (0, 0)); small = fr.resize((vw, vh), Image.LANCZOS)
    edge = Image.new('L', (vw, vh), 255); ed = ImageDraw.Draw(edge)
    for i in range(40): ed.rectangle((i, i, vw - 1 - i, vh - 1 - i), outline=int(255 * i / 40))
    bg.paste(small, ((W - vw) // 2, H - vh), edge); im = bg.convert('RGBA')
    im.alpha_composite(venn_layer((W, H), W / 2, 500, 235, *data, k=1.25)); return im
def opt_split(t, data):
    fr = Image.open(f'f{t}.png').convert('RGB'); top_h = 800
    im = Image.new('RGBA', (W, H), (238, 236, 232, 255))
    im.alpha_composite(venn_layer((W, top_h), W / 2, 500, 235, *data, k=1.3), (0, 0))
    her = fr.crop((0, 420, W, 420 + H - top_h)); im.paste(her, (0, top_h)); ImageDraw.Draw(im).line((0, top_h, W, top_h), fill=(30, 30, 34), width=4)
    return im

rows = [('A · paper pinned behind your head', opt_tuck), ('B · zoom out for more wall', opt_zoom), ('C · split screen', opt_split)]
sh = Image.new('RGB', (2 * 370 + 470, 3 * 670 + 10), (20, 20, 20)); dd = ImageDraw.Draw(sh)
for r_, (lab, fn) in enumerate(rows):
    for c, (t, data, cap) in enumerate([(30, EARLY, ['THE', 'BIGGEST', 'WINNER']), (120, FULL, ['THE', 'WEIRD', 'MIDDLE'])]):
        im = fn(t, data)
        if fn is opt_split:
            d0 = ImageDraw.Draw(im); f = MONT(800, 54); sp = d0.textlength(' ', font=f); tw = sum(d0.textlength(w, font=f) for w in cap) + sp * 2; x = (W - tw) / 2
            for k, w in enumerate(cap):
                for dx, dy in [(0, 4), (2, 3), (-2, 3)]: d0.text((x + dx, 1480 + dy), w, font=f, fill=(0, 0, 0))
                d0.text((x, 1480), w, font=f, fill=YEL if k == 1 else WHITE); x += d0.textlength(w, font=f) + sp
        else: caption(im, cap, 1); d = ImageDraw.Draw(im)
        for yy in (250, 1560): d.line((0, yy, W, yy), fill=(255, 0, 0), width=3)
        sh.paste(im.convert('RGB').resize((360, 640), Image.LANCZOS), (10 + c * 370, 10 + r_ * 670))
    dd.text((760, 30 + r_ * 670), lab, font=MONT(700, 26), fill=(240, 240, 240))
sh.save(V + '/options.png'); print('ok')
