exec(open('mock.py').read().split('frames = []')[0])
def paper_sheet(w, h, seed=5):
    rr = random.Random(seed); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # torn top edge, straight sides
    top = [(0, 26)] + [(x, 14 + rr.uniform(-9, 9)) for x in range(0, w + 1, 14)] + [(w, 26)]
    d.polygon(top + [(w, h), (0, h)], fill=(252, 250, 244, 255))
    for y in range(110, h, 46): d.line((0, y, w, y), fill=(170, 200, 230, 255), width=2)      # ruled lines
    d.line((70, 20, 70, h), fill=(240, 150, 150, 255), width=2)                                # margin
    tex = Image.effect_noise((w, h), 10).convert('L').point(lambda v: 255 - abs(v - 128) // 6)
    a = im.split()[3]; base = im.convert('RGB'); base = Image.composite(Image.merge('RGB', [Image.eval(c, lambda v: v) for c in base.split()]), base, tex.point(lambda v: 0))
    im = Image.merge('RGBA', (*base.split(), a)); return im
def paper_venn(fr, full=True):
    pw, ph = 860, 640; pap = paper_sheet(pw, ph); d = ImageDraw.Draw(pap)
    cxl, cxr, cy, r = 300, 560, 360, 210
    wobbly_circle(d, cxl, cy, r, BLUE, width=8, seed=1); wobbly_circle(d, cxr, cy, r, (235, 40, 90), width=8, seed=2)
    d.text((cxl - 150, cy - r - 70), 'winners', font=MARK(50), fill=BLUE); d.text((cxr + 10, cy - r - 70), 'losers', font=MARK(50), fill=(235, 40, 90))
    for i, n in enumerate(['jensen', 'nvidia staff', 'coreweave etc', 'the lawyers']): d.text((cxl - 170, cy - 100 + i * 52), n, font=CAV(46), fill=INK)
    for i, n in enumerate(['the board', 'kress', 'bessent']): d.text((cxr - 10, cy - 100 + i * 52), n, font=CAV(46), fill=INK)
    d.text((cxl + 98, cy + 80), 'weird', font=CAV(38), fill=INK); d.text((cxl + 90, cy + 116), 'middle', font=CAV(38), fill=INK)
    sh = Image.new('RGBA', (pw + 80, ph + 80), (0, 0, 0, 0)); sh.paste((0, 0, 0, 110), (40, 52), pap.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(16))
    fr.alpha_composite(sh, ((W - pw) // 2 - 40, 255 - 40)); fr.alpha_composite(pap, ((W - pw) // 2, 255)); return fr
a = Image.open(V + '/f70.png').convert('RGBA'); paper_venn(a); caption(a, ['THE', 'BIGGEST', 'LOSERS'], 1)
b = Image.open(V + '/f120.png').convert('RGBA'); venn(b, prog=1.0, names=True); caption(b, ['THE', 'WEIRD', 'MIDDLE'], 1)
sh = Image.new('RGB', (2 * 520 + 10, 960), (20, 20, 20)); dd = ImageDraw.Draw(sh)
for i, (fr, lab) in enumerate([(a, 'on paper (section turns)'), (b, 'marker on the wall (current)')]):
    d = ImageDraw.Draw(fr)
    for yy in (250, 1560): d.line((0, yy, W, yy), fill=(255, 0, 0), width=3)
    sh.paste(fr.convert('RGB').resize((510, 907), Image.LANCZOS), (10 + i * 520, 10)); dd.text((14 + i * 520, 925), lab, font=MONT(600, 20), fill=(230, 230, 230))
sh.save(V + '/paper_vs_wall.png'); print('ok')
