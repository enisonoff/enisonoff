"""map times between the v2 cut (plan_v2_backup.json) and the tighter v3 cut (plan2.json) through source frames"""
import json, bisect, os
def _load(f):
    P = json.load(open(f)); out = []; c = 0
    for k, a, b in P: out.append((k, a, b, c)); c += b - a
    return out
OLD, NEW = _load(os.environ['TMAP_OLD']), _load(os.environ['TMAP_NEW'])
def _to_src(P, f):
    for k, a, b, c in P:
        if c <= f < c + (b - a): return k, a + (f - c)
    k, a, b, c = P[-1]; return k, b - 1
def _from_src(P, k, s):
    best = None
    for kk, a, b, c in P:
        if kk != k: continue
        if a <= s < b: return c + (s - a)
        d = min(abs(s - a), abs(s - b + 1)); cand = c if s < a else c + (b - a) - 1
        if best is None or d < best[0]: best = (d, cand)
    return best[1]
def new_to_old_frame(f): return _from_src(OLD, *_to_src(NEW, f))
def old_to_new_frame(f): return _from_src(NEW, *_to_src(OLD, f))
