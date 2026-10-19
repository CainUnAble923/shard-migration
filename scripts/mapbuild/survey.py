"""Tools for studying OSI rooms before building (cc-P181): what OSI puts in corners and how dense, read from the stock
map plus ModernUO's decoration files (the server adds those items at startup; bookcases, candelabra, torches and most
furniture are NOT in the map statics, so a map-only survey undercounts them).

    python -P survey.py corners <label> x1 y1 x2 y2 [zmin zmax]     corner and density survey of a rect (Trammel)
    python -P survey.py grid <folder> <facet> x1 y1 x2 y2            land id / Z grid (cave letters, see land_grid)
    python -P survey.py deco x1 y1 x2 y2                             decoration items in a rect
"""
import collections, glob, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mapbuild import uofiles  # noqa: E402

DECORATION = r"D:\UO\ModernUO-pinned\Distribution\Data\Decoration"


def read_decoration_cfg(path):
    """[(x, y, z, itemId, typeName)] from one ModernUO decoration cfg (Type 0xID header lines, then x y z lines)."""
    rows = []
    cur = None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if re.match(r"^-?\d+\s+-?\d+\s+-?\d+", line):
            m = re.match(r"^(-?\d+)\s+(-?\d+)\s+(-?\d+)", line)
            if cur:
                rows.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), cur[1], cur[0]))
            continue
        m = re.match(r"^(\w+)\s+(0x[0-9A-Fa-f]+|\d+)(.*)$", line)
        if m:
            cur = (m.group(1), int(m.group(2), 0))
    return rows


def decoration(rect=None, folders=("Britannia", "Trammel")):
    """[(x, y, z, itemId, typeName, file)] from the Britannia (both facets) and Trammel decoration folders."""
    out = []
    for f in folders:
        for p in sorted(glob.glob(os.path.join(DECORATION, f, "*.cfg"))):
            for r in read_decoration_cfg(p):
                if rect is None or (rect[0] <= r[0] <= rect[2] and rect[1] <= r[1] <= rect[3]):
                    out.append(r + (os.path.basename(p),))
    return out


FLOORISH = ("floor", "pavers", "roof", "carpet", "rug", "boards", "planks", "nodraw", "no draw", "water", "marble", "stairs", "grass")


def survey_corners(label, x1, y1, x2, y2, fi=1, folder=uofiles.CLIENT, zmin=-128, zmax=127, with_decoration=True):
    """Inner corners of a rect and what sits within one tile of each; decor per 100 floor tiles by name.
    Floor = a tile without a wall-flagged piece whose land is not void (or that carries a surface). Prints and returns
    a dict."""
    land_td, items = uofiles.read_tiledata(folder)
    ids, zs = uofiles.load_land(folder, fi)
    tiles = collections.defaultdict(list)
    for (x, y, z, tid) in uofiles.statics_in(folder, fi, x1, y1, x2, y2):
        if zmin <= z <= zmax:
            tiles[(x, y)].append((tid, z, "map"))
    if with_decoration:
        for (x, y, z, tid, typ, src) in decoration(rect=(x1, y1, x2, y2)):
            if zmin <= z <= zmax and tid < 0x4000:
                tiles[(x, y)].append((tid, z, "deco:" + typ))
    is_wall = lambda c: any(items[t]["flags"] & uofiles.WALL for t, z, s in tiles.get(c, []))
    floor = set()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if is_wall((x, y)):
                continue
            if int(ids[x, y]) == uofiles.VOID and not any(items[t]["flags"] & uofiles.SURFACE for t, z, s in tiles.get((x, y), [])):
                continue
            floor.add((x, y))
    walls = {c for c in tiles if is_wall(c)}
    solid = lambda c: c in walls
    from mapbuild.walls import concave_corners
    corners = concave_corners(floor, solid)
    name = lambda t: items[t]["name"].lower()
    floorish = lambda t: any(w in name(t) for w in FLOORISH) or items[t]["flags"] & uofiles.ROOF
    corner_items = collections.Counter()
    dressed = 0
    for (x, y, nm) in corners:
        found = set()
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for t, z, s in tiles.get((x + a, y + b), []):
                    if items[t]["flags"] & uofiles.WALL or floorish(t):
                        continue
                    found.add(name(t))
        if found:
            dressed += 1
        corner_items.update(found)
    decor = collections.Counter()
    for c in floor:
        for t, z, s in tiles.get(c, []):
            if items[t]["flags"] & uofiles.WALL or floorish(t):
                continue
            decor[name(t)] += 1
    on_walls = collections.Counter()
    for c in walls:
        for t, z, s in tiles.get(c, []):
            if items[t]["flags"] & uofiles.WALL or floorish(t):
                continue
            on_walls[name(t)] += 1
    nf = max(1, len(floor))
    tot = sum(decor.values())
    print("== %s: x %d-%d y %d-%d: floor %d, wall tiles %d, inner corners %d, dressed within 1 tile %d (%.0f%%)"
          % (label, x1, x2, y1, y2, len(floor), len(walls), len(corners), dressed, 100.0 * dressed / max(1, len(corners))))
    print("   corner items:", ", ".join("%s %d" % kv for kv in corner_items.most_common(14)))
    print("   decor on floor: %d = %.1f per 100 floor tiles:" % (tot, 100.0 * tot / nf),
          ", ".join("%s %.1f" % (k, 100.0 * v / nf) for k, v in decor.most_common(16)))
    print("   non-wall items on wall tiles: %d:" % sum(on_walls.values()), ", ".join("%s %d" % kv for kv in on_walls.most_common(10)))
    return dict(floor=len(floor), walls=len(walls), corners=len(corners), dressed=dressed, corner_items=corner_items,
                decor=decor, per100=100.0 * tot / nf, on_walls=on_walls)


def land_grid(folder, fi, x1, y1, x2, y2, out=print):
    """Print a land grid: . cave floor, e cave edge (floor to black), r rock 0x025A, R rock variants, E rock edge,
    q second rock set, # void, c crystal, d dirt, m marble, s stone, ? other; then Z // 4 per tile."""
    ids, zs = uofiles.load_land(folder, fi)

    def code(t):
        if 0x0245 <= t <= 0x0249: return "."
        if 0x024A <= t <= 0x0259: return "e"
        if t == 0x025A: return "r"
        if 0x025B <= t <= 0x0261: return "R"
        if 0x0262 <= t <= 0x0265: return "E"
        if 0x0266 <= t <= 0x026D: return "q"
        if t == 0x0244: return "#"
        if 0x3867 <= t <= 0x386A: return "c"
        if 0x0071 <= t <= 0x0078: return "d"
        if 0x0486 <= t <= 0x0489: return "m"
        if 0x043C <= t <= 0x0441: return "s"
        return "?"
    out("ids:   " + "".join(str(x % 10) for x in range(x1, x2 + 1)))
    for y in range(y1, y2 + 1):
        out("%5d  " % y + "".join(code(int(ids[x, y])) for x in range(x1, x2 + 1)))
    out("z // 4 (- below 0):")
    for y in range(y1, y2 + 1):
        out("%5d  " % y + "".join("-" if int(zs[x, y]) < 0 else str(min(9, int(zs[x, y]) // 4)) for x in range(x1, x2 + 1)))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "corners":
        a = sys.argv[2:]
        survey_corners(a[0], *map(int, a[1:5]), zmin=int(a[5]) if len(a) > 6 else -128, zmax=int(a[6]) if len(a) > 6 else 127)
    elif mode == "grid":
        land_grid(sys.argv[2], int(sys.argv[3]), *map(int, sys.argv[4:8]))
    elif mode == "deco":
        for r in sorted(decoration(rect=tuple(map(int, sys.argv[2:6])))):
            print(r)
