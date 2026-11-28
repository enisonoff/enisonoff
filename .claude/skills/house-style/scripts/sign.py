"""WARNING / BEWARE OF AI MODEL sign in the style of a stock 'beware of dog' sign (her reference)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
F = os.environ.get('REEL_FONTS') or os.path.join(os.path.dirname(os.environ['REEL_DIR']), 'fonts')
BLK = lambda n: ImageFont.truetype(f'{F}/archivo-black/package/files/archivo-black-latin-400-normal.woff', n)
def center(d, cx, cy, text, font, fill):
    bb = d.textbbox((0, 0), text, font=font); d.text((cx - (bb[0] + bb[2]) / 2, cy - (bb[1] + bb[3]) / 2), text, font=font, fill=fill)
def sign(w=900):
    h = int(w * 2 / 3); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = int(w * 0.05)
    d.rounded_rectangle([0, 0, w - 1, h - 1], r, fill=(255, 255, 255)); m = int(w * 0.025)
    d.rounded_rectangle([m, m, w - 1 - m, h - 1 - m], r - m // 2, fill=(15, 15, 15))
    b = int(w * 0.012); band = int(h * 0.34)
    d.rounded_rectangle([m + b, m + band, w - 1 - m - b, h - 1 - m - b], r - m, fill=(255, 255, 255))
    d.rectangle([m + b, m + band, w - 1 - m - b, m + band + r], fill=(255, 255, 255))
    ow, oh = w * 0.66, band * 0.62; cx, cy = w / 2, m + band / 2 + b
    d.ellipse([cx - ow / 2 - 8, cy - oh / 2 - 8, cx + ow / 2 + 8, cy + oh / 2 + 8], fill=(255, 255, 255))
    d.ellipse([cx - ow / 2, cy - oh / 2, cx + ow / 2, cy + oh / 2], fill=(226, 30, 36))
    center(d, cx, cy, 'WARNING', BLK(int(h * 0.12)), (255, 255, 255))
    body = h - m - band; center(d, cx, m + band + body * 0.30, 'BEWARE', BLK(int(h * 0.15)), (10, 10, 10))
    center(d, cx, m + band + body * 0.68, 'OF AI MODEL', BLK(int(h * 0.15)), (10, 10, 10))
    for x in (w * 0.5,):                        # mounting bolts like the reference
        d.ellipse([x - 7, m + 8, x + 7, m + 22], fill=(170, 170, 170)); d.ellipse([x - 7, h - m - 24, x + 7, h - m - 10], fill=(170, 170, 170))
    return im
if __name__ == '__main__': sign().save('sign_test.png')

def fence_scene(t=0.0, W=1080, H=1920):
    """Black and white: soft-focus columned facade behind, iron fence with spear tops in front, sign on the bars."""
    import numpy as np
    bg = Image.new('L', (W, H), 175); d = ImageDraw.Draw(bg)
    d.rectangle([0, 0, W, 560], fill=150)                                 # sky
    d.rectangle([0, 560, W, 1350], fill=222)                              # facade
    d.polygon([(40, 560), (W - 40, 560), (W / 2, 380)], fill=214)         # pediment
    d.rectangle([20, 540, W - 20, 600], fill=232)                         # cornice
    for i in range(7):
        x = 90 + i * 150; d.rectangle([x, 620, x + 46, 1300], fill=238); d.rectangle([x + 46, 620, x + 58, 1300], fill=190)
    for i in range(6):
        x = 160 + i * 150; d.rectangle([x, 760, x + 52, 860], fill=120); d.rectangle([x, 1040, x + 52, 1140], fill=120)   # windows
    d.rectangle([0, 1350, W, H], fill=95)                                 # lawn
    bg = bg.filter(ImageFilter.GaussianBlur(14)).convert('RGBA')
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f = ImageDraw.Draw(fg)
    f.rectangle([0, 820, W, 846], fill=(18, 18, 18)); f.rectangle([0, 1480, W, 1510], fill=(18, 18, 18))   # rails
    for x in range(-20, W + 40, 92):
        f.rectangle([x, 760, x + 20, 1760], fill=(20, 20, 20)); f.polygon([(x - 8, 770), (x + 28, 770), (x + 10, 700)], fill=(20, 20, 20))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sg = sign(820)
    m = sg.getchannel('A'); sh.paste(Image.new('RGBA', sg.size, (0, 0, 0, 170)), (148, 948), m); sh = sh.filter(ImageFilter.GaussianBlur(14))
    out = Image.alpha_composite(bg, fg); out = Image.alpha_composite(out, sh); out.alpha_composite(sg, (130, 920))
    for x in (300, 780): ImageDraw.Draw(out).rectangle([x, 900, x + 14, 940], fill=(60, 60, 60))           # brackets
    a = np.asarray(out.convert('RGB'), np.float32) / 255; lum = (a * [0.299, 0.587, 0.114]).sum(2, keepdims=True)
    keep = (a[..., 0:1] - a[..., 1:2] > 0.25)                             # keep the red WARNING oval in color
    a = np.where(keep, a, lum); a = 0.5 + (a - 0.5) * 1.1
    yy, xx = np.mgrid[0:H, 0:W]; v = 1 - 0.5 * (((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H * 0.5) / (H * 0.65)) ** 2)
    a = a * np.clip(v, 0.45, 1)[..., None] + np.random.default_rng(int(t * 30)).normal(0, 0.025, a.shape)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
if __name__ == '__main__': fence_scene().save('fence_test.png')
