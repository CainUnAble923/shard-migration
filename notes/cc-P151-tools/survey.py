"""P151 survey: per town, list stock buildings (roofed components), signs, pinned spawners and open flat plots.
Read-only: reads client map files and pinned ModernUO data copied to the scratchpad."""
import json, os, sys, glob, math, collections
sys.path.insert(0, os.path.dirname(__file__))
import uomap
from uomap import F_IMPASSABLE, F_WET, F_ROOF, F_SURFACE, F_FOLIAGE, F_WALL, F_BACKGROUND

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "muo", "Distribution", "Data")
MAPNAME = {0: "Felucca", 1: "Trammel", 2: "Ilshenar", 3: "Malas", 4: "Tokuno", 5: "TerMur"}
SIGNMAP = {0: (0, 1), 1: (0,), 2: (1,), 3: (2,), 4: (3,), 5: (4,)}

land_td, stat_td = uomap.tiledata()


def load_spawners():
    out = collections.defaultdict(list)
    for folder in ("post-uoml", "shared"):
        for f in sorted(glob.glob(os.path.join(DATA, "Spawns", folder, "**", "*.json"), recursive=True)):
            for s in json.load(open(f, encoding="utf8")):
                loc = s.get("location")
                if not loc:
                    continue
                names = [e["name"] for e in s.get("entries", [])]
                out[s["map"]].append((loc[0], loc[1], loc[2], names, os.path.relpath(f, os.path.join(DATA, "Spawns")),
                                      s.get("homeRange", 0)))
    return out


import pickle
CLILOC = pickle.load(open(os.path.join(HERE, "..", "out", "cliloc.pkl"), "rb"))


def load_signs():
    out = collections.defaultdict(list)
    for l in open(os.path.join(DATA, "signs.cfg")):
        p = l.split()
        if len(p) < 6:
            continue
        m, iid, x, y, z = map(int, p[:5])
        name = " ".join(p[5:])
        if name.startswith("#"):
            name = CLILOC.get(int(name[1:]), name)
        for f in SIGNMAP[m]:
            out[f].append((x, y, z, name))
    return out


SPAWNERS = load_spawners()
SIGNS = load_signs()


def roofed(fac, x, y):
    for tid, z in fac.statics(x, y):
        fl, h, _ = stat_td[tid]
        if fl & F_ROOF or (fl & F_SURFACE and h <= 1):
            return True
    return False


def buildings(fac, x1, y1, x2, y2, min_tiles=12):
    seen = set()
    comps = []
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if (x, y) in seen or not roofed(fac, x, y):
                continue
            stack = [(x, y)]
            seen.add((x, y))
            tiles = []
            while stack:
                cx, cy = stack.pop()
                tiles.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (cx + dx, cy + dy)
                    if n in seen or not (x1 - 40 <= n[0] <= x2 + 40 and y1 - 40 <= n[1] <= y2 + 40):
                        continue
                    if roofed(fac, *n):
                        seen.add(n)
                        stack.append(n)
            if len(tiles) >= min_tiles:
                xs = [t[0] for t in tiles]; ys = [t[1] for t in tiles]
                comps.append((min(xs), min(ys), max(xs), max(ys), len(tiles)))
    return comps


def tile_ok(fac, x, y):
    tid, z = fac.land(x, y)
    fl = land_td[tid & 0x3FFF][0]
    if fl & (F_IMPASSABLE | F_WET):
        return None
    if tid in (0x2, 0x1DB) or (0x244 <= tid <= 0x24A):  # void/nodraw/cave black
        return None
    for sid, sz in fac.statics(x, y):
        sf, h, _ = stat_td[sid]
        if sf & (F_IMPASSABLE | F_WET | F_ROOF | F_WALL | F_SURFACE) or h > 2:
            return None
    return z


def open_plots(fac, x1, y1, x2, y2, size, maxspread=4, blockers=()):
    """Non-overlapping size x size plots inside the bbox where every tile is clear and flat."""
    ok = {}
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            ok[(x, y)] = tile_ok(fac, x, y)
    cands = []
    step = 2
    for x in range(x1, x2 - size + 2, step):
        for y in range(y1, y2 - size + 2, step):
            zs = []
            good = True
            for xx in range(x, x + size):
                for yy in range(y, y + size):
                    z = ok.get((xx, yy))
                    if z is None:
                        good = False; break
                    zs.append(z)
                if not good:
                    break
            if not good or max(zs) - min(zs) > maxspread:
                continue
            if any(x - 2 <= bx <= x + size + 1 and y - 2 <= by <= y + size + 1 for bx, by in blockers):
                continue
            cands.append((x, y, min(zs), max(zs)))
    return cands


def merge(cands, size):
    """Group overlapping plots into clear areas (bounding boxes)."""
    areas = []
    for x, y, zl, zh in cands:
        for a in areas:
            if x <= a[2] + 1 and x + size - 1 >= a[0] - 1 and y <= a[3] + 1 and y + size - 1 >= a[1] - 1:
                a[0] = min(a[0], x); a[1] = min(a[1], y); a[2] = max(a[2], x + size - 1); a[3] = max(a[3], y + size - 1)
                a[4] = min(a[4], zl); a[5] = max(a[5], zh)
                break
        else:
            areas.append([x, y, x + size - 1, y + size - 1, zl, zh])
    # second pass to merge chains
    changed = True
    while changed:
        changed = False
        for i in range(len(areas)):
            for j in range(i + 1, len(areas)):
                a, b = areas[i], areas[j]
                if a[0] <= b[2] + 1 and b[0] <= a[2] + 1 and a[1] <= b[3] + 1 and b[1] <= a[3] + 1:
                    areas[i] = [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]), min(a[4], b[4]), max(a[5], b[5])]
                    del areas[j]; changed = True; break
            if changed:
                break
    return areas


def report(name, facet, box, centre, size=14, margin=0):
    fac = uomap.Facet(facet)
    x1, y1, x2, y2 = box
    x1 -= margin; y1 -= margin; x2 += margin; y2 += margin
    mname = MAPNAME[facet]
    sp = [s for s in SPAWNERS[mname] if x1 <= s[0] <= x2 and y1 <= s[1] <= y2]
    sg = [s for s in SIGNS[facet] if x1 <= s[0] <= x2 and y1 <= s[1] <= y2]
    print(f"===== {name} ({mname}) box {x1},{y1}-{x2},{y2}")
    print(f"-- signs ({len(sg)})")
    for s in sorted(sg):
        print("   ", s)
    print(f"-- buildings (roofed, >=12 tiles)")
    for b in sorted(buildings(fac, x1, y1, x2, y2), key=lambda b: -b[4]):
        bx1, by1, bx2, by2, n = b
        inside = [s for s in sp if bx1 - 1 <= s[0] <= bx2 + 1 and by1 - 1 <= s[1] <= by2 + 1]
        signs = [s[3] for s in sg if bx1 - 3 <= s[0] <= bx2 + 3 and by1 - 3 <= s[1] <= by2 + 3]
        d = max(abs((bx1 + bx2) // 2 - centre[0]), abs((by1 + by2) // 2 - centre[1]))
        print(f"   {bx1},{by1}-{bx2},{by2} {bx2-bx1+1}x{by2-by1+1} roof={n} d={d} signs={signs} "
              f"spawns={[','.join(s[3]) for s in inside]}")
    print(f"-- open {size}x{size} plots (flat<=4, no blocking statics, clear of spawners by 2)")
    cands = open_plots(fac, x1, y1, x2, y2, size, blockers=[(s[0], s[1]) for s in sp])
    for a in sorted(merge(cands, size), key=lambda a: max(abs((a[0]+a[2])//2-centre[0]), abs((a[1]+a[3])//2-centre[1]))):
        d = max(abs((a[0] + a[2]) // 2 - centre[0]), abs((a[1] + a[3]) // 2 - centre[1]))
        c = collections.Counter(land_td[fac.land(x, y)[0] & 0x3FFF][1] for x in range(a[0], a[2]+1) for y in range(a[1], a[3]+1))
        top = ", ".join(f"{k} {v*100//sum(c.values())}%" for k, v in c.most_common(2))
        print(f"   area {a[0]},{a[1]}-{a[2]},{a[3]} ({a[2]-a[0]+1}x{a[3]-a[1]+1}) z{a[4]}..{a[5]} d={d} [{top}]")
    print("-- spawners in box")
    for s in sorted(sp, key=lambda s: (s[0], s[1])):
        print(f"   {s[0]},{s[1]},{s[2]} r{s[5]} {s[4]}: {', '.join(s[3])}")


if __name__ == "__main__":
    args = sys.argv[1:]
    name, facet = args[0], int(args[1])
    box = tuple(map(int, args[2].split(",")))
    centre = tuple(map(int, args[3].split(",")))
    size = int(args[4]) if len(args) > 4 else 14
    margin = int(args[5]) if len(args) > 5 else 0
    report(name, facet, box, centre, size, margin)
