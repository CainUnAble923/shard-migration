"""cc-P724: a top-down map of the Wakening Isle (x 6594-6865, y 3905-4049) from the built map files: land by kind
(water, sand, grass, dirt/road, rock), static items on top (impassable dark, passable light), the lesson stops and
the planned addon footprints labelled. Usage:
    python -P isle_topdown.py <map folder (map1LegacyMUL.uop, statics1, staidx1)> <out.png> [plan.json]
plan.json: [{"name", "x1", "y1", "x2", "y2"}] rectangles drawn in red (addon footprints).
"""
import json
import os
import sys

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from mapbuild import uofiles  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

X1, Y1, X2, Y2 = 6594, 3905, 6865, 4049
S = 5  # pixels per tile

STOPS = {
    "wake beach": (6638, 3993), "Tamsin": (6640, 3992), "camp": (6656, 3990), "rack/table": (6664, 3990),
    "chat sign": (6692, 3990), "Wren": (6714, 3978), "pests": (6702, 3978), "Pip": (6692, 3975),
    "echo rat": (6736, 3998), "Sera": (6740, 4000), "bank": (6762, 3976), "lodge": (6782, 3999),
    "stones": (6794, 3982), "gate": (6832, 3991), "dock road": (6812, 3991),
}


def kind(name):
    n = name.lower()
    if "water" in n:
        return (40, 70, 160)
    if "sand" in n or "beach" in n:
        return (214, 196, 140)
    if "grass" in n or "jungle" in n or "forest" in n:
        return (80, 140, 60)
    if "dirt" in n or "road" in n or "cobble" in n or "path" in n:
        return (140, 105, 70)
    if "rock" in n or "mountain" in n or "cave" in n:
        return (110, 110, 110)
    if n in ("nodraw", "void", ""):
        return (0, 0, 0)
    return (170, 60, 170)


def main():
    folder, out = sys.argv[1], sys.argv[2]
    plan = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else []
    land_td, items_td = uofiles.read_tiledata()
    mf = uofiles.MapFile(folder, 1)
    im = Image.new("RGB", ((X2 - X1 + 1) * S, (Y2 - Y1 + 1) * S + 14 * len(plan) + 14), (0, 0, 0))
    d = ImageDraw.Draw(im)
    unknown = {}
    for y in range(Y1, Y2 + 1):
        for x in range(X1, X2 + 1):
            tid, z = mf.get(x, y)
            nm = land_td[tid][2]
            c = kind(nm)
            if c == (170, 60, 170):
                unknown[nm] = unknown.get(nm, 0) + 1
            d.rectangle([(x - X1) * S, (y - Y1) * S, (x - X1) * S + S - 1, (y - Y1) * S + S - 1], fill=c)
    for (x, y, z, tid, *_rest) in uofiles.statics_in(folder, 1, X1, Y1, X2, Y2):
        imp = items_td[tid]["flags"] & uofiles.IMPASSABLE
        c = (30, 30, 30) if imp else (190, 190, 150)
        d.rectangle([(x - X1) * S + 1, (y - Y1) * S + 1, (x - X1) * S + S - 2, (y - Y1) * S + S - 2], fill=c)
    for name, (x, y) in STOPS.items():
        px, py = (x - X1) * S + S // 2, (y - Y1) * S + S // 2
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 0))
        d.text((px + 4, py - 6), name, fill=(255, 255, 255))
    for i, r in enumerate(plan):
        d.rectangle([(r["x1"] - X1) * S, (r["y1"] - Y1) * S, (r["x2"] - X1 + 1) * S - 1, (r["y2"] - Y1 + 1) * S - 1],
                    outline=(255, 40, 40))
        d.text(((r["x1"] - X1) * S + 2, (r["y1"] - Y1) * S + 2), str(i + 1), fill=(255, 80, 80))
        d.text((4, (Y2 - Y1 + 1) * S + 2 + 14 * i), "%d %s (%d,%d)-(%d,%d)" % (i + 1, r["name"], r["x1"], r["y1"], r["x2"], r["y2"]), fill=(255, 120, 120))
    for gx in range(X1 - X1 % 10 + 10, X2, 10):
        d.line([((gx - X1) * S, 0), ((gx - X1) * S, 4)], fill=(255, 255, 255))
        if gx % 50 == 0:
            d.text(((gx - X1) * S + 1, 5), str(gx), fill=(255, 255, 255))
    for gy in range(Y1 - Y1 % 10 + 10, Y2, 10):
        d.line([(0, (gy - Y1) * S), (4, (gy - Y1) * S)], fill=(255, 255, 255))
        if gy % 50 == 0:
            d.text((6, (gy - Y1) * S - 5), str(gy), fill=(255, 255, 255))
    im.save(out)
    print("saved", out, im.size, "unclassed land names:", sorted(unknown.items(), key=lambda kv: -kv[1])[:12])


if __name__ == "__main__":
    main()
