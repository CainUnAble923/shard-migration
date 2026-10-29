"""cc-P683 (SoS swap S6): the author's dungeon decoration (Zigholtul's SOS Trammel Dungeons.cfg) for Trammel and Felucca.

    python tools/tests/test_sos_dungeon_decoration.py      (SL_SHARD_REPO: another work copy of the shard repo)

Facts, from the author's file, the shard's two cfgs (server/data/Decoration/{Trammel,Felucca}/sos-dungeons.cfg, made by
notes/cc-P683-tools/port.py) and the SoS map:
  1. The shipped cfgs are port.py's output of the unchanged author file: every one of its 200 placements is there, in
     order, active or sealed; its one type is Teleporter (pinned's Server.Items.Teleporter); the Trammel copy's every
     MapDest is Trammel and the Felucca copy's Felucca, the two otherwise the same.
  2. Sealed: no surface Entrance of a dungeon port.OPENED does not hold is active (70 placements); nothing else is
     commented out but the author's unplaced MISC header; and no other shipped teleporter (P679's teleporters-sos.json,
     the decoration cfgs) leads into an author dungeon region from outside it, so a sealed dungeon has no way in.
  3. Walkable: every placement's two ends (all 200) have a floor from 15 below to 5 above their Z on SoS (pinned's
     trigger window, notes/cc-P683-tools/check.py), and no shipped teleporter stands on one of the shipped tiles.
Fact 3 needs the SoS map files; skipped without them.
"""
import importlib
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent.parent
TOOLS = DOCS / "notes" / "cc-P683-tools"
SHARD = Path(os.environ.get("SL_SHARD_REPO", r"D:\ShatteredLegacy"))
os.environ["SL_SHARD"] = str(SHARD)
DECO = SHARD / "server" / "data" / "Decoration"
SOS = DOCS / "notes" / "cc-P481-tools" / "scratch" / "sos" / "Map1.mul"
sys.path.insert(0, str(TOOLS))
HEADER = re.compile(r"^Teleporter 0x1BC3 \(PointDest=\((-?\d+), (-?\d+), (-?\d+)\); MapDest=(\w+)\)$")


def active(path):
    """[(x, y, z, dest, mapdest)] of every active placement of a cfg."""
    out, header = [], None
    for raw in open(path, encoding="utf-8"):
        s = raw.strip()
        if not s:
            header = None
            continue
        if s.startswith("#"):
            continue
        m = HEADER.match(s)
        if m:
            header = m
            continue
        if header is None:
            raise AssertionError(f"{path}: a line with no Teleporter header: {s}")
        x, y, z = (int(v) for v in s.split())
        out.append((x, y, z, tuple(int(header.group(i)) for i in (1, 2, 3)), header.group(4)))
    return out


@unittest.skipUnless((DECO / "Trammel" / "sos-dungeons.cfg").exists(), "needs the shard repo's sos-dungeons.cfg")
class SosDungeonDecoration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = importlib.import_module("port")
        cls.port.SHARD = str(SHARD)
        lines = open(cls.port.SOURCE, encoding="utf-8").read().splitlines()
        cls.rows, cls.placements = cls.port.parse(lines)

    def test_1_the_shipped_cfgs_are_the_ports_of_the_unchanged_author_file(self):
        import hashlib
        self.assertEqual(self.port.SOURCE_SHA256, hashlib.sha256(open(self.port.SOURCE, "rb").read()).hexdigest())
        placed = [p for p in self.placements if p[4] is not None]
        self.assertEqual(200, len(placed))
        self.assertEqual(775, len(self.rows))
        for facet in ("Trammel", "Felucca"):
            text = (DECO / facet / "sos-dungeons.cfg").read_text(encoding="utf-8")
            self.assertEqual(self.port.build(facet, self.rows, self.placements), text, facet)
            self.assertNotIn("MapDest=" + ("Felucca" if facet == "Trammel" else "Trammel"), text)
            self.assertIn("Zigholtul", text.splitlines()[0])
        tr = (DECO / "Trammel" / "sos-dungeons.cfg").read_text(encoding="utf-8")
        self.assertEqual([p[:4] + ("Felucca",) for p in active(DECO / "Trammel" / "sos-dungeons.cfg")],
                         active(DECO / "Felucca" / "sos-dungeons.cfg"))
        types = {s.split(" ")[0] for s in tr.splitlines() if s and not s.startswith("#") and not s[0].isdigit() and not s[0] == "-"}
        self.assertEqual({"Teleporter"}, types)

    def test_2_every_unopened_dungeons_way_in_is_out(self):
        live = active(DECO / "Trammel" / "sos-dungeons.cfg")
        live_at = {(x, y, z) for x, y, z, _, _ in live}
        sealed = [p for p in self.placements if p[4] is not None and p[3] == "Entrance" and p[2] not in self.port.OPENED]
        self.assertEqual(70, len(sealed))
        self.assertEqual(set(), {p[4] for p in sealed} & live_at)
        # everything else ships
        rest = [p for p in self.placements if p[4] is not None and p not in sealed]
        self.assertEqual({p[4] for p in rest}, live_at)
        self.assertEqual(len(rest), len(live))
        # no other shipped teleporter into an author dungeon from outside it
        import check
        rects = check.author_dungeon_rects({p[2] for p in self.placements if p[4] is not None})
        self.assertEqual(25, len(rects))
        ways = []
        tele = json.load(open(SHARD / "server" / "data" / "teleporters-sos.json", encoding="utf-8"))
        ends = [((t["src"]["loc"][0], t["src"]["loc"][1]), (t["dst"]["loc"][0], t["dst"]["loc"][1]), "teleporters-sos.json") for t in tele]
        for f in DECO.glob("*/*.cfg"):
            if f.name == "sos-dungeons.cfg":
                continue
            header = None
            for raw in open(f, encoding="utf-8", errors="replace"):
                s = raw.strip()
                if not s:
                    header = None
                elif not s.startswith("#"):
                    m = re.match(r"^(-?\d+) (-?\d+) (-?\d+)", s)
                    d = re.search(r"PointDest=\((-?\d+), ?(-?\d+)", header) if (m and header) else None
                    if d:
                        ends.append(((int(m.group(1)), int(m.group(2))), (int(d.group(1)), int(d.group(2))), f.name))
                    elif not m:
                        header = s
        for (sx, sy), (dx, dy), where in ends:
            for name, rs in rects.items():
                if check.in_rects(dx, dy, rs) and not check.in_rects(sx, sy, rs):
                    ways.append(f"{where}: {sx},{sy} -> {dx},{dy} into {name}")
        self.assertEqual([], ways)
        self.assertGreater(len(ends), 400)

    @unittest.skipUnless(SOS.exists(), "needs the SoS map files")
    def test_3_every_end_is_walkable_and_no_shipped_teleporter_shares_a_tile(self):
        r = subprocess.run([sys.executable, "-P", str(TOOLS / "check.py")], capture_output=True, text=True,
                           env=dict(os.environ, SL_SHARD=str(SHARD)))
        self.assertEqual(0, r.returncode, r.stderr[-2000:])
        self.assertIn("ends without a floor from 15 below to 5 above: 0", r.stdout)
        self.assertIn("collisions with shipped teleporters on the same tile: 0", r.stdout)
        self.assertIn("shipped teleporters into an author dungeon from outside it: 0", r.stdout)


if __name__ == "__main__":
    unittest.main()
