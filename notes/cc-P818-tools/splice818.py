"""cc-P818: the shipped trammel.mapops with its own header, F and B lines (they fingerprint the SoS base the shipped patch
was made on) and the isle driver's body (L, S+, S- lines) from a build on the stock base. The two bodies were identical
before this change (the baseline run), so the result differs from the shipped file only by the driver's changes.

    python -P splice818.py <shipped .mapops> <driver .mapops> <out .mapops>
"""
import sys
ship, drv, out = sys.argv[1:4]
def split(p):
    lines = open(p, encoding='utf-8').read().split('\n')
    i = max(n for n, l in enumerate(lines) if l.startswith(('B ', 'F ', '#')))
    return lines[:i + 1], lines[i + 1:]
h1, b1 = split(ship)
h2, b2 = split(drv)
assert [l for l in h1 if l.startswith('F ')] == [l for l in h2 if l.startswith('F ')], 'touched block count changed'
assert sorted(l.split()[1] for l in h1 if l.startswith('B ')) == sorted(l.split()[1] for l in h2 if l.startswith('B ')), 'block set changed'
open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(h1 + b2))
print('header', len(h1), 'body', len(b1), '->', len(b2))
