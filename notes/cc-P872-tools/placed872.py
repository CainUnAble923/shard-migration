# cc-P872 (P858's placed858.py): writes notes/cc-P872-review/placed.md: one line per placed part (the wagon's 207, at main's default origin),
# with the art's own name from the client's tiledata. Read only.
import os, re, sys
sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\scripts")
from mapbuild import uofiles as U
_, items = U.read_tiledata(r"D:\UO\tool-trials\client-data-copy")
DESIGN = r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\FestivalWagon\FortuneTellerWagonDesign.cs"
OX, OY, OZ = 3647, 2632, 0
rows = re.findall(r'new\(0x([0-9A-F]+), (-?\d+), (-?\d+), (-?\d+), (\d+), ([A-Za-z.0-9]+), (null|"[^"]*")\)', open(DESIGN, encoding="utf-8").read())
out = open(os.path.join(os.path.dirname(__file__), "..", "cc-P872-review", "placed.md"), "w", encoding="utf-8", newline="\n")
w = out.write
w("# cc-P872 review (fix-up of P858 after P868): what is placed in the world\n\n")
w("Two things are placed, both only while a festival season is on (FestivalMarket, `RewardStores/FestivalStore.cs`):\n"
  "the Festival stall as before (P760's six things, unchanged, `notes/cc-P760-review/placed.md`) and now the fortune\n"
  "teller's wagon beside it. The lamps are store items, placed by players; nothing seeds a lamp.\n\n")
w("## The wagon (addon `FortuneTellerWagon`)\n\n")
w("### What cc-P872 changed (the build review P868)\n\n"
  "Nothing on the roof (building guide 1.1, 2.3, 2.6). Out of the design: the rune glyphs 0x4862 at 3649,2630,52,\n"
  "0x4856 at 3649,2635,50, 0x4856 at 3647,2631,56 and 0x4844 at 3647,2635,56 (the author's hidden window lights,\n"
  "drawn as green symbols on the shingles), and the vent sculpture 0x2419 at 3648,2633,53 on the ridge. Moved: the\n"
  "black cat 0x4689 from the roof's corner at 3650,2629,47 down onto the two potion kegs 0x9E36 (z 21 and 26) on the\n"
  "south porch's west side, at **3646,2636,31**, beside the door and off the walk from the stair, its line kept. The\n"
  "wagon keeps its light from the porch\n"
  "lantern 0x0A22, the lamp stand 0x4C53 inside and the stained glass window 0xA5F8. Every other part is as P858\n"
  "had it.\n\n")
w("- Origin **%d,%d,%d** Trammel (setting `clusterf.festival.wagonAt`, default), main's New Haven (the Siege of Sosaria\n"
  "  land): the west edge of the paved square, south of the open forge, 8 tiles east of the stall's barrel. Its long side\n"
  "  runs north-south; the stair comes down the south end onto the street, climbing north. One variant only (no east/south\n"
  "  versions of this design exist); nothing turned.\n" % (OX, OY, OZ))
w("- Footprint x %d..%d, y %d..%d (with the stair); the stair's foot is %d,%d and %d,%d.\n" % (OX - 2, OX + 3, OY - 6, OY + 9, OX, OY + 10, OX + 1, OY + 10))
w("- Seeded with the stall, by serial, taken down with it; a world whose stall is already up gets it at the next load or\n  hourly check (`TopUpWagon`).\n\n")
w("### Our change: the stair (14 parts, light wood 0x0721 block / 0x0722 north step, hue 2418 as the wagon's wood)\n\n")
w("| Item | Location | Facing | What |\n|---|---|---|---|\n")
for i, x, y, z, hue, light, name in rows:
    if int(i, 16) in (0x0721, 0x0722):
        w("| 0x%s %s | %d,%d,%d | %s | %s |\n" % (i, items[int(i, 16)]["name"], OX + int(x), OY + int(y), OZ + int(z),
          "climbs north" if i == "0722" else "-", "step" if i == "0722" else "block under the upper steps"))
w("\nThe author's ladder 0x3DB4 (a 10-high block at 0,6, z 10) is left out.\n\n")
w("### Every part (%d), one line each\n\n| # | Item | Name (tiledata) | Location | Hue | Light | Shown name |\n|---|---|---|---|---|---|---|\n" % len(rows))
for n, (i, x, y, z, hue, light, name) in enumerate(rows, 1):
    w("| %d | 0x%s | %s | %d,%d,%d | %s | %s | %s |\n" % (n, i, items[int(i, 16)]["name"], OX + int(x), OY + int(y), OZ + int(z),
      hue, light.replace("LightType.", "") if light != "null" else "-", name.strip('"') if name != "null" else "-"))
out.close()
print(len(rows), "rows")
