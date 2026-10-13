"""cc-P92: the ServUO port list (tools/port-list.json) as progress.py counts it, and the page headline it drives.

    python -m unittest tools/tests/test_port_list.py

Every fact builds a small fake ServUO tree, stems file, customizations folder and port list in a temporary folder;
nothing reads the real trees except the last fact, which checks the real tools/port-list.json is well formed.
Standard library only. ASCII only.
"""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import progress  # noqa: E402
import render_dashboard as rd  # noqa: E402


class Fixture(object):
    def __init__(self, systems, files, stock=(), ported=()):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.servuo = root / "servuo"
        self.shard = root / "shard"
        for f in files:
            p = self.servuo / "Scripts" / f
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("// test", encoding="utf-8")
        cust = self.shard / "server" / "customizations"
        cust.mkdir(parents=True)
        for stem in ported:
            (cust / (stem + ".cs")).write_text("// ours", encoding="utf-8")
        self.stems = root / "stems.txt"
        self.stems.write_text("\n".join(stock) + "\n", encoding="utf-8")
        self.list = root / "port-list.json"
        self.list.write_text(json.dumps({"tiers": {"port": "counts"}, "systems": systems}), encoding="utf-8")

    def run(self):
        return progress.port_list(self.list, self.servuo, self.shard, self.stems)

    def close(self):
        self.tmp.cleanup()


def system(sid, tier, prefixes, exclude=None, title=None):
    return {"id": sid, "tier": tier, "title": title or sid, "feeds": "", "prefixes": prefixes, "exclude": exclude}


class PortList(unittest.TestCase):
    def tearDown(self):
        for f in getattr(self, "fx", []):
            f.close()

    def make(self, *a, **k):
        f = Fixture(*a, **k)
        self.fx = getattr(self, "fx", []) + [f]
        return f.run()

    def by_id(self, pl):
        return {r["id"]: r for r in pl["systems"]}

    def test_a_file_goes_to_the_first_matching_system_only(self):
        pl = self.make([system("narrow", "port", ["Items/Tools/Special/"]), system("wide", "port", ["Items/Tools/"])],
                       ["Items/Tools/Special/Hammer.cs", "Items/Tools/Saw.cs"])
        r = self.by_id(pl)
        self.assertEqual((1, 1), (r["narrow"]["candidates"], r["wide"]["candidates"]))
        self.assertEqual(2, pl["candidates"])

    def test_exclude_passes_the_file_on_to_a_later_system(self):
        pl = self.make([system("food", "port", ["Items/Consumables/"], exclude="Token|Deed"),
                        system("dropped", "drop", ["Items/Consumables/"])],
                       ["Items/Consumables/Apple.cs", "Items/Consumables/NameChangeToken.cs",
                        "Items/Consumables/BlessDeed.cs"])
        r = self.by_id(pl)
        self.assertEqual((1, 2), (r["food"]["candidates"], r["dropped"]["candidates"]))

    def test_stock_files_are_not_candidates_and_ours_count_as_done(self):
        pl = self.make([system("s", "port", ["Items/"])], ["Items/Apple.cs", "Items/Pear.cs", "Items/Plum.cs"],
                       stock=["apple"], ported=["Pear"])
        r = self.by_id(pl)["s"]
        self.assertEqual((2, 1, False), (r["candidates"], r["done"], r["complete"]))

    def test_an_unassigned_file_is_reported_not_dropped(self):
        pl = self.make([system("s", "port", ["Items/Tools/"])], ["Items/Tools/Saw.cs", "Mobiles/New/Gremlin.cs"])
        self.assertEqual(1, pl["unassigned"])
        self.assertEqual(["Mobiles/New/Gremlin.cs"], pl["unassigned_first"])
        self.assertEqual(2, pl["candidates"])

    def test_uncounted_tiers_never_move_the_headline(self):
        files = ["Items/Tools/Saw.cs", "Items/Addons/Fountain.cs", "Items/Addons/Statue.cs"]
        systems = [system("tools", "port", ["Items/Tools/"]), system("addons", "reward", ["Items/Addons/"])]
        before = self.make(systems, files)
        after = self.make(systems, files, ported=["Fountain", "Statue"])
        self.assertEqual(before["counted"], after["counted"], "porting reward-pool files moves nothing")
        self.assertEqual(progress.port_list_headline(before), progress.port_list_headline(after))
        self.assertEqual(2, after["tiers"]["reward"]["done"], "but the tier itself shows them")
        decide = self.make(systems + [system("pets", "decide", ["Items/Pets/"])], files + ["Items/Pets/Leash.cs"])
        self.assertEqual((1, 1), (decide["counted"]["systems"], decide["counted"]["total"]),
                         "a decide row waits on Chase; it is not counted until moved to port")

    def test_the_headline_names_the_first_port_system_not_in(self):
        pl = self.make([system("a", "port", ["Items/A/"], title="Alpha"), system("b", "port", ["Items/B/"], title="Beta"),
                        system("c", "port", ["Items/C/"], title="Gamma")],
                       ["Items/A/One.cs", "Items/B/Two.cs", "Items/C/Three.cs"], ported=["One", "Three"])
        self.assertEqual("Beta", pl["next"], "Alpha is in; Gamma is in but comes after Beta")
        self.assertEqual("Port list: 2 of 3 systems in. 2 of 3 files (67%).", progress.port_list_headline(pl))
        page = rd.headline_html({"port_list": pl})
        self.assertIn("Next to land: Beta.", page)
        self.assertIn("2 / 3", page)
        everything = self.make([system("a", "port", ["Items/A/"])], ["Items/A/One.cs"], ported=["One"])
        self.assertIsNone(everything["next"])

    def test_the_page_lists_decide_rows_and_collapses_uncounted_tiers(self):
        pl = self.make([system("a", "port", ["Items/A/"], title="Alpha"),
                        system("p", "decide", ["Items/P/"], title="Pets"),
                        system("r", "reward", ["Items/R/"], title="Rugs")],
                       ["Items/A/One.cs", "Items/P/Two.cs", "Items/R/Three.cs"])
        out = rd.portlist_html({"port_list": pl, "content_progress": []})
        self.assertIn("waiting on Chase", out)
        self.assertIn("<details><summary><strong>Reward pool</strong>: 1 files", out)
        self.assertNotIn("waiting on Chase", rd.portlist_html({"port_list": self.make(
            [system("a", "port", ["Items/A/"])], ["Items/A/One.cs"]), "content_progress": []}))

    def test_the_real_port_list_is_well_formed(self):
        pl = json.loads((HERE.parent / "port-list.json").read_text(encoding="utf-8"))
        ids = [s["id"] for s in pl["systems"]]
        self.assertEqual(len(ids), len(set(ids)), "ids are unique")
        for s in pl["systems"]:
            self.assertIn(s["tier"], progress.TIER_ORDER, s["id"])
            self.assertTrue(s["prefixes"], s["id"])
            if s.get("exclude"):
                re.compile(s["exclude"])
        port = [s for s in pl["systems"] if s["tier"] == "port"]
        self.assertEqual(16, len(port), "Chase, 2026-10-13: Pet Training joined the 15")
        titles = [s["title"] for s in port]
        self.assertEqual(titles.index(next(t for t in titles if t.startswith("Creatures"))) + 1,
                         titles.index(next(t for t in titles if t.startswith("Pet Training"))),
                         "Pet Training sits right after Creatures")
        self.assertFalse([s for s in pl["systems"] if s["tier"] == "decide"], "no decide row is left")


if __name__ == "__main__":
    unittest.main()
