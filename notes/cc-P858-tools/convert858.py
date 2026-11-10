"""cc-P858: the fortune teller's wagon as our own C# design table
(server/customizations/FestivalWagon/FortuneTellerWagonDesign.cs), read out of Olorin's YAAAG addon script
(D:/UO/third-party/code/olorin-fortune-teller-wagon/FortTellWagonAddon.cs). Only the numbers are read (item ID, x, y, z,
and for the "complex" parts hue, light and name); no code is taken. P856's convert856.py, one design.

Our change to the design: the author's "ladder" (0x3DB4 at 0,6, z 10: one 10-high block, so the porch at z 21 could not
be reached, "you will have to adjust the z a tad to get inside") is replaced by a real four-step stair up to the south
porch (STAIR below), so a player walks in.

cc-P872 (the build review P868): nothing on the roof (building guide 1.1, 2.3, 2.6). The author's four rune glyphs
(0x4862, 0x4856 twice, 0x4844: hidden window lights in his client, bright green symbols on the shingles in ours) and the
vent sculpture 0x2419 on the ridge are left out (ROOF_OUT), and the black cat on the roof's north-east corner moves down
onto the potion kegs on the south porch, beside the door (CAT_MOVE). The wagon keeps its light from the lantern 0x0A22 on the
porch, the lamp stand 0x4C53 inside and the stained glass window 0xA5F8.

  python -P convert858.py <output .cs>

Prints the part counts against the source's, the footprint and the lights.
"""

import os
import re
import sys

SRC = r"D:\UO\third-party\code\olorin-fortune-teller-wagon\FortTellWagonAddon.cs"
URL = "https://www.servuo.dev/archive/fortune-tellers-wagon.1831/"

# pinned Projects/Server/Items/LightType.cs, in order (only the values this file uses).
LIGHT_NAMES = {0: "ArchedWindowEast", 2: "Circle150", 29: "Circle300"}

SIMPLE = re.compile(r"\{\s*(\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\}")
COMPLEX = re.compile(r"AddComplexComponent\(\s*\(BaseAddon\)\s*this\s*,([^;]*)\)\s*;")

LADDER = (0x3DB4, 0, 6, 10)
WOOD_HUE = 2418   # the wagon's own wood hue (its deck, walls and roof beams)

# cc-P872: parts taken off the roof (item ID, x, y, z as the source has them), and the cat moved off it.
ROOF_OUT = [(0x4862, 2, -2, 52), (0x4856, 2, 3, 50), (0x4856, 0, -1, 56), (0x4844, 0, 3, 56), (0x2419, 1, 1, 53)]
# onto the stack of two potion kegs (0x9E36 at -1,4, z 21 and 26) on the porch's west side, beside the door and off the
# walk from the stair: seen from the default camera (on the driver's bench at the north end the wagon hid it)
CAT_MOVE = ((0x4689, 3, -3, 47), (-1, 4, 31))

# The stair: light wood (building guide 4.2: block 0x0721, north step 0x0722, a "north" step climbs north). The porch
# deck (0x3EB0 at z 18, 3 high) tops out at 21; four steps of 5 reach 20 (the last step up is 1). One step per tile, each
# 5 higher, blocks under the upper steps where the side shows. Two tiles wide, under the porch's two open deck tiles.
STAIR = []
for dx in (0, 1):
    for dy, z in ((9, 0), (8, 5), (7, 10), (6, 15)):
        STAIR.append((0x0722, dx, dy, z, WOOD_HUE, -1, ""))
    STAIR.append((0x0721, dx, 7, 0, WOOD_HUE, -1, ""))
    STAIR.append((0x0721, dx, 6, 0, WOOD_HUE, -1, ""))
    STAIR.append((0x0721, dx, 6, 5, WOOD_HUE, -1, ""))


def parse(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    pieces = []
    m = re.search(r"m_AddOnSimpleComponents\s*=\s*new int\[,\]\s*\{(.*?)\};", text, re.S)
    for g in SIMPLE.findall(m.group(1)):
        pieces.append((int(g[0]), int(g[1]), int(g[2]), int(g[3]), 0, -1, ""))
    for args in COMPLEX.findall(text):
        m2 = re.fullmatch(r'\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*"(.*)"\s*,\s*(\d+)\s*', args)
        item, x, y, z, hue, light = (int(v) for v in m2.groups()[:6])
        name, amount = m2.group(7), int(m2.group(8))
        if amount != 1:
            raise ValueError(f"amount {amount}")
        pieces.append((item, x, y, z, hue, light, name))
    expected = len(SIMPLE.findall(m.group(1))) + len(re.findall(r"AddComplexComponent\(\s*\(BaseAddon\)", text))
    return pieces, expected


def cs(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    out = sys.argv[1]
    pieces, expected = parse(SRC)
    print("source parts %d, read %d" % (expected, len(pieces)))
    ladder = [p for p in pieces if p[:4] == LADDER]
    assert len(ladder) == 1, ladder
    pieces = [p for p in pieces if p[:4] != LADDER] + STAIR
    out_found = [p for p in pieces if p[:4] in ROOF_OUT]   # cc-P872
    assert len(out_found) == len(ROOF_OUT), out_found
    pieces = [p for p in pieces if p[:4] not in ROOF_OUT]
    cats = [i for i, p in enumerate(pieces) if p[:4] == CAT_MOVE[0]]
    assert len(cats) == 1, cats
    item, x, y, z, hue, light, name = pieces[cats[0]]
    pieces[cats[0]] = (item,) + CAT_MOVE[1] + (hue, light, name)
    print("cc-P872: %d roof parts out, the cat moved to %s" % (len(out_found), CAT_MOVE[1]))
    xs = [p[1] for p in pieces]
    ys = [p[2] for p in pieces]
    print("ours: %d parts (the ladder out, %d stair parts in); x %d..%d, y %d..%d" %
          (len(pieces), len(STAIR), min(xs), max(xs), min(ys), max(ys)))
    print("lights:", sorted({(p[0], LIGHT_NAMES[p[5]]) for p in pieces if p[5] >= 0}))
    lines = [
        "// GENERATED by shard-migration notes/cc-P858-tools/convert858.py from the download's component list. Do not edit",
        "// by hand: rerun the script. cc-P858: the fortune teller's wagon by Olorin (" + URL + "),",
        "// stock client art only. Each row: item ID, x, y, z offset from the addon's tile, hue, light (or null), name (or",
        "// null). The author's ladder (0x3DB4 at 0,6) is replaced by a four-step stair up to the south porch (the last rows).",
        "// cc-P872: nothing on the roof: the four rune glyphs and the vent are left out, the black cat sits on the porch kegs.",
        "",
        "#nullable enable",
        "",
        "namespace Server.Items;",
        "",
        "public static class FortuneTellerWagonDesign",
        "{",
        "    public const string Credit = \"Olorin\";",
        "    public const string Source = \"" + URL + "\";",
        "",
        "    public static readonly WagonPart[] Parts =",
        "    [",
    ]
    for item, x, y, z, hue, light, name in pieces:
        lt = ("LightType." + LIGHT_NAMES[light]) if light >= 0 else "null"
        nm = cs(name) if name else "null"
        lines.append("        new(0x%04X, %d, %d, %d, %d, %s, %s)," % (item, x, y, z, hue, lt, nm))
    lines += ["    ];", "}", ""]
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print("wrote", out)


if __name__ == "__main__":
    main()
