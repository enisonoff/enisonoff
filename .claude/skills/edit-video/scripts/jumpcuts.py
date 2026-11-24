"""Find the jump cuts already in Elena's footage (she edits before sending).
usage: python3 jumpcuts.py VIDEO > jumpcuts.txt      (space-separated seconds, source time)
Every graphic must start/end ON one of these (if one is within 0.45 s), or two cuts land a few frames apart and it looks like a glitch.
"""
import sys, subprocess, numpy as np
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-vf', 'fps=30,scale=54:96', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
prev, i, cuts = None, 0, []
while True:
    b = p.stdout.read(54 * 96)
    if len(b) < 54 * 96: break
    f = np.frombuffer(b, np.uint8).astype(int)
    if prev is not None and abs(f - prev).mean() > 14: cuts.append(round(i / 30, 2))
    prev = f; i += 1
print(' '.join(map(str, cuts)))
