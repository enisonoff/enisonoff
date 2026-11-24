exec(open('sbD.py').read().split("E0 = ([], [], ['?']);")[0])
import random, math, subprocess
rr = random.Random(11)
C0, C1 = 114.7, 116.35
# pop schedule: starts slow, then floods the screen (accelerating), ending with one giant jensen
N = 34; times = [C0 + 1.25 * (k / N) ** 1.8 for k in range(N)]
spots = []
for k in range(N):
    sz = rr.uniform(230, 360) if k > 0 else 420
    x = W / 2 if k == 0 else rr.uniform(60, W - 60); y = 980 if k == 0 else rr.uniform(330, 1350)
    spots.append((times[k], x, y, sz))
GIANT_T = C0 + 1.3
def frame_at(t):
    im = dotgrid(); d = ImageDraw.Draw(im)
    for tk, x, y, sz in spots:
        if t < tk: continue
        q = (t - tk) / 0.12; sc = (0.2 + 1.0 * min(q, 1) + 0.15 * math.sin(min(q, 1) * math.pi)) if q < 1 else 1.0
        c = JC.copy(); h = int(sz * sc); c = c.resize((max(1, int(c.width * h / c.height)), max(1, h)), Image.LANCZOS)
        sh = Image.new('RGBA', (c.width + 40, c.height + 40), (0, 0, 0, 0)); sh.paste((0, 0, 0, 80), (20, 28), c.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(8))
        im.alpha_composite(sh, (int(x - c.width / 2 - 20), int(y - c.height / 2 - 20))); im.alpha_composite(c, (int(x - c.width / 2), int(y - c.height / 2)))
    if t >= GIANT_T:                                            # the punchline: one enormous jensen pops up front
        q = min((t - GIANT_T) / 0.14, 1); sc = 0.3 + 0.8 * q + 0.12 * math.sin(q * math.pi)
        c = JC.copy(); h = int(1150 * sc); c = c.resize((int(c.width * h / c.height), h), Image.LANCZOS)
        im.alpha_composite(c, (int(W / 2 - c.width / 2), int(1560 - c.height)))
    if t >= 115.22:                                             # title lands on the word "cloning"
        q = min((t - 115.22) / 0.12, 1); f = ANTON(int(170 * (0.6 + 0.4 * q + 0.1 * math.sin(q * math.pi)))); txt = 'CLONING?'
        tw = d.textlength(txt, font=f); bb = d.textbbox(((W - tw) / 2, 280), txt, font=f); d.rounded_rectangle((bb[0] - 30, bb[1] - 18, bb[2] + 30, bb[3] + 18), 26, fill=(255, 255, 255)); d.text(((W - tw) / 2, 280), txt, font=f, fill=BLUE)
    return im.convert('RGB')
# storyboard strip
ts = [114.75, 114.95, 115.15, 115.3, 115.6, 115.85, 116.05, 116.3]
strip = Image.new('RGB', (len(ts) * 230 + 10, 440), (20, 20, 20)); dd = ImageDraw.Draw(strip)
for i, t in enumerate(ts):
    strip.paste(frame_at(t).resize((220, 391), Image.LANCZOS), (10 + i * 230, 10)); dd.text((14 + i * 230, 410), f'{t - C0:+.2f}s', font=MONT(700, 20), fill=(255, 232, 0))
strip.save(V + '/clones_strip.png')
# short animatic with her audio so the timing can be heard
fps = 30; n = int((C1 - C0) * fps)
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-', '-ss', str(C0), '-t', str(C1 - C0), '-i', V + '/raw.mp4',
                      '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', V + '/clones_test.mp4'], stdin=subprocess.PIPE)
for i in range(n): p.stdin.write(frame_at(C0 + i / fps).tobytes())
p.stdin.close(); p.wait(); print('ok')
