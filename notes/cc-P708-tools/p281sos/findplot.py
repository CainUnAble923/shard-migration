# cc-P281: where OSI's Guild House (multi 0x74) fits near a P151 plot: every centre within R tiles of the plot's centre
# whose footprint is clear of statics (but low grass, leaves and flowers the floor covers), decoration and spawners (2 tiles), with land within 3 of one z and standable
# ground below the steps; nearest first. Read only.   python -P findplot.py <facet> <cx> <cy> [R]
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hallbase as H
import multidump
fi, cx, cy = (int(v) for v in sys.argv[1:4])
R = int(sys.argv[4]) if len(sys.argv) > 4 else 10
F = H.Facet(fi)
comps = multidump.components(0x74)
offs = {(c[0], c[1]) for c in comps}
deco = {(d[0], d[1]) for d in H.decoration_in(fi, cx - R - 12, cy - R - 12, cx + R + 12, cy + R + 12)}
sp = [(s[1], s[2]) for s in H.spawns_in(H.FNAME[fi], cx - R - 12, cy - R - 12, cx + R + 12, cy + R + 12)]
def low(sid):
    # grass, leaves, ferns and flowers: under 3 high, not impassable, surface, wall or roof; the guild house floor
    # (7 above the ground) covers them
    return H.iheight(sid) <= 2 and not H.iflags(sid) & (H.IMP | H.SURF | H.WALL | H.ROOF)


res = []
for x in range(cx - R, cx + R + 1):
    for y in range(cy - R, cy + R + 1):
        zs = []
        ok = True
        for (dx, dy) in offs:
            tx, ty = x + dx, y + dy
            if any(not low(sid) for sid, sz in F.statics(tx, ty)) or (tx, ty) in deco or any(max(abs(tx - a), abs(ty - b)) <= 2 for a, b in sp):
                ok = False; break
            zs.append(F.avgz(tx, ty))
        if not ok or max(zs) - min(zs) > 3:
            continue
        bz = collections.Counter(zs).most_common(1)[0][0]
        if any(not low(sid) for dx in (-2, -1, 0, 1) for sid, sz in F.statics(x + dx, y + 8)):
            continue
        res.append((max(abs(x - cx), abs(y - cy)), x, y, bz, max(zs) - min(zs)))
res.sort()
for r in res[:12]:
    print('centre %d,%d z%d spread %d distance %d' % (r[1], r[2], r[3], r[4], r[0]))
print(len(res), 'fits')
