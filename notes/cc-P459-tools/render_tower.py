"""cc-P459: render a guild hall tower from the design file, its door closed and open, with P265's client-geometry renderer.

    python -P render_tower.py <ShatteredLegacy repo> <group key> <out.png>

Closed: every row. Open: the door row left out (the open door is unseen; the doorway shows what is behind it). Hidden
rows (the invisible side walls) are never drawn. Stock art (the floors) comes from the classic client's art.mul.
"""
import os
import sys

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\ClassicUO\ClassicUO\Ultima Online Classic")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cc-P265-tools"))
import decor  # noqa: E402
from PIL import Image  # noqa: E402

repo, key, out = sys.argv[1], sys.argv[2], sys.argv[3]
_, _, d = decor.load_design(repo)
group = next(g for s in d["sets"] for g in s["groups"] if g["key"] == key)
rows = [r for r in group["rows"] if not r.get("hidden")]
shut = [(decor.row_id(r), r["dx"], r["dy"], r["dz"]) for r in rows]
opened = [(decor.row_id(r), r["dx"], r["dy"], r["dz"]) for r in rows if not r.get("door")]
a, b = decor.compose_rows(shut, repo), decor.compose_rows(opened, repo)
sheet = Image.new("RGBA", (a.width + b.width + 16, max(a.height, b.height)), (24, 24, 30, 255))
sheet.alpha_composite(a, (0, 0))
sheet.alpha_composite(b, (a.width + 16, 0))
sheet.save(out)
print(out, sheet.size)
