"""cc-P856: find856.py for the RELEASE branch's New Haven (the ML plaza on the vanilla Trammel map, x 3400-3560). The
same tests per tile as main's: reached on foot from the square's start (HavenSpots.Start 3503,2574 in the release copy)
by relwalk.py (P678's walk over vanilla Trammel), standing z within 2 of the base, not protected (this folder's copy
of P266's protected.py, read from Iron's release copy p856-isle), not another winter row's tile (the release copy's
ClusterFWinterDecorLayout.cs, P266's rows), nothing impassable at the base (P237's nhbase), outdoors or (indoor) under
a roof with the room's wall north of the back row; then the walk with the footprint blocked cuts nothing off.

  python -P findrel.py <design> <x1> <y1> <x2> <y2> <tx> <ty> [indoor] [top N]
  python -P findrel.py --validate <placed.md out>     the release rows (RELEASE_ROWS below) together
(env PLACED="design@x,y;...": pieces already chosen, kept a tile apart)
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nhbase as B  # noqa: E402
import protected as PR  # noqa: E402
import relwalk  # noqa: E402
sys.path.insert(0, os.path.dirname(HERE))
import keepclear as KC  # noqa: E402  (cc-P869)

DESIGNS = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/WinterSet/WinterSetDesigns.cs"
LAYOUT = "D:/UO/golems/Iron/p856-isle/server/customizations/ClusterFWinterDecorLayout.cs"
F = B.Facet(1)
START = (3503, 2574)
W = relwalk.Walk((3380, 2440, 3600, 2680))
REACH = set(W.flood(START))

# The release rows chosen (key, design, x, y, z), as ClusterFWinterSetLayout.cs in the release diff has them.
RELEASE_ROWS = [
    ("set-train", "christmas-train", 3436, 2614, 43, False),        # cc-P869: was 3548,2523,14 (a sapling and a walnut)
    ("set-snowman-bench", "snowman-bench", 3503, 2596, 1, False),
    ("set-santa-bench", "santa-bench", 3505, 2589, 16, False),     # cc-P869: was 3503,2588,16 (an o'hii tree 2 west)
    ("set-snow-globe", "large-snow-globe", 3518, 2591, 1, False),  # cc-P869: was 3519,2592,1 (the dock sleigh 3 south)
]


def design_tiles(key):
    text = open(DESIGNS, encoding="utf-8").read()
    block = text.split('["%s"]' % key, 1)[1].split("]),", 1)[0]
    return sorted({(int(x), int(y)) for x, y in re.findall(r"new\(0x[0-9A-F]+, (-?\d+), (-?\d+), -?\d+,", block)})


def parts(design):
    text = open(DESIGNS, encoding="utf-8").read()
    block = text.split('["%s"]' % design, 1)[1].split("]),", 1)[0]
    return [(int(i, 16), int(x), int(y), int(z), n) for i, x, y, z, n in
            re.findall(r'new\(0x([0-9A-F]+), (-?\d+), (-?\d+), (-?\d+), -?\d+, [A-Za-z0-9.]+, (null|"[^"]*")\)', block)]


def taken_tiles():
    text = open(LAYOUT, encoding="utf-8").read()
    taken = {(int(x), int(y)): k for k, x, y in re.findall(r'new\("([^"]+)", "[^"]+", (\d+), (\d+), -?\d+,', text)}
    for spec in filter(None, os.environ.get("PLACED", "").split(";")):
        key, at = spec.split("@")
        ox, oy = (int(v) for v in at.split(","))
        for dx, dy in design_tiles(key):
            for rx in (-1, 0, 1):
                for ry in (-1, 0, 1):
                    taken.setdefault((ox + dx + rx, oy + dy + ry), key)
    return taken


def winter_rows():
    """cc-P869: P678's winter rows, as (x, y, key). The set's own other pieces (PLACED) are kept a tile apart by
    taken_tiles, as P856 had it: the set stands as a group (P865 passed the release harbour's bench pair)."""
    rows = [(int(x), int(y), k) for k, x, y in re.findall(r'new\("([^"]+)", "[^"]+", (\d+), (\d+), -?\d+,', open(LAYOUT, encoding="utf-8").read())]
    return rows


def fits(key, ox, oy, indoor, taken, verbose=False, base=None):
    tiles = design_tiles(key)
    if base is None:
        base = W.stand.get((ox, oy))
    if base is None:
        return None, ["origin not standable"]
    errs, walkway = [], 0
    for dx, dy in tiles:
        x, y = ox + dx, oy + dy
        stand = W.stand.get((x, y))
        if (x, y) not in REACH:
            errs.append("%d,%d not reached" % (x, y))
        elif stand is None or abs(stand - base) > 2:
            errs.append("%d,%d stand %s vs base %s" % (x, y, stand, base))
        prot = [p for p in PR.P.get((x, y), ()) if "ClusterFWinterSetLayout" not in p]
        if prot:
            errs.append("%d,%d protected: %s" % (x, y, "; ".join(sorted(prot))))
        if (x, y) in taken:
            errs.append("%d,%d winter row %s" % (x, y, taken[(x, y)]))
        if F.blocked(x, y, base):
            errs.append("%d,%d blocked by %s" % (x, y, F.blocked(x, y, base)))
        roof = F.roof_over(x, y, base)
        if indoor and not roof:
            errs.append("%d,%d not under a roof" % (x, y))
        if not indoor and roof:
            errs.append("%d,%d under a roof" % (x, y))
        if B.walkway(F, x, y, base):
            walkway += 1
        for sid, sz in F.statics(x, y):   # cc-P856 render review: nothing standing on a covered tile
            if B.iheight(sid) > 0 and sz >= base - 2 and not (B.iflags(sid) & B.SURF and sz + B.calch(sid) <= base + 2):   # a floor is fine
                errs.append("%d,%d has 0x%04X %s at z%d" % (x, y, sid, B.iname(sid), sz))
        if not verbose and errs:
            return None, errs
    # cc-P856 render review: nothing impassable in the bounding box, gaps included
    xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]
    for x in range(ox + min(xs), ox + max(xs) + 1):
        for y in range(oy + min(ys), oy + max(ys) + 1):
            for sid, sz in F.statics(x, y):
                if B.iflags(sid) & B.IMP and sz + B.iheight(sid) > base and sz < base + 16:
                    errs.append("%d,%d in the box: 0x%04X %s" % (x, y, sid, B.iname(sid)))
                    break
    if not verbose and errs:
        return None, errs
    # cc-P856 after the first shots: camera and room (clearance.py)
    x1, x2, y1, y2 = ox + min(xs), ox + max(xs), oy + min(ys), oy + max(ys)
    if not indoor:
        for x in range(x1 - 1, x2 + 4):
            for y in range(y1 - 1, y2 + 4):
                south_or_east = x > x2 or y > y2
                ring = x in (x1 - 1, x2 + 1) or y in (y1 - 1, y2 + 1)
                if not (south_or_east or ring):
                    continue
                for sid, sz in F.statics(x, y):
                    top = sz + B.iheight(sid)
                    building = B.iflags(sid) & (B.WALL | B.ROOF)
                    if building and south_or_east and x <= x2 + 3 and y <= y2 + 3 and top >= base + 10 and sz <= base + 20:
                        errs.append("camera: %d,%d has 0x%04X %s (top z%d) south or east of the piece" % (x, y, sid, B.iname(sid), top))
                        break
                    if False and ring:   # dropped (clearance2.py): trees and pier posts beside a piece read fine
                        errs.append("room: %d,%d has 0x%04X %s against the piece" % (x, y, sid, B.iname(sid)))
                        break
    if not verbose and errs:
        return None, errs
    if not indoor:   # cc-P869 (P865 item 5): no tree and no other winter row within 3 tiles of a covered tile
        cover = [(ox + dx, oy + dy) for dx, dy in tiles]
        errs += ["tree within %d: %s" % (KC.RADIUS, h) for h in KC.trees_near(F.statics, B.iname, cover)]
        errs += ["winter row within %d: %s" % (KC.RADIUS, h) for h in KC.rows_near(winter_rows(), cover)]
    if not verbose and errs:
        return None, errs
    if indoor:
        back = min(dy for _, dy in tiles)
        for dx in sorted({dx for dx, dy in tiles if dy == back}):
            if not F.wall_at(ox + dx, oy + back - 1, base):
                errs.append("no wall north of the back row at %d,%d" % (ox + dx, oy + back - 1))
    if errs:
        return None, errs
    xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]   # gaps inside the piece's box are the piece's
    inside = {(x, y) for x in range(ox + min(xs), ox + max(xs) + 1) for y in range(oy + min(ys), oy + max(ys) + 1)}
    cut = [t for t in walk_cut({(ox + dx, oy + dy) for dx, dy in tiles}) if t not in inside]
    if cut:
        return None, ["cuts off %d tiles, e.g. %s" % (len(cut), cut[:5])]
    return (walkway, base), []


def walk_cut(block):
    stand = dict(W.stand)
    for t in block:
        stand[t] = None
    saved, W.stand = W.stand, stand
    try:
        after = set(W.flood(START))
    finally:
        W.stand = saved
    return sorted(REACH - after - set(block))


def search():
    key = sys.argv[1]
    x1, y1, x2, y2, tx, ty = (int(v) for v in sys.argv[2:8])
    indoor = "indoor" in sys.argv[8:]
    top = int(sys.argv[sys.argv.index("top") + 1]) if "top" in sys.argv else 8
    taken = taken_tiles()
    found = []
    for ox in range(x1, x2 + 1):
        for oy in range(y1, y2 + 1):
            ok, _ = fits(key, ox, oy, indoor, taken)
            if ok:
                walkway, base = ok
                found.append((walkway * 2 + abs(ox - tx) + abs(oy - ty), walkway, ox, oy, base))
    found.sort()
    print("%s: %d origins fit in %d,%d-%d,%d (%s), release map" % (key, len(found), x1, y1, x2, y2, "indoor" if indoor else "outdoor"))
    for score, walkway, ox, oy, base in found[:top]:
        print("  %d,%d,%d  walkway tiles %d, score %d" % (ox, oy, base, walkway, score))


def validate(out):
    bad, lines, block, inside = 0, [], set(), set()
    for key, design, x, y, z, indoor in RELEASE_ROWS:
        os.environ["PLACED"] = ";".join("%s@%d,%d" % (d, ox, oy) for k, d, ox, oy, oz, i in RELEASE_ROWS if k != key)
        ok, errs = fits(design, x, y, indoor, taken_tiles(), base=z)
        status = "ok" if ok else "FAIL: " + "; ".join(errs[:5])
        bad += status != "ok"
        print("%s (%s) at %d,%d,%d: %s" % (key, design, x, y, z, status))
        lines.append("### %s (%s), origin %d,%d,%d: %s" % (key, design, x, y, z, status))
        for item, dx, dy, dz, n in parts(design):
            lines.append("- 0x%04X, %d,%d,%d, as made%s" % (item, x + dx, y + dy, z + dz, "" if n == "null" else ", " + n.strip('"')))
        lines.append("")
        block |= {(x + dx, y + dy) for dx, dy in design_tiles(design)}
        tiles = design_tiles(design)
        xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]
        inside |= {(i, j) for i in range(x + min(xs), x + max(xs) + 1) for j in range(y + min(ys), y + max(ys) + 1)}
    cut = [t for t in walk_cut(block) if t not in inside]
    summary = "All %d pieces together cover %d tiles; the walk from %d,%d reaches every tile it reached before: %s." % (
        len(RELEASE_ROWS), len(block), START[0], START[1], "yes" if not cut else "NO, cut off %d, e.g. %s" % (len(cut), cut[:5]))
    print(summary)
    bad += bool(cut)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("## Release (the ML plaza New Haven, vanilla Trammel)\n\n" + summary + "\n\n" + "\n".join(lines))
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--validate":
        sys.exit(validate(sys.argv[2]))
    search()
