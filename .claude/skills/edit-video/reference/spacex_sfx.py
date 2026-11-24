"""Synthesized SFX bed, placed by source time and mapped through the edit's keep-list.
usage: python3 sfx.py full|preview  -> writes sfx_full.wav / sfx_preview.wav
Each sound is generated (no samples), varied in pitch/length so nothing repeats exactly.
"""
import sys, wave, numpy as np
SR = 48000
rng = np.random.default_rng(3)
FULL = [(0.0, 173.73)]
PREV = [(3.0, 22.0), (62.0, 77.0), (83.0, 89.0), (107.0, 118.0), (166.0, 173.73)]
keep = FULL if sys.argv[1] == 'full' else PREV
def s2o(t):
    o = 0
    for a, b in keep:
        if a <= t <= b: return o + t - a
        o += b - a
    return None
DUR = sum(b - a for a, b in keep)
out = np.zeros((int(DUR * SR) + SR, 2))

def env(n, att, rel, shape=2.0):
    e = np.ones(n); a = int(att * SR); r = int(rel * SR)
    if a: e[:a] = np.linspace(0, 1, a) ** shape
    if r: e[-r:] *= np.linspace(1, 0, r) ** shape
    return e
def lp(x, k):                      # cheap one-pole lowpass, k in (0,1): smaller = darker
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += k * (v - acc); y[i] = acc
    return y
def noise(n): return rng.standard_normal(n)
def pan(x, p=0.0): return np.stack([x * (1 - max(p, 0)), x * (1 + min(p, 0))], 1)

def whoosh(dur=0.7, bright=0.12, peak=0.6):
    n = int(dur * SR); x = noise(n)
    # sweep the filter: dark -> bright -> dark
    ks = bright * (0.25 + 0.75 * np.sin(np.linspace(0, np.pi, n)) ** 1.5)
    y = np.empty(n); acc = 0.0
    for i in range(n): acc += ks[i] * (x[i] - acc); y[i] = acc
    return y * env(n, dur * peak, dur * (1 - peak), 1.6)
def swell(dur=1.4, base=60):     # soft airy space swell with a low hum
    n = int(dur * SR); t = np.arange(n) / SR
    air = lp(noise(n), 0.03) * 2.2; hum = np.sin(2 * np.pi * base * t) * 0.35 + np.sin(2 * np.pi * base * 1.5 * t) * 0.12
    return (air + hum) * env(n, dur * 0.55, dur * 0.45, 1.3)
def impact(f0=70, dur=0.7):
    n = int(dur * SR); t = np.arange(n) / SR; f = f0 * (1 + 1.6 * np.exp(-t * 18))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)
    click = lp(noise(n), 0.4) * np.exp(-t * 60) * 0.6
    return body + click
def pop(f=720, dur=0.09):
    n = int(dur * SR); t = np.arange(n) / SR; fr = f * (1 + 0.8 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 45)
def tick(f=2200, dur=0.03):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * 0.6 + lp(noise(n), 0.5) * 0.4) * np.exp(-t * 160)
def chime(f=1320, dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * m * t) * a for m, a in [(1, 1), (2.01, 0.35), (3.02, 0.15)]) * np.exp(-t * 3.2) * env(n, 0.005, 0.2)
def fwump(dur=0.45):
    n = int(dur * SR); t = np.arange(n) / SR
    return (lp(noise(n), 0.06) * 2.5 + np.sin(2 * np.pi * (90 + 120 * t / dur) * t) * 0.5) * env(n, 0.06, 0.3, 1.5)
def riser(dur=2.4):
    n = int(dur * SR); t = np.arange(n) / SR; f = 180 * 2 ** (2.2 * t / dur)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    ks = np.linspace(0.02, 0.25, n); x = noise(n); y = np.empty(n); acc = 0.0
    for i in range(n): acc += ks[i] * (x[i] - acc); y[i] = acc
    return (tone + y * 1.4) * env(n, dur * 0.9, dur * 0.1, 2.2)

def place(sig, t_src, gain_db, p=0.0, offset=0.0):
    o = s2o(t_src)
    if o is None: return
    i = int((o + offset) * SR); sig = sig / (np.abs(sig).max() + 1e-9) * 10 ** (gain_db / 20)
    st = pan(sig, p); j = min(len(out), i + len(st)); out[i:j] += st[:j - i]

# --- events: subtle clicks only, varied pitch/length/pan; nothing on cuts back to her ---
def click(f, dur=0.035, body=0.5):
    a = pop(f * 0.4, dur * 2) * body; b = tick(f, dur) * (1 - body); a[:len(b)] += b; return a
place(click(1700), 5.54, -30)                                # into space
place(click(2300, 0.025, 0.3), 16.68, -31, p=-0.2)           # into the data center
for k in range(20):                                          # rack units stacking
    place(tick(1500 + 45 * k + rng.uniform(-60, 60), 0.022), 16.68 + 0.55 * k / 20 + 0.03, -35 + k * 0.2, p=rng.uniform(-0.3, 0.3))
place(click(900, 0.06, 0.7), 17.32, -26)                     # $44B lands: a deeper click
place(click(2800, 0.02, 0.2), 18.4, -33)                     # "in debt for spacex"
for k, ch in enumerate('what should i have for dinner?'):    # keyboard clicks while the question types
    if ch != ' ': place(tick(2400 + rng.uniform(-500, 500), 0.018), 64.95 + (67.1 - 64.95) * k / 30, -36 + rng.uniform(-2, 1), p=rng.uniform(-0.15, 0.15))
place(click(1300, 0.05, 0.6), 67.35, -29)                    # send
place(click(2000, 0.03, 0.3), 68.9, -32, p=-0.3)             # cut to space
place(click(1100, 0.07, 0.8), 72.8, -29, p=-0.4)             # orb reaches the data center
place(click(1500, 0.04, 0.5), 84.44, -32)                    # "can't repossess"
place(click(1900, 0.03, 0.4), 110.2, -31)                    # umbrella
for k in range(14):                                          # counter rolling
    place(tick(2100 + 60 * k, 0.018), 112.6 + k * 0.065, -36 + k * 0.3, p=0.1)
place(click(1250, 0.05, 0.6), 113.5, -30)
pk = np.abs(out).max(); out = np.clip(out, -0.98, 0.98)
fn = f'sfx_{sys.argv[1]}.wav'; w = wave.open(fn, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype('<i2').tobytes()); w.close(); print(fn, 'peak', round(float(pk), 3))
