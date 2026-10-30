"""cc-P734: print a house multi's pieces as a grid per Z (item id per tile), to copy OSI's floor, wall and roof
conventions. Usage: python -P notes/cc-P734-tools/dump_multi.py 0x00A0 [0x0064 ...] (PYTHONPATH=scripts)."""
import collections
import sys

sys.path.insert(0, __file__.rsplit('notes', 1)[0] + 'notes/cc-P734-tools')
import stair_survey as S  # noqa: E402  (reads tiledata and the multi collection once)

for arg in sys.argv[1:]:
    mid = int(arg, 16)
    cs = S.comps(mid)
    print('== multi 0x%04X: %d pieces' % (mid, len(cs)))
    byz = collections.defaultdict(list)
    for x, y, z, t in cs:
        byz[z].append((x, y, t))
    xs = [c[0] for c in cs]
    ys = [c[1] for c in cs]
    for z in sorted(byz):
        print('-- z %d' % z)
        grid = collections.defaultdict(list)
        for x, y, t in byz[z]:
            grid[(x, y)].append(t)
        for y in range(min(ys), max(ys) + 1):
            row = []
            for x in range(min(xs), max(xs) + 1):
                ts = grid.get((x, y), [])
                row.append(('/'.join('%04X' % t for t in ts) if ts else '.').ljust(10))
            print('  %3d ' % y + ''.join(row))
    names = sorted({t for _, _, _, t in cs})
    print('-- names: ' + ', '.join('%04X %s(h%d)' % (t, S.name(t), S.items[t]['height']) for t in names))
