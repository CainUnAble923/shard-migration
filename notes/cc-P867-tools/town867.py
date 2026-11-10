"""cc-P867: spots inside main's New Haven buildings (SoS Trammel) for staff to stand each wall-backed design against
the wall its facing names, for the in-game shots (P864 item 2). The player's own placement path in a house was proven
separately (run 4, notes); these shots are for the facing against a real wall with a real floor.

Read with P678's SoS tools (notes/cc-P678-tools/winter: sosbase, rules, protected). A tile is usable when
  - it is reached on foot from the square (rules.REACH) and stands at a floor Z with a roof or a storey over it
    (indoors);
  - it is not protected (doors and their swing, NPC posts, spawners, seeded rows, pinned decoration: protected.P);
  - no wall stands on it and nothing with height (or impassable) stands on it between its floor and 15 over it;
and a design fits at an origin when every tile is usable at one Z, no tile is the floor tile in front of a window,
and its back row touches a full plain wall at that floor (from 2 under it to 15 over it, no window): west of its west column for "east", north of its north row for
"south", both for "northwest", east and south for "southeast". The first fit nearest the square wins; each design
gets its own building if it can. The trainee stands on the usable tile of the same room farthest south-east.

  python -P town867.py         prints TOWN = [(design, facing, x, y, z, (sx, sy, sz)), ...] and any design with no spot
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W678 = os.path.join(HERE, "..", "cc-P678-tools", "winter")
sys.path.insert(0, W678)
sys.path.insert(0, HERE)
import rules as R  # noqa: E402
import sosbase as B  # noqa: E402
import protected as PR  # noqa: E402
import decorcfg as D  # noqa: E402

DESIGNS = [
    "grey-fireplace-small-east", "grey-fireplace-small-south", "grey-fireplace-low-east", "grey-fireplace-low-south",
    "grey-fireplace-medium-east", "grey-fireplace-medium-south", "grey-fireplace-large-east",
    "grey-fireplace-large-south", "grey-fireplace-grand-east", "grey-fireplace-grand-south",
    "country-kitchen-east", "country-kitchen-south", "small-kitchen-northwest", "small-kitchen-southeast",
    "harpsichord-east", "harpsichord-south", "blue-couch-east", "blue-couch-south", "holiday-fireplace",
]
F = B.facet()


def wall_at(x, y, z, windows=False):
    """A full wall piece standing on (x, y) at floor Z z: wall flag, from at most 2 under the floor to 15 over it."""
    for sid, sz in F.statics(x, y):
        if B.iflags(sid) & B.WALL and sz <= z + 2 and sz + B.iheight(sid) >= z + 15:
            if ("window" in B.iname(sid).lower()) == windows:
                return True
    return False


def classify():
    usable = {}
    for (x, y) in R.REACH:
        z = R.W.stand.get((x, y))
        if z is None or (x, y) in PR.P:
            continue
        st = F.statics(x, y)
        if any(B.iflags(sid) & B.WALL for sid, sz in st if sz < z + 15 and sz + B.iheight(sid) > z):
            continue
        over = [sz for sid, sz in st if sz >= z + 15]
        # anything standing on the floor (height over 0, or impassable) between the floor and 15 over it is clutter
        clutter = [sid for sid, sz in st if z <= sz < z + 15 and (B.iheight(sid) > 0 or B.iflags(sid) & B.IMP)]
        if over and not clutter:
            usable[(x, y)] = z
    return usable


def fits(design, ox, oy, usable):
    head, parts = D.read(design)
    tiles = {(ox + p[1], oy + p[2]) for p in parts}
    zs = {usable.get(t) for t in tiles}
    if None in zs or len(zs) != 1:
        return None
    z = zs.pop()
    for x, y in tiles:      # no tile is the floor tile in front of a window (guide 11.4, 11.13)
        if any(wall_at(x + dx, y + dy, z, windows=True) for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1))):
            return None
    xs = [t[0] for t in tiles]
    ys = [t[1] for t in tiles]
    need = {
        "east": [(x - 1, y) for x, y in tiles if x == min(xs)],
        "south": [(x, y - 1) for x, y in tiles if y == min(ys)],
        "northwest": [(x - 1, y) for x, y in tiles if x == min(xs)] + [(x, y - 1) for x, y in tiles if y == min(ys)],
        "southeast": [(x + 1, y) for x, y in tiles if x == max(xs)] + [(x, y + 1) for x, y in tiles if y == max(ys)],
    }.get(head.get("facing"))
    if not need or not all(wall_at(wx, wy, z) for wx, wy in need):
        return None
    return tiles, z


def room(start, usable, z):
    seen, todo = set(), [start]
    while todo:
        t = todo.pop()
        if t in seen or usable.get(t) != z or len(seen) > 400:
            continue
        seen.add(t)
        todo += [(t[0] + 1, t[1]), (t[0] - 1, t[1]), (t[0], t[1] + 1), (t[0], t[1] - 1)]
    return seen


def main():
    usable = classify()
    sx0, sy0 = R.START
    order = sorted(usable, key=lambda t: abs(t[0] - sx0) + abs(t[1] - sy0))
    out, missing, used_rooms = [], [], []
    for design in DESIGNS:
        best = None
        for (x, y) in order:
            _, parts = D.read(design)
            for p in parts[:1]:
                ox, oy = x - p[1], y - p[2]
            f = fits(design, ox, oy, usable)
            if not f:
                continue
            tiles, z = f
            rm = room(next(iter(tiles)), usable, z)
            if any(tiles & r for r in used_rooms) and best is None:
                best = (ox, oy, z, tiles, rm)    # a room already used: keep looking for a fresh one
                continue
            best = (ox, oy, z, tiles, rm)
            break
        if not best:
            missing.append(design)
            continue
        ox, oy, z, tiles, rm = best
        used_rooms.append(rm)
        near = [t for t in rm - tiles if max(abs(t[0] - ox), abs(t[1] - oy)) <= 6] or list(rm - tiles)
        stand = max(near, key=lambda t: (t[0] + t[1], t[0]))   # within 6 tiles, so the shot holds the piece
        out.append((design, D.read(design)[0].get("facing"), ox, oy, z, (stand[0], stand[1], usable[stand])))
    print("TOWN = [")
    for row in out:
        print("    %r," % (row,))
    print("]")
    for m in missing:
        print("NO SPOT", m)


if __name__ == "__main__":
    main()
