r"""cc-P678: checks every placed prop of the League field office (design/registrar-office/layout.json), the League board
(ClusterFRequisitionSeeder.OfficeBoard in Requisitions/Appraiser.cs) and the Order of the Alembic hall
(ClusterFAlembicGuild.Hall) against the SoS Trammel map files. Reads the Iron code copy; read only.
    python -P check.py > check.out.txt
Each prop: open on SoS (townmap.tile) with the floor z we use; a floor prop stands at that z by pinned's walk (soswalk),
a prop above the floor stands on a surface static whose top is its z (a table or counter); inside its building (a
covered tile of buildings.find) or, for the office's outside group, an uncovered open tile south of the doorway; not a
stock spawner/decoration/HavenSpots tile (placer.stock_tiles), not an NPC tile in out/homes.csv, not on or next to a
doorway (a tile the walk enters between two wall statics). A prop against a wall (bookcase, shelf, chest, flowerpot,
the paired alchemist tables) has a wall on its north or west side. Then the walk, with every floor prop blocking its
tile: from each building's street door to each NPC's tile, and to every walkable tile around the Alembic guildmaster.
Exit status 1 on any failure.
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)
import buildings  # noqa: E402
import placer  # noqa: E402
import soswalk  # noqa: E402
import townmap  # noqa: E402

CODE = "D:/UO/golems/Iron/ShatteredLegacy"
WALLFLAG = 0x10
FLOOR = 0
START = (3634, 2586)          # the new start (HavenSpots.Centre is 3660,2590; Sir Helper 3634,2586)

OFFICE = dict(name="League field office", box=(3658, 2547, 3674, 2562),
              npcs={"League Registrar": (3660, 2549), "Appraiser": (3660, 2551), "Sanitation Warden": (3662, 2549)})
ALEMBIC = dict(name="Order of the Alembic hall", box=(3599, 2495, 3615, 2511),
               npcs={"Alembic guildmaster": (3608, 2497), "Sadrah": (3610, 2497)})
AGAINST_WALL = ("bookcase", "wooden shelf", "wooden chest", "flowerpot")

fails = []


def ok(cond, msg):
    print(("  ok    " if cond else "  FAIL  ") + msg)
    if not cond:
        fails.append(msg)


def office_props():
    L = json.load(open(CODE + "/design/registrar-office/layout.json"))
    return [(c["area"], c["name"], int(c["id"], 16), c["x"], c["y"], c["z"]) for c in L["components"]]


def alembic_props():
    t = open(CODE + "/server/customizations/ClusterFAlembicGuild.cs").read()
    body = t[t.index("public static readonly MineCampComponent[] Hall ="):]
    body = body[:body.index("];")]
    return [(a, n, int(i, 16), int(x), int(y), int(z)) for a, i, n, x, y, z in
            re.findall(r'new\("(\w+)", 0x([0-9A-F]+), "([^"]+)", (\d+), (\d+), (-?\d+)\)', body)]


def board():
    t = open(CODE + "/server/customizations/Requisitions/Appraiser.cs").read()
    m = re.search(r'OfficeBoard = new\("New Haven", "[^"]*", 1, (\d+), (\d+), (-?\d+), Direction\.(\w+)', t)
    return int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)


def statics_at(w, x, y):
    return w.sts.get((x, y), [])


def is_wall(w, x, y):
    items = soswalk.files()["items"]
    return any(items[i]["flags"] & WALLFLAG for z, i in statics_at(w, x, y) if z <= FLOOR + 2)


def surface_top(w, x, y):
    items = soswalk.files()["items"]
    return [z + items[i]["height"] for z, i in statics_at(w, x, y) if items[i]["flags"] & soswalk.SURF and items[i]["height"]]


def doorways(w, reach, box):
    """Tiles the walk enters through a wall: a run of at most 3 reachable tiles along a wall line, closed by a wall
    static at each end, with no wall static in front of or behind it (an arch under a lintel, or a door's gap)."""
    x1, y1, x2, y2 = box
    out = []
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if (x, y) not in reach or is_wall(w, x, y):
                continue
            for (dx, dy), (px, py) in (((1, 0), (0, 1)), ((0, 1), (1, 0))):
                if is_wall(w, x + px, y + py) or is_wall(w, x - px, y - py):
                    continue
                ends, run = [], 1
                for s in (1, -1):
                    k = 1
                    while (x + s * k * dx, y + s * k * dy) in reach and not is_wall(w, x + s * k * dx, y + s * k * dy) and k <= 3:
                        k += 1
                    run += k - 1
                    ends.append(is_wall(w, x + s * k * dx, y + s * k * dy))
                if all(ends) and run <= 3:
                    out.append((x, y))
                    break
    return out


def street_doors(reach, box, inside):
    """Doorway tiles on the building's outer wall line that the walk from the start reaches."""
    x1, y1, x2, y2 = box
    return [p for p in inside if p[0] in (x1, x2) or p[1] in (y1, y2)]


def main():
    w = soswalk.Walk((3590, 2490, 3680, 2600))
    reach = w.flood(START)
    stock = placer.stock_tiles()
    homes = {}
    for r in csv.DictReader(open(os.path.join(TOOLS, "out", "homes.csv"))):
        homes[(int(r["x"]), int(r["y"]))] = r["name"]

    for B, props in ((OFFICE, office_props()), (ALEMBIC, alembic_props())):
        x1, y1, x2, y2 = B["box"]
        cov, _ = buildings.find(x1, y1, x2, y2)
        doors = doorways(w, reach, B["box"])
        street = street_doors(reach, B["box"], doors)
        print("== %s: walls x%d-%d y%d-%d; doorways %s; street door %s" % (B["name"], x1, x2, y1, y2, doors, street))
        near_door = {(dx + a, dy + b) for a, b in doors for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
        floor_props = set()
        for area, name, iid, x, y, z in props:
            print("%-8s %-18s 0x%04X %d,%d,%d" % (area, name, iid, x, y, z))
            kind, tz = townmap.tile(x, y)
            ok(kind == "open" and tz == FLOOR, "townmap.tile(%d,%d) = %s z%d (want open z%d)" % (x, y, kind, tz, FLOOR))
            if z == FLOOR:
                ok(w.stand[(x, y)] == FLOOR, "stands at floor z%d by the walk (stand %s)" % (FLOOR, w.stand[(x, y)]))
                floor_props.add((x, y))
            else:
                items = soswalk.files()["items"]
                tops = surface_top(w, x, y) + [pz + items[pi]["height"] for pa, pn, pi, px, py, pz in props
                                               if (px, py) == (x, y) and pz == FLOOR]
                # an item on a table: the table top is the lowest surface top at or below the item; offsets as before
                ok(any(t <= z <= t + 3 for t in tops) and tops, "on a table or shelf (a surface static, or our own prop): tops %s, item z%d" % (tops, z))
            if area == "outside":
                ok((x, y) not in cov and y == y2 + 1 and x1 <= x <= x2, "outside, south of the hall (uncovered, y%d)" % (y2 + 1))
            else:
                ok((x, y) in cov and x1 < x < x2 and y1 < y < y2, "inside the building (a covered tile)")
            ok((x, y) not in stock, "not a stock tile")
            ok((x, y) not in homes, "not an NPC tile in homes.csv%s" % ("" if (x, y) not in homes else " (" + homes[(x, y)] + ")"))
            ok((x, y) not in near_door, "not on or next to a doorway")
            if name in AGAINST_WALL or (name == "alchemist table" and y == y1 + 1):
                ok(is_wall(w, x, y - 1) or is_wall(w, x - 1, y), "against the north or west wall")

        # The walk with the floor props blocking: street door to each NPC (and around the guildmaster).
        blocked = soswalk.Walk((3590, 2490, 3680, 2600))
        for p in floor_props:
            blocked.stand[p] = None
        breach = blocked.flood(START)
        bare = w
        for npc, p in B["npcs"].items():
            ok(p in breach, "%s at %d,%d reachable from the start with the props in place" % (npc, *p))
            for d in street:
                path = bare.path(d, p) or []
                on = [q for q in path if q in floor_props]
                ok(not on, "no prop on the shortest walk %s -> %s (%s) %s" % (d, p, npc, on or ""))
        if B is ALEMBIC:
            gx, gy = B["npcs"]["Alembic guildmaster"]
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    n = (gx + dx, gy + dy)
                    if n != (gx, gy) and w.stand.get(n) is not None:
                        ok(n in breach, "guildmaster's neighbour %d,%d reachable with the props in place" % n)

        if B is OFFICE:
            bx, by, bz, facing = board()
            print("board    League board       %d,%d,%d facing %s" % (bx, by, bz, facing))
            ok(bz == FLOOR and by == y1 and x1 < bx < x2 and is_wall(w, bx, by), "on the hall's north wall line at floor z")
            below = (bx, by + 1)
            ok(townmap.tile(*below) == ("open", FLOOR) and below in cov and below not in floor_props
               and below not in stock and below not in homes, "the floor tile below it (%d,%d) is open and free" % below)
            pots = [(x, y) for a, n, i, x, y, z in props if n == "flowerpot"]
            ok(any(abs(x - bx) == 1 and y == by + 1 for x, y in pots), "beside the flowerpot %s" % pots)

    print("\n%d failure(s)" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
