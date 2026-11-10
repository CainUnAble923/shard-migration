"""cc-P871 (P866 review, item 1): writes notes/cc-P871-review/placed.md: the six styles' pieces as ArtAt lays them,
then one line per tile of every carpet laid in the TazUO proofs (P857's two 4 by 4s and P871's six non-square ones),
the art chosen by render871.art_at, which follows VariableCarpetStyle.ArtAt read from the code copy."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render871 as R  # noqa: E402

OUT = r"D:\UO\golems\Iron\shard-migration\notes\cc-P871-review\placed.md"
NAMES = ["NW corner", "NE corner", "SE corner", "SW corner", "W edge", "N edge", "E edge", "S edge", "middle"]
CODE_NAMES = ["NorthCorner", "EastCorner", "SouthCorner", "WestCorner", "NorthWestEdge", "NorthEastEdge",
              "SouthEastEdge", "SouthWestEdge", "Middle"]
# (shot, style index, hue, x0, y0, z, width, height)
LAID = [
    ("P857 shots/p857/p857-carpet-laid.jpg", 3, 1157, 1984, 2240, 7, 4, 4),
    ("P857 shots/p857/p857-carpet-blue-gold.jpg", 2, 0, 1984, 2240, 7, 4, 4),
    ("P871 shots/p871-0-blue-patterned-5x3.jpg", 0, 0, 1984, 2240, 7, 5, 3),
    ("P871 shots/p871-1-blue-plain-3x4.jpg", 1, 0, 1984, 2240, 7, 3, 4),
    ("P871 shots/p871-2-blue-with-gold-5x3.jpg", 2, 0, 1984, 2240, 7, 5, 3),
    ("P871 shots/p871-3-red-patterned-3x4.jpg", 3, 0, 1984, 2240, 7, 3, 4),
    ("P871 shots/p871-4-red-plain-5x3.jpg", 4, 0, 1984, 2240, 7, 5, 3),
    ("P871 shots/p871-5-gold-patterned-3x4.jpg", 5, 0, 1984, 2240, 7, 3, 4),
]


def where(x, y, w, h):
    west, east, north, south = x == 0, x == w - 1, y == 0, y == h - 1
    for cond, i in (((west and north), 0), ((east and north), 1), ((east and south), 2), ((west and south), 3),
                    (west, 4), (north, 5), (east, 6), (south, 7)):
        if cond:
            return NAMES[i]
    return NAMES[8]


def main():
    st = R.styles()
    out = ["# cc-P871: placed list for the variable carpet (P857, fixed up after the build review P866)", "",
           "Item IDs are the stock carpet art. \"Map\" directions: x grows east, y grows south; the code names the corners",
           "by the screen (ArtAt's NorthCorner is the map's north-west tile, the top of the screen). Facing: carpet",
           "pieces have one facing each; the piece is chosen by its place in the carpet, nothing is turned.", "",
           "## The six styles, as `VariableCarpetStyle.ArtAt` lays them", "",
           "| # | Style | " + " | ".join("%s (`%s`)" % (n, c) for n, c in zip(NAMES, CODE_NAMES)) + " |",
           "|---|---|" + "---|" * 9]
    for i, (name, s) in enumerate(st):
        out.append("| %d | %s | " % (i, name) + " | ".join("0x%04X" % v for v in s) + " |")
    out += ["", "The red set agrees with the building guide's carpet rule (section 2.5: edges north 0x0ACE, south 0x0AD0,",
            "west 0x0ACD, east 0x0ACF; corners NW 0x0ACA, SE 0x0AC9, NE 0x0ACC, SW 0x0ACB). Renders of every style laid",
            "5 by 3 and 3 by 5: `carpet-<n>-<style>.jpg` and `carpets-all-six.jpg` in this folder.", "",
            "## Carpets laid in the TazUO proofs", "",
            "All in the trainee's own stone-and-plaster house (Trammel, centre 1986,2242, floor z 7), one at a time,",
            "each rolled up before the next.", ""]
    for shot, si, hue, x0, y0, z, w, h in LAID:
        name, s = st[si]
        out.append("### %s, hue %d, %d by %d (x by y), from %d,%d,%d to %d,%d,%d (%s)" % (
            name, hue, w, h, x0, y0, z, x0 + w - 1, y0 + h - 1, z, shot))
        for y in range(h):
            for x in range(w):
                out.append("- 0x%04X, %d,%d,%d, %s" % (R.art_at(s, x, y, w - 1, h - 1), x0 + x, y0 + y, z, where(x, y, w, h)))
        out.append("")
    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print(OUT, len(out))


if __name__ == "__main__":
    main()
