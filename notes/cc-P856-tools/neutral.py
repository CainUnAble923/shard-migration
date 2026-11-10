"""cc-P856: one-off. The seeder's new header named main's spots; it now points at the layout file, the same text on main
and on the release copy. python -P neutral.py <code copy folder>"""
import os
import sys

p = os.path.join(sys.argv[1], "server", "customizations", "ClusterFWinterDecorSeeder.cs")
s = open(p, encoding="utf-8").read()
old = """// cc-P856: the rows are P678's layout (ClusterFWinterDecorLayout) and the winter set's (ClusterFWinterSetLayout: the
// Christmas train, the snowman and Santa benches in the park west of the hall, the large snow globe in the garden south
// of the square), whose layer "addon" makes a WinterSeasonAddon instead of a WinterDecor."""
new = """// cc-P856: the rows are the layout's (ClusterFWinterDecorLayout) and the winter set's (ClusterFWinterSetLayout: the
// Christmas train, the snowman and Santa benches and the large snow globe; that file says where each stands), whose
// layer "addon" makes a WinterSeasonAddon instead of a WinterDecor."""
assert s.count(old) == 1, p
s = s.replace(old, new)
s = s.replace("(bank, square, main road, inn, entrance, healer hall, field office, docks, park)",
              "(bank, square, main road, inn, entrance, healer hall, field office, docks, and the winter set's: "
              + ("east, west" if "p856-isle" in p else "park") + ")")
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok", p)
