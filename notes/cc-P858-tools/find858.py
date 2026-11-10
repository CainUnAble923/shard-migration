"""cc-P858 (a copy of cc-P856's find856.py): where the fortune teller's wagon fits beside the Festival stall. cc-P856: where the five winter addons fit in MAIN's New Haven (the Siege of Sosaria map), by P678's own map rules
(notes/cc-P678-tools/winter: rules.py, sosbase.py, protected.py, soswalk). For every candidate origin it checks each
tile the addon covers:

  - reached on foot from the square's start (3634,2586) before the decor, at a standing z within 2 of the base;
  - not protected (doors and their swing, NPC posts, spawner tiles, the arrival tile, the Reset Stone, other seeders'
    tiles), not blocked by an impassable static, not another winter row's tile;
  - outdoors (no roof) for the square's pieces; under a roof, with the room's wall right north of its back row, for
    the fireplace;
and then that the walk from the start still reaches every tile it reached before, with the whole footprint blocked.
Candidates are ranked by distance to the target plus 2 for each walkway tile covered (roads and plaza paving).

  python -P find856.py <design> <x1> <y1> <x2> <y2> <tx> <ty> [indoor] [top N]
  (env PLACED="design@x,y;...": pieces already chosen, kept a tile apart)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W678 = os.path.join(HERE, "..", "cc-P678-tools", "winter")   # cc-P858: Iron's docs copy
sys.path.insert(0, W678)
import rules as R  # noqa: E402  (loads the SoS facet, the walk and the protected tiles)
import sosbase as B  # noqa: E402
import protected as PR  # noqa: E402

DESIGNS = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/FestivalWagon/FortuneTellerWagonDesign.cs"
# cc-P858: the stall (FestivalStore.cs FestivalMarket.Pieces and the peddler) at its anchor, kept a tile apart
STALL_AT = (3636, 2627)
STALL = [(0, 0), (0, 1), (1, 1), (-1, 0), (1, 0), (-2, -1)]
APPROACH = [(0, 10), (1, 10)]   # where a player stands to climb the stair


def design_tiles(key):
    text = open(DESIGNS, encoding="utf-8").read()
    return sorted({(int(x), int(y)) for x, y in re.findall(r"new\(0x[0-9A-F]+, (-?\d+), (-?\d+), -?\d+,", text)})


def taken_tiles():
    rows = json.load(open(os.path.join(W678, "placement.json")))
    taken = {(r["x"], r["y"]): r["key"] for r in rows}
    for sx, sy in STALL:   # cc-P858: the stall and a 1-tile ring
        for rx in (-1, 0, 1):
            for ry in (-1, 0, 1):
                taken.setdefault((STALL_AT[0] + sx + rx, STALL_AT[1] + sy + ry), "festival stall")
    # PLACED="design@x,y;design@x,y": this prompt's pieces already chosen, each tile they cover and a 1-tile ring kept clear
    for spec in filter(None, os.environ.get("PLACED", "").split(";")):
        key, at = spec.split("@")
        ox, oy = (int(v) for v in at.split(","))
        for dx, dy in design_tiles(key):
            for rx in (-1, 0, 1):
                for ry in (-1, 0, 1):
                    taken.setdefault((ox + dx + rx, oy + dy + ry), key)
    return taken


def fits(key, ox, oy, indoor, taken, verbose=False):
    tiles = design_tiles(key)
    base = R.W.stand.get((ox, oy))
    if base is None:
        return None, ["origin not standable"]
    errs, walkway = [], 0
    for dx, dy in tiles:
        x, y = ox + dx, oy + dy
        stand = R.W.stand.get((x, y))
        if (x, y) not in R.REACH:
            errs.append("%d,%d not reached" % (x, y))
        elif stand is None or abs(stand - base) > 2:
            errs.append("%d,%d stand %s vs base %s" % (x, y, stand, base))
        prot = [p for p in PR.P.get((x, y), ()) if "ClusterFWinterSetLayout" not in p]   # not this prompt's own rows
        if prot:
            errs.append("%d,%d protected: %s" % (x, y, "; ".join(sorted(prot))))
        if (x, y) in taken:
            errs.append("%d,%d taken: %s" % (x, y, taken[(x, y)]))
        if R.F.blocked(x, y, base):
            errs.append("%d,%d blocked by %s" % (x, y, R.F.blocked(x, y, base)))
        roof = R.F.roof_over(x, y, base)
        if indoor and not roof:
            errs.append("%d,%d not under a roof" % (x, y))
        if not indoor and roof:
            errs.append("%d,%d under a roof" % (x, y))
        if B.walkway(R.F, x, y, base):
            walkway += 1
        for sid, sz in R.F.statics(x, y):   # cc-P856 render review: nothing standing on a covered tile
            if B.iheight(sid) > 0 and sz >= base - 2 and not (B.iflags(sid) & B.SURF and sz + B.calch(sid) <= base + 2):   # a floor is fine
                errs.append("%d,%d has 0x%04X %s at z%d" % (x, y, sid, B.iname(sid), sz))
        if not verbose and errs:
            return None, errs
    # cc-P856 render review: nothing impassable in the bounding box, gaps included
    xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]
    for x in range(ox + min(xs), ox + max(xs) + 1):
        for y in range(oy + min(ys), oy + max(ys) + 1):
            for sid, sz in R.F.statics(x, y):
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
                for sid, sz in R.F.statics(x, y):
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
    if indoor:
        back = min(dy for _, dy in tiles)
        for dx in sorted({dx for dx, dy in tiles if dy == back}):
            if not R.F.wall_at(ox + dx, oy + back - 1, base):
                errs.append("no wall north of the back row at %d,%d" % (ox + dx, oy + back - 1))
    for dx, dy in APPROACH:   # cc-P858: the stair's foot is reached on foot, at the base's z
        x, y = ox + dx, oy + dy
        stand = R.W.stand.get((x, y))
        if (x, y) not in R.REACH or stand is None or abs(stand - base) > 2 or (x, y) in taken or PR.P.get((x, y)):
            errs.append("stair foot %d,%d not a free reached tile" % (x, y))
    if errs:
        return None, errs
    # the walk with the whole footprint blocked
    stand = dict(R.W.stand)
    block = {(ox + dx, oy + dy) for dx, dy in tiles}
    for t in block:
        stand[t] = None
    saved, R.W.stand = R.W.stand, stand
    try:
        after = set(R.W.flood(R.START))
    finally:
        R.W.stand = saved
    # a tile inside the piece's own box (a gap between its parts) is the piece's, not cut off from the town
    xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]
    inside = {(x, y) for x in range(ox + min(xs), ox + max(xs) + 1) for y in range(oy + min(ys), oy + max(ys) + 1)}
    cut = sorted(R.REACH - after - block - inside)
    if cut:
        return None, ["cuts off %d tiles, e.g. %s" % (len(cut), cut[:5])]
    return (walkway, base), []


def main():
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
    print("%s: %d origins fit in %d,%d-%d,%d (%s)" % (key, len(found), x1, y1, x2, y2, "indoor" if indoor else "outdoor"))
    for score, walkway, ox, oy, base in found[:top]:
        print("  %d,%d,%d  walkway tiles %d, score %d (distance to %d,%d plus 2 per walkway tile)" % (ox, oy, base, walkway, score, tx, ty))


if __name__ == "__main__":
    main()
