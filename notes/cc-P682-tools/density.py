"""cc-P682: the spawn density figures, per 100 dry tiles, against stock's (out\\density.txt).

    python -P density.py

Reads build_spawns.py's out\\density.csv (stock towns, the new towns, stock's wild rate by terrain) and
out\\wild-density-<facet>.csv (each new-land area and terrain: its free dry tiles, stock's rate, the target, placed).
"""
import collections
import csv
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402


def report():
    rows = list(csv.DictReader(open(os.path.join(common.OUT, "density.csv"))))
    lines = []
    for facet in ("Trammel", "Felucca"):
        st = [float(r["per100"]) for r in rows if r["facet"] == facet and r["kind"] == "stock town"]
        lines.append(f"== {facet}")
        lines.append(f"stock towns ({len(st)}): people and town animals per 100 dry tiles, median {statistics.median(st):.3f}, "
                     f"range {min(st):.3f} to {max(st):.3f}")
        for r in rows:
            if r["facet"] == facet and r["kind"] == "new town":
                lines.append(f"  {r['name']:<14} {int(r['spawned']):>4} spawned on {int(r['dry']):>6} dry tiles: {float(r['per100']):.3f}")
        wild = [r for r in rows if r["facet"] == facet and r["kind"] == "stock wild"]
        sd = sum(int(r["dry"]) for r in wild)
        sc = sum(int(r["spawned"]) for r in wild)
        lines.append(f"stock wild (surface, outdoors, outside towns): {sc} creatures on {sd} dry tiles: {100.0 * sc / sd:.3f} per 100")
        for r in wild:
            if int(r["dry"]):
                lines.append(f"  {r['name']:<7} {float(r['per100']):.3f} per 100 ({r['spawned']} on {r['dry']}; {r.get('templates', '')} stock spawners to copy)")
        wd = list(csv.DictReader(open(os.path.join(common.OUT, f"wild-density-{facet.lower()}.csv"))))
        by = collections.defaultdict(lambda: [0, 0.0, 0])
        for r in wd:
            k = r["file"]
            by[k][0] += int(r["dry"])
            by[k][1] += float(r["target"])
            by[k][2] += int(r["placed"])
        td = sum(v[0] for v in by.values())
        tt = sum(v[1] for v in by.values())
        tp = sum(v[2] for v in by.values())
        lines.append(f"new land, free dry tiles (less towns, closures, dungeons, stock-covered): {td}")
        for k, (d, t, p) in sorted(by.items()):
            lines.append(f"  {k:<16} {p:>5} placed on {d:>7} tiles: {100.0 * p / d:.3f} per 100 (stock's rate for its terrain: {100.0 * t / d:.3f})")
        lines.append(f"  all new land     {tp:>5} placed on {td:>7} tiles: {100.0 * tp / td:.3f} per 100 (stock's rate for its terrain: {100.0 * tt / td:.3f})")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    text = report()
    open(os.path.join(common.OUT, "density.txt"), "w").write(text)
    print(text)
