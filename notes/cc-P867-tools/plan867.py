"""cc-P867: where each wall-backed design stands in the staged house, for the TazUO run (Walk867.py), the renders
(render867.py) and placed.md (gen_placed.py).

The house: OSI's large brick house (multi 0x74, BrickHouseDeed, offset -1,7,0; the house class is GuildHouse), one
storey under a pitched roof, so the client hides the roof when the trainee stands inside and nothing stands 20 over
the floor. (Runs 2-4 used the two-story stone house 0x78: its upper floor 20 over the ground floor kept the room
covered in the shots and refused the 21-high fireplaces; see the notes.) It stands on Felucca, west of Britain, on
flat grass with no static over 3 high or impassable, no pinned decoration within 12 tiles and no spawner within 25
(found with P856's vanilla facet reader, rel/nhbase.py). Main's New Haven (SoS Trammel) has no such 16 x 17 plot: every
one there holds town paving, farm furrows or trees. The shard put a house aimed at Z 0 there at Z 12 (run 3), so the
floor is Z 19.

The spots are searched, not hand-picked: for each design, every origin where
  - every tile is the house's own floor (wooden boards at multi Z 7, no wall, stair or anything impassable on it);
  - its back row touches its wall: an "east" facing has a plain wall piece west of each tile of its west column, a
    "south" facing one north of each tile of its north row, "northwest" both, "southeast" the south and east walls;
  - no tile is the floor tile in front of a window (guide 11.4 and 11.13);
  - no tile is within one tile of a door (pinned BaseAddon.CouldFit, DoorTooClose);
The first spot in reading order wins. Where no spot passes the door rule, staff stand the piece instead (a spot that
still backs onto its wall clear of windows), and placed.md says so.

  python -P plan867.py            prints MAP, HOUSE, ROUNDS (for Walk867.py) and any design with no spot
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
import decorcfg as D  # noqa: E402

MULTI = 0x74
DEED = "BrickHouseDeed"
HOUSE_TYPE = "guildhouse"
OFFSET = (-1, 7, 0)
MAP = "Felucca"
CX, CY = 1228, 1346
HOUSE_Z = 12
FLOOR = HOUSE_Z + 7
HOUSE = (CX + OFFSET[0], CY + OFFSET[1], 0)   # the deed's target: centre = target - offset
# pinned Houses.cs GuildHouse: AddSouthDoors(-1, 6) (two leaves, -1 and 0), AddSouthDoor(-3, -1), AddSouthDoor(3, -1)
DOORS = [(-1, 6), (0, 6), (-3, -1), (3, -1)]

ROUNDS = [
    ("small-fireplaces", ["grey-fireplace-small-east", "grey-fireplace-small-south"]),
    ("low-fireplaces", ["grey-fireplace-low-east", "grey-fireplace-low-south"]),
    ("medium-fireplaces", ["grey-fireplace-medium-east", "grey-fireplace-medium-south"]),
    ("large-fireplaces", ["grey-fireplace-large-east", "grey-fireplace-large-south"]),
    ("grand-fireplaces", ["grey-fireplace-grand-east", "grey-fireplace-grand-south"]),
    ("country-kitchens", ["country-kitchen-east", "country-kitchen-south"]),
    ("small-kitchens", ["small-kitchen-northwest", "small-kitchen-southeast"]),
    ("harpsichords", ["harpsichord-east", "harpsichord-south"]),
    ("couches", ["blue-couch-east", "blue-couch-south"]),
    ("holiday-fireplace", ["holiday-fireplace"]),
]


def house_cells():
    from mapbuild import isorender as iso, uofiles
    _, items = uofiles.read_tiledata(os.environ["MAPBUILD_CLIENT"])
    sc = iso.Scene.from_multi(MULTI, 26)
    walls, windows, floor, blocked = set(), set(), set(), set()
    for x, y, z, t in sc.statics:
        it = items[t]
        name = it["name"].lower()
        if it["flags"] & 0x10:
            (windows if "wind" in name else walls).add((x, y))
        elif "stair" in name or (it["flags"] & 0x40 and z >= 7):
            blocked.add((x, y))
        elif z == 7 and ("board" in name or "floor" in name):
            floor.add((x, y))
    free = floor - walls - windows - blocked
    global FLOOR_TILES
    FLOOR_TILES = set(free)
    front = set()
    for x, y in windows:
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            if (x + dx, y + dy) in free:
                front.add((x + dx, y + dy))
    near_door = {(x + dx, y + dy) for x, y in DOORS for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    return walls, free - front - near_door, free - front


def fits(design, ox, oy, walls, ok):
    head, parts = D.read(design)
    tiles = {(ox + p[1], oy + p[2]) for p in parts}
    if not tiles <= ok:
        return None
    facing = head.get("facing")
    xs = [t[0] for t in tiles]
    ys = [t[1] for t in tiles]
    west = [(x - 1, y) for x, y in tiles if x == min(xs)]
    north = [(x, y - 1) for x, y in tiles if y == min(ys)]
    east = [(x + 1, y) for x, y in tiles if x == max(xs)]
    south = [(x, y + 1) for x, y in tiles if y == max(ys)]
    need = {"east": west, "south": north, "northwest": west + north, "southeast": east + south}.get(facing)
    if need is None or not all(w in walls for w in need):
        return None
    return tiles


def spot(design, walls, ok):
    for oy in range(-8, 9):
        for ox in range(-8, 9):
            if fits(design, ox, oy, walls, ok):
                return ox, oy
    return None


FLOOR_TILES = set()


def stand_for(design, at):
    """Where the trainee stands for the shot: the floor tile of the piece's own room farthest south-east (the default
    camera looks from the south-east, so the piece and its wall are in front of the trainee)."""
    _, parts = D.read(design)
    tiles = {(at[0] + p[1], at[1] + p[2]) for p in parts}
    seen, todo = set(), [next(iter(tiles))]
    while todo:
        t = todo.pop()
        if t in seen or t not in FLOOR_TILES:
            continue
        seen.add(t)
        todo += [(t[0] + 1, t[1]), (t[0] - 1, t[1]), (t[0], t[1] + 1), (t[0], t[1] - 1)]
    return max(seen - tiles, key=lambda t: (t[0] + t[1], t[0]))


def plan():
    """One design per round: the owner places it from its deed where a spot passes every rule; else staff stand it
    with [DecorAddon place (no house or door rule) at a spot that still backs onto its wall clear of windows."""
    walls, owner_ok, staff_ok = house_cells()
    rounds, missing = [], []
    for _, designs in ROUNDS:
        for design in designs:
            who, at = "owner", spot(design, walls, owner_ok)
            if at is None:
                who, at = "staff", spot(design, walls, staff_ok)
            if at is None:
                missing.append(design)
                continue
            stand = stand_for(design, at)
            rounds.append((design, [(design, D.read(design)[0].get("facing"), CX + at[0], CY + at[1], FLOOR, who)],
                           (CX + stand[0], CY + stand[1], FLOOR)))
    return rounds, missing


def main():
    rounds, missing = plan()
    print("MAP = %r" % MAP)
    print("HOUSE = %r" % (HOUSE,))
    print("ROUNDS = [")
    for name, row, stand in rounds:
        print("    (%r, %r, %r)," % (name, row, stand))
    print("]")
    for m in missing:
        print("NO SPOT", m)
    return rounds, missing


if __name__ == "__main__":
    main()
