"""cc-P856: checks MAIN's winter set rows together (ClusterFWinterSetLayout.cs in the code copy), by find856.py's
rules: each piece fits with the others in place (a tile apart), and the town's walk from the square's start reaches
every tile it reached before with all of them standing. Writes the main section of placed.md (one line per part).

  python -P validate856.py <placed.md out>
Exit 1 on any failure.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import find856 as F  # noqa: E402

LAYOUT = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/WinterSet/ClusterFWinterSetLayout.cs"
DESIGNS = F.DESIGNS


def rows():
    text = open(LAYOUT, encoding="utf-8").read()
    designs = dict(re.findall(r'\["([a-z-]+)"\] = "([a-z-]+)"', text))
    out = []
    for key, area, x, y, z, name in re.findall(r'new\("([a-z-]+)", "([a-z ]+)", (\d+), (\d+), (-?\d+), 0, "([^"]+)"', text):
        out.append((key, area, designs[key], int(x), int(y), int(z), name))
    return out


def parts(design):
    text = open(DESIGNS, encoding="utf-8").read()
    block = text.split('["%s"]' % design, 1)[1].split("]),", 1)[0]
    return [(int(i, 16), int(x), int(y), int(z), n) for i, x, y, z, n in
            re.findall(r'new\(0x([0-9A-F]+), (-?\d+), (-?\d+), (-?\d+), -?\d+, [A-Za-z0-9.]+, (null|"[^"]*")\)', block)]


def main():
    out = sys.argv[1]
    rs = rows()
    bad = 0
    lines = []
    for key, area, design, x, y, z, name in rs:
        os.environ["PLACED"] = ";".join("%s@%d,%d" % (d, ox, oy) for k, a, d, ox, oy, oz, n in rs if k != key)
        ok, errs = F.fits(design, x, y, False, F.taken_tiles())
        status = "ok" if ok and ok[1] == z else "FAIL: %s" % ("; ".join(errs[:5]) if errs else "base z %s, row z %s" % (ok and ok[1], z))
        bad += status != "ok"
        print("%s (%s) at %d,%d,%d: %s" % (key, design, x, y, z, status))
        lines.append("### %s: %s (%s), origin %d,%d,%d, area %s: %s" % (key, name, design, x, y, z, area, status))
        for item, dx, dy, dz, n in parts(design):
            lines.append("- 0x%04X, %d,%d,%d, as made%s" % (item, x + dx, y + dy, z + dz, "" if n == "null" else ", " + n.strip('"')))
        lines.append("")
    # all together
    stand = dict(F.R.W.stand)
    block, inside = set(), set()
    for key, area, design, x, y, z, name in rs:
        tiles = F.design_tiles(design)
        block |= {(x + dx, y + dy) for dx, dy in tiles}
        xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]   # gaps inside a piece's box are the piece's
        inside |= {(i, j) for i in range(x + min(xs), x + max(xs) + 1) for j in range(y + min(ys), y + max(ys) + 1)}
    for t in block:
        stand[t] = None
    saved, F.R.W.stand = F.R.W.stand, stand
    try:
        after = set(F.R.W.flood(F.R.START))
    finally:
        F.R.W.stand = saved
    cut = sorted(F.R.REACH - after - block - inside)
    summary = "All %d pieces together cover %d tiles; the walk from %d,%d reaches every tile it reached before: %s." % (
        len(rs), len(block), F.R.START[0], F.R.START[1], "yes" if not cut else "NO, cut off %d, e.g. %s" % (len(cut), cut[:5]))
    print(summary)
    bad += bool(cut)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("## Main (the Siege of Sosaria New Haven, Trammel)\n\n" + summary + "\n\n" + "\n".join(lines))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
