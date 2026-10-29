"""cc-P682 exploration: one town's reach, roofs and outdoor tiles, as a small ASCII map (. reach, # roofed reach,
r roofed unreached, o standable unreached, space nothing)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import build_spawns as bs  # noqa: E402

name = sys.argv[1]
regs = common.regions()
rec = next(r for r in common.region_records() if r.get("Name") == name)
start = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (rec["GoLocation"]["x"], rec["GoLocation"]["y"])
t = bs.Town(name, regs[name], start, margin=int(sys.argv[4]) if len(sys.argv) > 4 else 6)
print(name, "box", t.x1, t.y1, t.x2, t.y2, "start", start, "inside", int(t.inside.sum()), "roofed", int(t.roofed.sum()),
      "reach", int(t.reach.sum()), "outdoor", len(t.outdoor()), "buildings", len(t.buildings))
step = max(1, (t.x2 - t.x1) // 110)
for y in range(0, t.stand.shape[1], step):
    row = ""
    for x in range(0, t.stand.shape[0], step):
        s = t.stand[x, y] != common.NONE
        row += ("#" if t.roofed[x, y] else ".") if t.reach[x, y] else ("r" if t.roofed[x, y] and s else ("o" if s else " "))
    print(row)
