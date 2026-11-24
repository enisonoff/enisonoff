"""Post-render checks. Run on every render before sending it to Elena.
usage: python3 check_render.py RENDER.mp4 RAW.mp4 [out_t:src_t ...]
1. flashes: any shot shorter than 8 frames (the "glitch" she noticed twice) -> must be []
2. sync: for each out_t:src_t pair, finds the frame offset between render and source; must be within 1 frame (0.033 s).
   Pass pairs that account for any cuts (e.g. after a 2.03 s cut at 139, out 150 = src 152.03).
"""
import sys, subprocess, numpy as np
out, raw = sys.argv[1], sys.argv[2]
b = subprocess.run(['ffmpeg', '-v', 'error', '-i', out, '-vf', 'scale=27:48', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
f = np.frombuffer(b, np.uint8).reshape(-1, 48, 27).astype(int); cuts = [i for i in range(1, len(f)) if abs(f[i] - f[i - 1]).mean() > 25]
print('frames', len(f), '| short flashes:', [round(cuts[k] / 30, 2) for k in range(len(cuts) - 1) if cuts[k + 1] - cuts[k] < 8])
def fr(fn, t):
    x = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', fn, '-frames:v', '1', '-vf', 'scale=54:96', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
    return np.frombuffer(x, np.uint8).astype(int)
for pair in sys.argv[3:] or ['20:20', '60:60']:
    to, ts = map(float, pair.split(':')); a = fr(out, to)
    print('sync', pair, 'offset', min((abs(a - fr(raw, ts + o)).mean(), round(o, 3)) for o in [x / 30 for x in range(-6, 7)])[1])
