"""US and PRC flags drawn from their official proportions, side by side, slight wave, for the America-vs-China beat."""
import math, numpy as np
from PIL import Image, ImageDraw
def star(d, cx, cy, r, rot=0, fill=(255, 255, 255)):
    pts = []
    for i in range(10):
        a = rot - math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.382
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)
def us(h=600):
    w = int(h * 1.9); im = Image.new('RGB', (w, h), (255, 255, 255)); d = ImageDraw.Draw(im); sh = h / 13
    for i in range(0, 13, 2): d.rectangle([0, i * sh, w, (i + 1) * sh], fill=(178, 34, 52))
    cw, ch = w * 0.4, sh * 7; d.rectangle([0, 0, cw, ch], fill=(60, 59, 110))
    for r in range(9):
        for c in range(6 if r % 2 == 0 else 5):
            x = cw / 12 * (2 * c + 1 + (r % 2)); y = ch / 10 * (r + 1); star(d, x, y, h * 0.0616 / 2 * 0.95)
    return im
def cn(h=600):
    w = int(h * 1.5); im = Image.new('RGB', (w, h), (238, 28, 37)); d = ImageDraw.Draw(im); u = h / 20
    star(d, 5 * u, 5 * u, 3 * u, fill=(255, 255, 0))
    for (x, y) in [(10, 2), (12, 4), (12, 7), (10, 9)]:
        rot = math.atan2(5 - y, 5 - x) + math.pi / 2; star(d, x * u, y * u, u, rot, fill=(255, 255, 0))
    return im
def wave(im, amp=14, phase=0.0):
    a = np.asarray(im); h, w, _ = a.shape; out = np.zeros((h + 2 * amp, w, 3), np.uint8); shade = np.zeros(w)
    for x in range(w):
        s = math.sin(x / w * 2 * math.pi * 1.3 + phase); dy = int(amp * s); out[amp + dy:amp + dy + h, x] = a[:, x]; shade[x] = 0.85 + 0.15 * math.cos(x / w * 2 * math.pi * 1.3 + phase)
    out = (out * shade[None, :, None]).clip(0, 255).astype(np.uint8); m = np.zeros((h + 2 * amp, w), np.uint8)
    for x in range(w): dy = int(amp * math.sin(x / w * 2 * math.pi * 1.3 + phase)); m[amp + dy:amp + dy + h, x] = 255
    o = Image.fromarray(out).convert('RGBA'); o.putalpha(Image.fromarray(m)); return o
def frame(t=0.0, W=1080, H=1920):
    bg = Image.new('RGBA', (W, H), (12, 12, 12, 255))
    a = wave(us(300).resize((540, 284)), 12, t * 5); b = wave(cn(300).resize((426, 284)), 12, t * 5 + 1)
    bg.alpha_composite(a, (270, 560)); bg.alpha_composite(b, (327, 1000)); return bg
if __name__ == '__main__': frame().save('flags_test.png')
