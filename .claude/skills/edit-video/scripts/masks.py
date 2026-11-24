"""Per-frame cutout masks of Elena, for graphics that tuck behind her head/hair.
usage: U2NET_HOME=~/.u2net ~/.venvs/seg/bin/python masks.py VIDEO OUTDIR START END
Saves OUTDIR/{frame:05d}.png (360x640, frame = round(t*30) in SOURCE time). Only run it for the seconds where
something is tucked behind her; at render time upscale to 1080x1920 with a 2px blur and paste her frame over the graphic.
"""
import sys, os, subprocess
from rembg import new_session, remove
from PIL import Image
video, out, a, b = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]); os.makedirs(out, exist_ok=True)
s = new_session('u2net_human_seg')
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-i', video, '-t', str(b - a), '-vf', 'fps=30,scale=360:640', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
n = len(raw) // (360 * 640 * 3)
for i in range(n):
    im = Image.frombuffer('RGB', (360, 640), raw[i * 691200:(i + 1) * 691200]); remove(im, session=s, only_mask=True).save(f'{out}/{int(round(a * 30)) + i:05d}.png')
print('masks', n)
