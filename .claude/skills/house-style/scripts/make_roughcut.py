"""Rough cut for the house style: push-ins that start/end exactly on cuts, voice levelled to -14 LUFS.
usage: python3 make_roughcut.py WORKDIR/cut.mov WORKDIR/plan.json OUT.mp4 "24.3-26.9@1.15" "26.9-32.1@1.3"
Each push is START-END@ZOOM in cut seconds. Ends within 0.25 s of a cut snap onto it: a push that runs a few
frames past a cut flashes the next shot zoomed in (the "weird frame" on the outage video)."""
import sys, json, subprocess
mov, plan, out, pushes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
P = json.load(open(plan)); bounds, c = [], 0
for k, a, b in P: bounds.append(c / 30); c += b - a
bounds.append(c / 30)
snap = lambda x: min(bounds, key=lambda y: abs(y - x)) if min(abs(y - x) for y in bounds) < 0.25 else x
fl, last = [f'[0:v]split={len(pushes) + 1}[base]' + ''.join(f'[z{i}]' for i in range(len(pushes)))], 'base'
for i, p in enumerate(pushes):
    rng, z = p.split('@'); a, b = map(float, rng.split('-')); a, b, z = snap(a), snap(b), float(z)
    fl.append(f'[z{i}]crop=iw/{z}:ih/{z}:(iw-iw/{z})/2:(ih-ih/{z})/2.6,scale=1080:1920[p{i}]')
    fl.append(f"[{last}][p{i}]overlay=0:0:enable='between(t,{a:.3f},{b - 0.001:.3f})'[v{i}]"); last = f'v{i}'
    print(f'push {z}x {a:.3f}-{b:.3f}')
fl.append('[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mov, '-filter_complex', ';'.join(fl), '-map', f'[{last}]', '-map', '[a]', '-c:v', 'libx264', '-crf', '14',
                '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', out], check=True); print('wrote', out)
