"""cc-P734: which wall each window piece stands in, over every house multi 0x60-0xA3 (count of window tiles): an
east-west (north or south) wall or a north-south (west or east) one. Usage (PYTHONPATH=scripts;notes/cc-P734-tools):
python -P notes/cc-P734-tools/window_survey.py"""
import collections

import stair_survey as S

res = collections.defaultdict(collections.Counter)
for mid in range(0x60, 0xA4):
    try:
        cs = S.comps(mid)
    except Exception:
        continue
    walls = [c for c in cs if S.items[c[3]]['height'] >= 19]
    for z0 in sorted({w[2] for w in walls}):
        base = [w for w in walls if w[2] == z0]
        x0 = min(b[0] for b in base); x1 = max(b[0] for b in base)
        y0 = min(b[1] for b in base); y1 = max(b[1] for b in base)
        for x, y, z, t in base:
            if 'window' not in S.name(t):
                continue
            if y in (y0, y1) and x0 < x < x1:
                res[t]['in an east-west wall'] += 1
            elif x in (x0, x1) and y0 < y < y1:
                res[t]['in a north-south wall'] += 1
for t in sorted(res):
    print('0x%04X %s' % (t, dict(res[t])))
