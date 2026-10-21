"""cc-P276 part 1: the tutorial farm's map edit. Removes the two trees inside the west farm's fence (Chase approved,
2026-10-21; the list is design/tutorial-farm/west_v3_layout.json map_edit_remove_statics) by the playbook's route
(notes/map-building-playbook.md section 6): the shard's current patch is applied to scratch copies of the pristine
7.0.117.0 Trammel files, the four statics are removed there, and the patch is made again from pristine and scratch, then
checked by the same tool.

    python -P build_farm_map.py <scratch folder> [--write]

--write replaces player-package/vendor/shattered-legacy-map/trammel.mapops; without it the new patch is written beside
the scratch only. ASCII only.
"""
import json
import os
import shutil
import sys

sys.path.insert(0, r"D:\UO\shard-migration\scripts")
from mapbuild import mapops, uofiles  # noqa: E402

BASE = uofiles.CLIENT
OPS = r"D:\ShatteredLegacy\player-package\vendor\shattered-legacy-map\trammel.mapops"
LAYOUT = r"D:\ShatteredLegacy\design\tutorial-farm\west_v3_layout.json"
FACET = 1
FENCE = (3381, 2603, 3399, 2619)


def main():
    scratch = sys.argv[1]
    write = "--write" in sys.argv
    trees = [(r["x"], r["y"], r["z"], int(r["id"], 16)) for r in json.load(open(LAYOUT))["map_edit_remove_statics"]]
    print("to remove:", ["%d,%d z%d 0x%04X" % t for t in trees])

    # Every static on the two trunk tiles in EA's files, so nothing else on them is touched or missed.
    for (x, y) in sorted({(t[0], t[1]) for t in trees}):
        here = uofiles.statics_in(BASE, FACET, x, y, x, y)
        print("EA statics at %d,%d:" % (x, y), ["z%d 0x%04X" % (s[2], s[3]) for s in here])
        assert sorted(here) == sorted(t for t in trees if (t[0], t[1]) == (x, y)), "the tile holds other statics"

    # No other trunk inside the fence (the mockup's farmsite.blocked was the first count; this is the second).
    td = uofiles.read_tiledata(BASE)
    inside = uofiles.statics_in(BASE, FACET, FENCE[0] + 1, FENCE[1] + 1, FENCE[2] - 1, FENCE[3] - 1)
    blocking = [s for s in inside if uofiles.impassable_item(s[3], BASE)]
    print("impassable statics inside the fence in EA's files:", ["%d,%d 0x%04X" % (s[0], s[1], s[3]) for s in blocking])

    if os.path.isdir(scratch):
        shutil.rmtree(scratch)
    old = open(OPS).read()
    d0, m0 = mapops.apply(old, BASE, scratch, FACET)
    print("the current patch on pristine: drifted %d, removals not found %d" % (len(d0), len(m0)))
    assert not d0 and not m0
    removed, missing = uofiles.remove_statics(scratch, FACET, trees)
    print("removed", removed, "missing", missing)
    assert removed == 4 and not missing

    new = mapops.diff(BASE, scratch, FACET)
    drifted, miss, land_equal, bad = mapops.check(new, BASE, scratch, FACET, scratch=scratch + "-check")
    print("check: drifted %d, missing %d, land identical %s, blocks differing %d" % (len(drifted), len(miss), land_equal, len(bad)))
    assert not drifted and not miss and land_equal and not bad

    old_lines = [l for l in old.splitlines() if l and not l.startswith(("#", "F "))]
    new_lines = [l for l in new.splitlines() if l and not l.startswith(("#", "F "))]
    added = sorted(set(new_lines) - set(old_lines))
    gone = sorted(set(old_lines) - set(new_lines))
    print("lines added:", added)
    print("lines gone:", gone)
    print("F lines:", [l for l in old.splitlines() if l.startswith("F ")], "->", [l for l in new.splitlines() if l.startswith("F ")])

    out = OPS if write else os.path.join(scratch, "trammel.mapops")
    with open(out, "w", newline="\n") as f:
        f.write(new)
    print("wrote", out, len(new), "bytes")


if __name__ == "__main__":
    main()
