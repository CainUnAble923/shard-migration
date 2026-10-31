"""Three-way merge of two mapops files that share a base, written in mapops.py diff's own order.
usage: merge_mapops.py base ours theirs out"""
import collections, sys

def load(p):
    head, fi, B, L, S = [], None, {}, {}, collections.Counter()
    for line in open(p, encoding='utf-8').read().splitlines():
        if not line:
            continue
        if line.startswith('#'):
            head.append(line); continue
        t = line.split()
        if t[0] == 'F':
            fi = int(t[1])
        elif t[0] == 'B':
            B[int(t[1])] = t[2]
        elif t[0] == 'L':
            L[(int(t[1]), int(t[2]))] = (int(t[3]), int(t[4]))
        elif t[0] in ('S+', 'S-'):
            S[(t[0],) + tuple(int(v) for v in t[1:6])] += 1
        else:
            raise ValueError(line)
    return head, fi, B, L, S

def merge_map(b, o, t, what):
    out, clash = {}, []
    for k in set(b) | set(o) | set(t):
        vb, vo, vt = b.get(k), o.get(k), t.get(k)
        if vo == vt: v = vo
        elif vo == vb: v = vt
        elif vt == vb: v = vo
        else:
            clash.append((what, k, vb, vo, vt)); v = vo
        if v is not None:
            out[k] = v
    return out, clash

base, ours, theirs, outp = sys.argv[1:5]
hb, fb, Bb, Lb, Sb = load(base)
ho, fo, Bo, Lo, So = load(ours)
ht, ft, Bt, Lt, St = load(theirs)
assert fb == fo == ft and ho == ht == hb
B, c1 = merge_map(Bb, Bo, Bt, 'B')
L, c2 = merge_map(Lb, Lo, Lt, 'L')
S = collections.Counter()
c3 = []
for k in set(Sb) | set(So) | set(St):
    nb, no, nt = Sb[k], So[k], St[k]
    if no == nt: n = no
    elif no == nb: n = nt
    elif nt == nb: n = no
    else:
        c3.append(('S', k, nb, no, nt)); n = no
    if n: S[k] = n
for c in c1 + c2 + c3:
    print('CLASH', c)
order = {'L': 0, 'S-': 1, 'S+': 2}
lines = [('L', x, y, tl, z) for (x, y), (tl, z) in L.items()]
for k, n in S.items():
    lines += [k] * n
lines.sort(key=lambda l: (order[l[0]], l[1], l[2], l[3:]))
out = hb + ['F %d %d' % (fb, len(B))] + ['B %d %s' % (b, B[b]) for b in sorted(B)]
out += [' '.join(str(v) for v in l) for l in lines]
open(outp, 'w', newline='\n', encoding='utf-8').write('\n'.join(out) + '\n')
print('B', len(Bb), len(Bo), len(Bt), '->', len(B))
print('L', len(Lb), len(Lo), len(Lt), '->', len(L))
print('S', sum(Sb.values()), sum(So.values()), sum(St.values()), '->', sum(S.values()))
print('clashes', len(c1 + c2 + c3))
