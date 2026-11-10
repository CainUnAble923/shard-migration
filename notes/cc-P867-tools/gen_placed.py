"""cc-P867: writes notes/cc-P867-review/placed.md from the design files (decorcfg.py) and the staged-house rounds
(render867.py's placed-rows.txt). ASCII only.

  python -P gen_placed.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decorcfg as D  # noqa: E402

OUT = os.path.join(HERE, "..", "cc-P867-review", "placed.md")

# what each facing means in a house (read from the art in decorcfg.py room renders and the in-game shots)
WALL = {
    "east": "faces east; its back against a **west** wall",
    "south": "faces south; its back against a **north** wall",
    "west": "faces west; its back against an **east** wall (the camera-side wall: the client draws that wall over it)",
    "north": "faces north; its back against a **south** wall (the camera-side wall)",
    "northwest": "an L counter in a room's **north-west corner**, against the north and west walls",
    "southeast": "an L counter in a room's **south-east corner**, against the south and east walls (camera side)",
    "east-west": "free-standing; the table's long side runs east-west",
    "north-south": "free-standing; the table's long side runs north-south",
}
NOTE = {
    "harpsichord-east": "facing chosen by the converter from the art's name (tiledata \"Harpsichord EAST\", the download's "
                        "file pianomodern2 names none); the render and shot agree: keyboard on its east side, bench east of it",
    "harpsichord-south": "facing chosen by the converter from the art's name (tiledata \"Harpsichord SOUTH\", file "
                         "pianomodern); the render and shot agree: keyboard on its south side, bench south of it",
    "holiday-fireplace": "cc-P867: the download's own fieldstone wall box (post 0x001D, four 0x001C, two 0x001B) left "
                         "out, so the hearth's stone surround stands against the house's own north wall (P864 item 3)",
}


def wall_text(head, design):
    f = head.get("facing", "as made")
    if design.startswith("barbecue-"):
        return "free-standing grill (outdoor or a kitchen), cook side to the %s" % f
    if f.startswith("style"):
        return "free-standing, " + f
    return WALL.get(f, f)


def main():
    lines = [
        "# cc-P867 placed list: P855's decor addons (fix-up of P864's review)",
        "",
        "Nothing here is placed in the world by a seeder: every piece is a house addon a player places from a deed (or staff",
        "with `[DecorAddon place`). Part 1 is one line per design file (P864 item 1). Part 2 is every piece the trainee",
        "placed in the staged house (P864 items 2 and 3): item ID, location x,y,z, the design it belongs to and the wall.",
        "No piece of any design was turned; a facing is a whole file.",
        "",
        "## 1. The 30 designs (server/data/Decoration/Addons/*.cfg)",
        "",
        "| File | Pieces | Facing | Where it stands in a house | Note |",
        "|---|---|---|---|---|",
    ]
    total = 0
    for d in D.designs():
        head, p = D.read(d)
        total += len(p)
        lines.append("| %s | %d | %s | %s | %s |" % (d, len(p), head.get("facing", "as made"), wall_text(head, d),
                                                   NOTE.get(d, "")))
    lines += ["", "%d pieces in 30 files (P855 had 649: the holiday fireplace lost its 7 wall pieces)." % total, ""]

    lines += [
        "## 2. Against real walls in main's New Haven (the shots)",
        "",
        "Each wall-backed design stood by staff (`[DecorAddon place`, no house rules) inside a New Haven building on main",
        "(SoS Trammel), at the spot `notes/cc-P867-tools/town867.py` found: every tile on the building's floor at one Z,",
        "reached on foot, not protected (doors, NPC posts, spawners, seeded rows), nothing with height standing on it; the",
        "back row against a full plain wall at that floor (no window); no tile in front of a window. The trainee stood",
        "south-east of it in the same room for the shot (`shots/p867-<design>.jpg`, the default camera, roof hidden",
        "inside); `town-<design>.jpg` is the isorender of the same spot (roofs cut). Staff cleared each before the next.",
        "No piece was turned.",
        "",
    ]
    rows = [r.split("|") for r in open(os.path.join(HERE, "town-rows.txt")).read().split(chr(10)) if r]
    cur = None
    for design, facing, tid, at in rows:
        if design != cur:
            cur = design
            lines += ["", "### %s (faces %s): %s" % (design, facing, wall_text(D.read(design)[0], design).replace("its back against a ", "against the building's ").replace("**", "")), ""]
        lines.append("- %s, %s, %s" % (tid, at, design))
    lines += [
        "",
        "## 3. Placed by the owner from a deed, in a house they own (run 4)",
        "",
        "OSI's two-story stone and plaster house (multi 0x78, TwoStoryHouse) placed by staff on Felucca at 1228,1346,12",
        "and handed to the trainee (Owner set). The trainee double-clicked each deed, picked the facing in the deed's",
        "window and targeted the ground floor (Z 19) by the room's west wall: these three were placed (the deed used up;",
        "`notes/cc-P867-tools/run4/walk.txt`):",
        "",
        "- grey-fireplace-small-east, origin 1222,1349,19, faces east, against the west wall",
        "- country-kitchen-east, origin 1222,1349,19, faces east, against the west wall",
        "- blue-couch-east, origin 1222,1349,19, faces east, against the west wall",
        "",
        "The rest of that run's tries were refused by pinned's house rules (unchanged), and the walk did not record which",
        "rule. Known from the code and the data: the medium and grand fireplaces are 21 high, one more than a classic",
        "storey, so they cannot stand under an upper floor 20 over theirs; and no piece may stand within a tile of a door.",
        "That house's upper storey also kept the room covered from the camera, so the shots are section 2's.",
    ]
    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print(OUT, len(lines))


if __name__ == "__main__":
    main()
