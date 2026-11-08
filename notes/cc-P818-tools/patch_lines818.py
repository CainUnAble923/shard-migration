"""cc-P818: carries the driver's lodge change into another copy of trammel.mapops (the isle release's) line by line: the
lines the driver dropped are removed (each must be there once) and the lines it added go into the S+ run in its order
(x, y, z, id, hue), so the file differs only by the change. The change is read from two driver builds of the same base.

    python -P patch_lines818.py <driver before .mapops> <driver after .mapops> <target .mapops>
"""
import sys

before, after, target = sys.argv[1:4]
body = lambda p: [l for l in open(p, encoding='utf-8').read().split('\n') if l[:2] in ('L ', 'S+', 'S-')]
b, a = body(before), body(after)
drop = sorted(set(b) - set(a))
add = sorted(set(a) - set(b))
lines = open(target, encoding='utf-8').read().split('\n')
for l in drop:
    assert lines.count(l) == 1, ('not once in the target', l)
    lines.remove(l)
for l in add:
    assert l.startswith('S+ ') and l not in lines, l
key = lambda l: tuple(int(v) for v in l.split()[1:6])
idx = [i for i, l in enumerate(lines) if l.startswith('S+ ')]
first, last = idx[0], idx[-1]
assert idx == list(range(first, last + 1)), 'the S+ lines are one run'
run = sorted(lines[first:last + 1] + add, key=key)
lines = lines[:first] + run + lines[last + 1:]
open(target, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('dropped', len(drop), 'added', len(add))
