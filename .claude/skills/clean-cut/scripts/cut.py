"""Cut a talking-head video from an edit list: keep chosen spans, tighten pauses, frame-accurate, in sync.
usage: python cut.py EDL.json plan|audio|render

EDL.json:
{
  "workdir": "/path/to/work",                     # holds the clips' .wav (48 kHz mono) and .mov, and the outputs
  "clips": {"a": {"video": "a.mov", "wav": "a.wav", "offset": 0.077}},   # offset = audio start_time from ffprobe
  "maxgap": 0.06,                                 # longest pause left between words (s)
  "segs": [["a", 6.04, [11.98, 12.14], "So why is everything... finding holes"], ...]
}
Each seg: clip, start, end, note. A number is an exact edge (audio time, checked with zones.py);
a [lo, hi] pair means "cut at the quietest 10 ms in that window".
Outputs: cut.wav (audio only) / cut.mov (video, CRF 14, PCM audio) in workdir.
"""
import sys, json, wave, subprocess
import numpy as np

E = json.load(open(sys.argv[1])); MODE = sys.argv[2]
V = E['workdir']; SR = 48000; FPS = 30; HOP = 480
SIL_DB = -47.0          # stricter than speech threshold so quiet consonants/soft words are never treated as silence
MAXGAP = E.get('maxgap', 0.06)
MIN_PAUSE = MAXGAP + 0.06   # only pauses longer than this get shortened
PAD = 0.01

def load(path):
    w = wave.open(path); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    m = len(x) // HOP; db = 20 * np.log10(np.sqrt((x[:m * HOP].reshape(m, HOP) ** 2).mean(1)) + 1e-9)
    return x, db
CL = E['clips']; AUD = {k: load(f"{V}/{c['wav']}") for k, c in CL.items()}

def edge(k, v):
    if not isinstance(v, (list, tuple)): return v
    db = AUD[k][1]; a, b = int(v[0] * 100), int(v[1] * 100); return (a + int(np.argmin(db[a:b]))) / 100

def tighten(k, s, e):
    db = AUD[k][1]; a, b = int(s * 100), int(e * 100); out = []; cur = s; run = None
    for i in range(a, b):
        quiet = db[i] <= SIL_DB
        if quiet and run is None: run = i
        if (not quiet or i == b - 1) and run is not None:
            if (i - run) / 100 > MIN_PAUSE and run > a:
                out.append((cur, run / 100 + MAXGAP / 2 + PAD)); cur = i / 100 - MAXGAP / 2 - PAD
            run = None
    out.append((cur, e)); return [(x, y) for x, y in out if y - x > 0.04]

EDGE_DB = -42.0   # speech onset/offset for trimming dead air at segment joins
def trim_edges(k, s, e):
    """Pull a segment's start/end in to the first/last speech, keeping a short lead (0.04 s) and tail (0.07 s).
    Removes the breaths and pauses that pile up at joins ("make it snappier")."""
    db = AUD[k][1]; a, b = int(s * 100), int(e * 100)
    i = a
    while i < b and db[i] <= EDGE_DB: i += 1
    j = b - 1
    while j > i and db[j] <= EDGE_DB: j -= 1
    if j <= i: return s, e
    return max(s, i / 100 - 0.04), min(e, (j + 1) / 100 + 0.07)

def plan():
    P = []
    for seg in E['segs']:
        k, s, e = seg[0], edge(seg[0], seg[1]), edge(seg[0], seg[2])
        if E.get('trim_edges'): s, e = trim_edges(k, s, e)
        for x, y in tighten(k, s, e):
            f0 = int(round((x + CL[k]['offset']) * FPS)); f1 = int(round((y + CL[k]['offset']) * FPS))
            if f1 <= f0: continue
            a_, b_ = int(x * 100), int(y * 100)
            if f1 - f0 < 10 and AUD[k][1][a_:max(b_, a_ + 1)].max() < -36: continue   # stray noise blip
            P.append((k, f0, f1))
    return P

P = plan(); json.dump(P, open(f'{V}/plan.json', 'w'))
print('pieces', len(P), 'duration', round(sum(f1 - f0 for _, f0, f1 in P) / FPS, 2))
if MODE in ('audio', 'render'):
    out, fade = [], int(0.004 * SR)
    for k, f0, f1 in P:
        x = AUD[k][0]; a0 = int((f0 / FPS - CL[k]['offset']) * SR); a1 = a0 + (f1 - f0) * (SR // FPS)
        seg = np.zeros(a1 - a0, np.float32); src = x[max(0, a0):max(0, a1)]; seg[len(seg) - len(src):] = src[:len(seg)]
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade); out.append(seg)
    y = np.concatenate(out); wv = wave.open(f'{V}/cut.wav', 'wb'); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
    wv.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); wv.close(); print('wrote cut.wav')
if MODE == 'render':
    W, H = 1080, 1920; fs = W * H * 3
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-i', f'{V}/cut.wav',
                            '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', f'{V}/cut.mov'], stdin=subprocess.PIPE)
    rd = {k: subprocess.Popen(['ffmpeg', '-v', 'error', '-i', f"{V}/{c['video']}", '-vf', f'fps=30,scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                              stdout=subprocess.PIPE) for k, c in CL.items()}
    pos = {k: 0 for k in CL}
    for k, f0, f1 in P:       # pieces must be in increasing order within each clip (they are, for a linear edit)
        assert f0 >= pos[k], f'clip {k} goes backwards at frame {f0}; split it into a second clip entry'
        while pos[k] < f0: rd[k].stdout.read(fs); pos[k] += 1
        for _ in range(f0, f1): enc.stdin.write(rd[k].stdout.read(fs)); pos[k] += 1
    enc.stdin.close(); enc.wait(); [r.kill() for r in rd.values()]; print('wrote cut.mov')
