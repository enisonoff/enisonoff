exec(open('options.py').read().split("rows = [")[0])
def dotgrid():
    im = Image.new('RGBA', (W, H), (250, 250, 248, 255)); d = ImageDraw.Draw(im)
    for y in range(20, H, 36):
        for x in range(20, W, 36): d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(214, 214, 214))
    return im
LIME = (212, 245, 66)
def inkcap(im, words, hi):
    d = ImageDraw.Draw(im); f = MONT(800, 54); sp = d.textlength(' ', font=f)
    tw = sum(d.textlength(w, font=f) for w in words) + sp * (len(words) - 1); x = (W - tw) / 2; y = 1380
    for k, w in enumerate(words):
        if k == hi: d.rectangle((x - 8, y + 4, x + d.textlength(w, font=f) + 8, y + 66), fill=LIME)
        d.text((x, y), w, font=f, fill=INK); x += d.textlength(w, font=f) + sp
def optD(data, cap, hl_word=None):
    im = dotgrid(); im.alpha_composite(venn_layer((W, H), W / 2, 860, 265, *data, k=1.4))
    inkcap(im, cap, 1); return im
def headline(lines, hl):
    im = dotgrid(); d = ImageDraw.Draw(im); f = MONT(700, 64); y = 640
    d.text((80, 560), 'EXAMPLE · the real headline screenshot goes here', font=MONT(700, 26), fill=(150, 150, 156))
    for ln in lines:
        x = 80
        for w in ln.split():
            tw = d.textlength(w + ' ', font=f)
            if w.strip(',.') in hl: d.rectangle((x - 6, y + 6, x + tw - 8, y + 74), fill=LIME)
            d.text((x, y), w, font=f, fill=INK); x += tw
        y += 84
    inkcap(im, ['IN', 'ONE', 'DAY'], 2); return im
a = optD(EARLY, ['THE', 'BIGGEST', 'WINNER']); b = optD(FULL, ['THE', 'WEIRD', 'MIDDLE'])
c = headline(['Nvidia adds nearly', '$1 trillion in value', 'as Huang returns'], ['$1', 'trillion'])
sh = Image.new('RGB', (3 * 370 + 10, 670), (20, 20, 20))
for i, im in enumerate([a, b, c]):
    d = ImageDraw.Draw(im)
    for yy in (250, 1560): d.line((0, yy, W, yy), fill=(255, 0, 0), width=3)
    sh.paste(im.convert('RGB').resize((360, 640), Image.LANCZOS), (10 + i * 370, 10))
sh.save(V + '/optionD.png'); print('ok')
