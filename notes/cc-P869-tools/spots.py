"""cc-P869: for each piece of the set, a standable tile beside the middle of its west (or north) side for the trainee
(so the camera, centred on the trainee, frames the whole piece), and a 4-step walk leg from there along that side and
back, every tile standable within 2 of the last and not covered by a piece. Prints Walk869 SPOTS lines.

  python -P spots.py main|release
"""
import sys
town = sys.argv[1]
if town == "main":
    sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\notes\cc-P856-tools")
    import find856 as F
    import validate856 as V
    rows = [(k, d, x, y, z) for k, a, d, x, y, z, n in V.rows()]
    W, REACH = F.R.W, F.R.REACH
else:
    sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\notes\cc-P856-tools\rel")
    import findrel as F
    rows = [(k, d, x, y, z) for k, d, x, y, z, i in F.RELEASE_ROWS]
    W, REACH = F.W, F.REACH
PART = {"christmas-train": 0x1B73, "santa-bench": 0x4A99, "large-snow-globe": 0x17CD, "snowman-bench": 0x9E1B}
covered = set()
for k, d, x, y, z in rows:
    covered |= {(x + dx, y + dy) for dx, dy in F.design_tiles(d)}
for k, d, ox, oy, oz in rows:
    t = F.design_tiles(d)
    xs, ys = [ox + dx for dx, _ in t], [oy + dy for _, dy in t]
    x1, x2, y1, y2 = min(xs), max(xs), min(ys), max(ys)
    long_y = (y2 - y1) >= (x2 - x1)
    mid = ((y1 + y2) // 2) if long_y else ((x1 + x2) // 2)
    best = None
    for gap in (1, 2, 3, -1, -2, -3):   # west or north first; then east or south (negative: past the far side)
        for off in (0, -1, 1, -2, 2):
            if gap > 0:
                sx, sy = (x1 - gap, mid + off) if long_y else (mid + off, y1 - gap)
            else:
                sx, sy = (x2 - gap, mid + off) if long_y else (mid + off, y2 - gap)
            z = W.stand.get((sx, sy))
            if z is None or (sx, sy) not in REACH or (sx, sy) in covered or abs(z - oz) > 2:
                continue
            leg, ok, lz = [], True, z
            for i in range(1, 5):
                p = (sx, sy - i) if long_y else (sx - i, sy)
                pz = W.stand.get(p)
                if pz is None or p in covered or abs(pz - lz) > 2:
                    ok = False
                    break
                leg.append(p)
                lz = pz
            if ok:
                best = (sx, sy, z, "North" if long_y else "West", "South" if long_y else "East")
                break
        if best:
            break
    print('    ("%s", %s, %s, 0x%04X),  # %s box %d-%d x %d-%d' % (
        k.replace("set-", ""), best[:3], best[3:], PART[d], d, x1, x2, y1, y2))
