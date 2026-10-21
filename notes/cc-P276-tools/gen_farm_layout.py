"""cc-P276: writes server/customizations/Tutorial/TutorialFarmLayout.cs from the approved v3 layout
(D:/ShatteredLegacy/design/tutorial-farm/west_v3_layout.json, Chase 2026-10-04 "looks good"). Every piece keeps its
tile, art and Z exactly; the wooden door 0x06AD becomes a real door (TutorialFarm places it), so it is left out of the
addon rows and its spot is written as its own constant.

    python -P gen_farm_layout.py
"""
import json

SRC = r"D:\ShatteredLegacy\design\tutorial-farm\west_v3_layout.json"
OUT = r"D:\ShatteredLegacy\server\customizations\Tutorial\TutorialFarmLayout.cs"

d = json.load(open(SRC))
cx, cy = d["farmhouse_center"]
items = d["items"]
door = [i for i in items if i["id"] == "0x06AD"]
assert len(door) == 1
rows = [i for i in items if i["id"] != "0x06AD"]

lines = []
lines.append("// cc-P276: the tutorial farm's pieces, generated from the approved v3 layout (Chase, 2026-10-04 \"looks good\") by")
lines.append("// shard-migration notes/cc-P276-tools/gen_farm_layout.py from design/tutorial-farm/west_v3_layout.json. Do not edit by")
lines.append("// hand: change the layout and run the generator. Every piece is stock art at its tile and Z, absolute Trammel")
lines.append("// coordinates; Z is the client land the mockup was drawn on (the farm sits on unpatched land: P276's map patch only")
lines.append("// removes two trees). The wooden door 0x06AD is not a row: TutorialFarm places a real door at DoorSpot.")
lines.append("")
lines.append("namespace Server.Tutorial;")
lines.append("")
lines.append("public static class TutorialFarmLayout")
lines.append("{")
lines.append("    /// <summary>The farmhouse's centre (the addon's anchor) and the lowest Z under it.</summary>")
lines.append("    public static readonly Point3D Anchor = new(%d, %d, %d);" % (cx, cy, d["base_z"]))
lines.append("")
lines.append("    /// <summary>The farmhouse door (east wall), dark wood, closed art 0x06AD.</summary>")
lines.append("    public static readonly Point3D DoorSpot = new(%d, %d, %d);" % (door[0]["x"], door[0]["y"], door[0]["z"]))
lines.append("")
lines.append("    /// <summary>The two map statics P276's map patch removes (trunk and foliage of each tree): id, x, y, z.</summary>")
lines.append("    public static readonly (int Id, int X, int Y, int Z)[] RemovedTrees =")
lines.append("    [")
for r in d["map_edit_remove_statics"]:
    lines.append("        (%s, %d, %d, %d), // %s" % (r["id"], r["x"], r["y"], r["z"], r["name"]))
lines.append("    ];")
lines.append("")
lines.append("    /// <summary>Every piece: art id, x, y, z (%d rows).</summary>" % len(rows))
lines.append("    public static readonly (int Id, int X, int Y, int Z)[] Pieces =")
lines.append("    [")
for r in rows:
    name = r["name"].replace("%s%", "s")
    lines.append("        (%s, %d, %d, %d), // %s" % (r["id"], r["x"], r["y"], r["z"], name))
lines.append("    ];")
lines.append("}")

with open(OUT, "w", newline="\n") as f:
    f.write("\n".join(lines) + "\n")
print("wrote", OUT, len(rows), "pieces; door", door[0])
