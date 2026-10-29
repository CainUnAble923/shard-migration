r"""cc-P683 (SoS swap S6): the author's dungeon decoration (SOS Trammel Dungeons.cfg, 775 lines) for Trammel and Felucca.

    python -P port.py      writes the shard's two cfgs (server\data\Decoration\{Trammel,Felucca}\sos-dungeons.cfg in
                           the code copy) and out\teleporters.csv (every placement, both ends, shipped or sealed)

The author's file is already in the cfg syntax pinned's DecorationList reads (P694, Valorite: "No type or coordinate
translation is needed"). Its one type is ServUO's Server.Items.Teleporter, which is pinned's Server.Items.Teleporter
(same name, item 0x1BC3, PointDest and MapDest). Every line is kept, in order, after our header; three things change:
  - the surface "Entrance" blocks of every dungeon not in OPENED are commented out ("# S6 SEALED: "), so a sealed
    dungeon has no way in; its exits, level links and inner teleporters stay, harmless without the way in;
  - the last MISC header, which places nothing, is commented ("# S6 UNPLACED: "), so it is visibly not an entrance;
  - the Felucca copy says MapDest=Felucca, so travel stays on the facet it was loaded on (Teleporter.cs: a non-null
    MapDest picks the destination map).
S18 opens a dungeon by adding its name to OPENED and running this again, once its monsters are in.
"""
import csv
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
DOCS = os.path.dirname(NOTES)
SHARD = os.environ.get("SL_SHARD", os.path.join(os.path.dirname(DOCS), "ShatteredLegacy"))
SOURCE = os.path.join(NOTES, "sos-author-data", "SOS-Trammel-Dungeons.cfg")
SOURCE_SHA256 = "40fe3e9260672436df655a885b3547eeef61c0956eb724da1a1f8df08bf1f2d4"
OUT = os.path.join(HERE, "out")

# Dungeons S18 has opened (spawned): their surface entrances ship. None yet (Chase 10-27: "seal the author's dungeons
# until each has monsters").
OPENED = []

HEADER = re.compile(r"^Teleporter 0x1BC3 \(PointDest=\((-?\d+), (-?\d+), (-?\d+)\); MapDest=Trammel\)$")
COORD = re.compile(r"^(-?\d+) (-?\d+) (-?\d+)$")


def parse(lines):
    """Each line with its dungeon and section; each placement as (header index, coord index, dungeon, section, src, dst)."""
    dungeon = section = None
    rows, placements = [], []
    i = 0
    while i < len(lines):
        s = lines[i].rstrip("\n")
        if s.startswith("## ") and i > 0 and lines[i - 1].startswith("####") and i + 1 < len(lines) and lines[i + 1].startswith("####"):
            dungeon, section = s[3:].strip(), None
        elif s.startswith("## ") and not s.startswith("####"):
            section = s[3:].strip()
        m = HEADER.match(s)
        if m:
            c = COORD.match(lines[i + 1].rstrip("\n")) if i + 1 < len(lines) else None
            dst = tuple(int(v) for v in m.groups())
            if c:
                placements.append((i, i + 1, dungeon, section, tuple(int(v) for v in c.groups()), dst))
            else:
                placements.append((i, None, dungeon, section, None, dst))
        rows.append(s)
        i += 1
    return rows, placements


def sealed(p):
    return p[4] is not None and p[3] == "Entrance" and p[2] not in OPENED


def build(facet, rows, placements):
    out = list(rows)
    for p in placements:
        hi, ci = p[0], p[1]
        if ci is None:
            out[hi] = "# S6 UNPLACED: " + out[hi]
        elif sealed(p):
            out[hi] = "# S6 SEALED: " + out[hi]
            out[ci] = "# S6 SEALED: " + out[ci]
    if facet == "Felucca":
        out = [r.replace("MapDest=Trammel", "MapDest=Felucca") for r in out]
    shut = sorted({p[2] for p in placements if sealed(p)})
    n_sealed = sum(1 for p in placements if sealed(p))
    n_live = sum(1 for p in placements if p[1] is not None and not sealed(p))
    head = [
        "# Siege of Sosaria: the author's dungeon decoration. Author: Zigholtul, Siege of Sosaria Trammel Map 3.0",
        "# (SOS Trammel Dungeons.cfg, used with credit). Ported for Shattered Legacy by cc-P683 (SoS swap S6), from P694.",
        f"# This copy is {facet}'s: load it on {facet} only; every MapDest is {facet}. Types: ServUO's",
        "# Server.Items.Teleporter = pinned's Server.Items.Teleporter (item 0x1BC3); no type without a match.",
        f"# {n_live} placements ship. Sealed until S18 spawns the dungeon (Chase 10-27), their surface entrances",
        f"# commented out with \"# S6 SEALED: \" ({n_sealed} placements). Made by shard-migration notes/cc-P683-tools/port.py;",
        "# to open a dungeon, add it to OPENED there and run it again. The sealed dungeons:",
    ]
    line = "#  "
    for d in shut:
        if len(line) + len(d) + 2 > 118:
            head.append(line.rstrip(", "))
            line = "#  "
        line += d + ", "
    head.append(line.rstrip(", "))
    head.append("# The last MISC header places nothing in the author's file and is kept as a comment (\"# S6 UNPLACED: \").")
    head.append("")
    return "\n".join(head + out) + "\n"


def main():
    raw = open(SOURCE, "rb").read()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        sys.exit("the author's file changed: " + hashlib.sha256(raw).hexdigest())
    lines = raw.decode("utf-8").splitlines()
    rows, placements = parse(lines)
    for facet in ("Trammel", "Felucca"):
        path = os.path.join(SHARD, "server", "data", "Decoration", facet, "sos-dungeons.cfg")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(build(facet, rows, placements))
        print("wrote", path)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "teleporters.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_line", "dungeon", "section", "x", "y", "z", "dest_x", "dest_y", "dest_z", "state"])
        for p in placements:
            if p[1] is None:
                w.writerow([p[0] + 1, p[2], p[3], "", "", "", *p[5], "unplaced (comment)"])
                continue
            w.writerow([p[0] + 1, p[2], p[3], *p[4], *p[5], "sealed until S18" if sealed(p) else "ships"])
    print(len(lines), "source lines;", sum(1 for p in placements if p[1] is not None), "placements;",
          sum(1 for p in placements if sealed(p)), "sealed;", len({p[2] for p in placements if p[1] is not None}), "dungeons with placements")


if __name__ == "__main__":
    main()
