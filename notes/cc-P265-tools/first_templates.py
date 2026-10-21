"""cc-P265: writes the FIRST version of design/guild-hall-decor/templates.json. After that the JSON is the source:
tune it by hand (F-49) and re-run `decor.py layout` to regenerate the server table. Running this again overwrites the
design file, so it refuses when the file exists unless --force.

Offsets are tiles from the point staff target (dx east, dy south, dz up). The tower and vat layouts were solved from
the authors' previews (notes, "How the multi-piece art fits"): screen slots (col, row) in 22-pixel steps, turned into
tiles by x = (row + col) / 2, y = (row - col) / 2.

    python -P first_templates.py <ShatteredLegacy repo> [--force]
"""
import json
import os
import sys


def t(col, row):
    assert (col + row) % 2 == 0, (col, row)
    return (row + col) // 2, (row - col) // 2


def P(key, dx, dy, dz=0, hue=0):
    r = {"piece": key, "dx": dx, "dy": dy, "dz": dz}
    if hue:
        r["hue"] = hue
    return r


def I(item, name, dx, dy, dz=0):
    return {"item": item, "name": name, "dx": dx, "dy": dy, "dz": dz}


def at(rows, ox, oy, oz=0):
    return [dict(r, dx=r["dx"] + ox, dy=r["dy"] + oy, dz=r["dz"] + oz) for r in rows]


# ---------------------------------------------------------------- Order of the Alembic
VAT = [P("vat-1", -2, 0), P("vat-4", -1, -1), P("vat-6", 0, -2), P("vat-3", -1, 0), P("vat-5", 0, 0),
       P("vat-7", 0, -1), P("vat-2", 0, 2), P("vat-front", 1, 1), P("vat-8", 2, 0)]
NORTH = []
for i, c in enumerate(["fish", "frog", "hamster", "lobster"]):
    x0 = -6 + 3 * i      # a south-facing stand is two tiles along x: its west half, then its east half under the tank
    NORTH += [P("stand-s2", x0, -6), P("stand-s1", x0 + 1, -6), P(f"tank-{c}-s", x0 + 1, -6, 5)]
WEST = []
for i, c in enumerate(["scorpion", "snake", "tarantula", "turtle"]):
    y0 = -2 + 3 * i      # an east-facing stand is two tiles along y: its north half, then its south half under the tank
    WEST += [P("stand-e2", -6, y0), P("stand-e1", -6, y0 + 1), P(f"tank-{c}-e", -6, y0 + 1, 5)]
BENCH = []
for i in range(8):       # eight counters down the east side, a flask on each (counter height 6)
    BENCH += [I("0x0B3F", "counter", 5, -3 + i), P(f"flask-{i + 1}", 5, -3 + i, 6)]
SCRY = [P("ball-cloth", 2, 5), P("ball-on", 2, 5, 1)]

# ---------------------------------------------------------------- Society of Smiths
FORGE = [P("firepit-lit", 0, 0), I("0x0FB1", "forge", -2, -2), I("0x0FAF", "anvil", 2, 1), P("blacksmith", 3, 1),
         P("firepit-cold", -3, 2)]

# ---------------------------------------------------------------- Artificers
GATE = [P("orb-gate", 0, 0), P("orb-floor", 3, 3), P("crystal-green", -2, 2), P("crystal-purple", 2, -2),
        P("crystal-pillar", -3, -1), P("orb-item", -3, -1, 17), P("crystal-pillar", -1, -3), P("orb-item", -1, -3, 17)]

# ---------------------------------------------------------------- hall structure (each tower: its back tile is 0,0)
# The towers stand in one screen row (+x, -y keeps the depth), spaced so none draws over the next.
LARGE_SLOTS = {"2a": (0, 0), "2b": (2, 0), "2h": (-2, 0), "2c": (3, 1), "a2i": (-3, 1), "2d": (4, 2), "2j": (-4, 2),
               "2e": (4, 4), "2k": (-4, 4), "a2f": (3, 5), "a2la": (-3, 5), "2q": (0, 6), "a2g": (2, 6), "a2ma": (-2, 6)}
LARGE = [P(f"large-{k}", *t(*s)) for k, s in LARGE_SLOTS.items()] + [P("large-turret", *t(0, 6), 20)]
MEDIUM = [P("medium-1a", -1, 1), P("medium-1b", 0, 0), P("medium-1c", 1, -1), P("medium-1d", 1, 3),
          P("medium-1h", 2, 2), P("medium-1e", 3, 1), P("medium-turret", 3, 3, 28)]
SMALL = [P("small-a2a", 0, 0), P("small-a3", 0, 1), P("small-a4", 1, 0), P("small-a8", 1, 1), P("small-top", 1, 1, 22)]
WB_SLOTS = {1: (-4, 0), 2: (-2, 0), 3: (0, 0), 4: (2, 0), 5: (4, 0), 6: (-4, 4), 7: (-2, 4), 12: (0, 4), 9: (2, 4), 10: (4, 4)}
WBRICK = [P(f"wbrick-{k}", *t(*s)) for k, s in WB_SLOTS.items()] + [P("wbrick-dome", *t(0, 4), 24)]
WC_SLOTS = {n + 1: ((n % 5) * 2 - 4, 0 if n < 5 else 4) for n in range(10)}
WCOL = [P(f"wcol-{11 if k == 8 else k}", *t(*s)) for k, s in WC_SLOTS.items()]      # the door on the ground storey
WCOL += [P(f"wcol-{k}", *t(*s), 22) for k, s in WC_SLOTS.items()] + [P("wcol-dome", *t(0, 4), 44)]
RAIL = [P("marble-70298", 0, y) for y in range(0, 4)] + [P("marble-70303", 0, 4)] + \
       [P("marble-70292", x, 4) for x in range(1, 5)] + [P("marble-70388", 6, 2)]

DESIGN = {
    "about": "cc-P265: the guild hall decor templates. Offsets are tiles from the point staff target (dx east, dy south, "
             "dz up). A row names a catalogue piece (notes/cc-P265-tools/decor.py; its art ID is the server's "
             "GuildHallDecorArt) or a stock item (\"item\": hex, with a name). Each set is one staff command; a group "
             "can be placed alone. Placed nowhere: F-49 picks the halls, then tunes these per hall. After an edit, run "
             "shard-migration notes/cc-P265-tools/decor.py layout <repo> to regenerate GuildHallDecorTemplates.cs.",
    "sets": [
        {"key": "alembic", "guild": "Order of the Alembic", "command": "DecorAlembicHall", "groups": [
            {"key": "vat", "about": "Hestia's bubbling vat, the centrepiece (3 tiles across)", "rows": VAT},
            {"key": "tanks-north", "about": "four specimen tanks on stands along the north wall", "rows": NORTH},
            {"key": "tanks-west", "about": "four specimen tanks on stands along the west wall", "rows": WEST},
            {"key": "bench", "about": "the glassware bench: eight counters, a partial-hue flask on each", "rows": BENCH},
            {"key": "scrying", "about": "the crystal ball on its ritual cloth, lit", "rows": SCRY}]},
        {"key": "smiths", "guild": "Society of Smiths", "command": "DecorSmithsHall", "groups": [
            {"key": "forge", "about": "the fire pit with a forge, an anvil and a blacksmith at work; a cold pit by it",
             "rows": FORGE}]},
        {"key": "artificers", "guild": "Artificers' Order", "command": "DecorArtificersHall", "groups": [
            {"key": "gate", "about": "the arc orb gate between two floating crystals, its field before it, and two "
                                     "pillars each holding a small arc orb", "rows": GATE}]},
        {"key": "structure", "guild": "any hall (shared structure)", "command": "DecorHallStructure", "groups": [
            {"key": "tower-large", "about": "Hestia's large brick tower with its turret (9 tiles across)",
             "rows": at(LARGE, 0, 0)},
            {"key": "tower-medium", "about": "the medium brick tower with its turret", "rows": at(MEDIUM, 6, -6)},
            {"key": "tower-small", "about": "the small brick tower with its crenellated top", "rows": at(SMALL, 10, -10)},
            {"key": "tower-white-brick", "about": "the white brick tower with its dome", "rows": at(WBRICK, 14, -14)},
            {"key": "tower-white-column", "about": "the white column tower, two storeys and a dome",
             "rows": at(WCOL, 20, -20)},
            {"key": "balustrade", "about": "an L of marble balustrade with its corner, and a marble ladder",
             "rows": at(RAIL, 0, 10)}]},
    ],
}

if __name__ == "__main__":
    path = os.path.join(sys.argv[1], "design", "guild-hall-decor", "templates.json")
    if os.path.exists(path) and "--force" not in sys.argv:
        sys.exit(f"{path} exists: it is the source now (use --force to start over)")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = json.dumps(DESIGN, indent=1)
    # one row per line, so a hand edit is one line
    import re
    text = re.sub(r"\{\n\s+(\"(?:piece|item)\"[^{}]*?)\n\s+\}", lambda m: "{" + " ".join(m.group(1).split()) + "}", text)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    print("wrote", path)
