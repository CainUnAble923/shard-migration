"""cc-P265: find empty, flat, dry squares on a facet for the proof seeding (read only).

    python -P find_spot.py <facet index> x1 y1 x2 y2 [size]

A spot is a size x size square (default 26) where every tile's land is dry and passable, the land z spread is 2 or
less, and no static stands on it; squares are listed by their centre, best (flattest) first. It reads the shard's own
map files through P237's loader (nhbase: D:\\UO\\tool-trials\\client-data-copy, SHA-256 equal to the server's).
Player houses and items placed in a world are not in the map files: look before seeding.
"""
import sys

sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\notes\cc-P237-tools")
import nhbase as N  # noqa: E402

fi, x1, y1, x2, y2 = (int(v) for v in sys.argv[1:6])
size = int(sys.argv[6]) if len(sys.argv) > 6 else 26
mf = N.uofiles.MapFile(N.CLIENT, fi)
idx, sta = N.uofiles.load_statics_index(N.CLIENT, fi)
bh = mf.bh


ok = {}
for x in range(x1, x2):
    for y in range(y1, y2):
        tid, z = mf.get(x, y)
        fl = N.LAND[tid][0]
        good = not (fl & (N.WET | N.IMP))
        ok[(x, y)] = (good, z)
stat = set()
for bx in range(x1 // 8, x2 // 8 + 1):
    for by in range(y1 // 8, y2 // 8 + 1):
        for s in N.uofiles.block_statics(idx, sta, bx * bh + by):
            sx, sy = bx * 8 + s[1], by * 8 + s[2]
            stat.add((sx, sy))
found = []
for cx in range(x1 + size // 2, x2 - size // 2, 4):
    for cy in range(y1 + size // 2, y2 - size // 2, 4):
        zs = []
        bad = False
        for x in range(cx - size // 2, cx + size // 2):
            for y in range(cy - size // 2, cy + size // 2):
                g, z = ok[(x, y)]
                if not g or (x, y) in stat:
                    bad = True
                    break
                zs.append(z)
            if bad:
                break
        if not bad and max(zs) - min(zs) <= 2:
            found.append((max(zs) - min(zs), cx, cy, sorted(zs)[len(zs) // 2]))
found.sort()
for f in found[:12]:
    print(f"centre {f[1]},{f[2]} z {f[3]} (spread {f[0]})")
print(len(found), "squares")
