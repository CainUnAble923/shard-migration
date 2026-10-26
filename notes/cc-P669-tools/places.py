r"""cc-P669: our named places and EA's later areas against SoS 3.0, and the blocks trammel.mapops writes.

    python -P places.py   -> out\places.csv, out\mapops-blocks.csv (printed too)

For each rectangle: tiles whose land (id or Z) differs, statics in stock and in SoS, statics only in one, dry tiles in
each. A rectangle where SoS has far fewer statics than stock, and the stock ones are gone, is EA content SoS lacks.
"""
import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))
import islands  # noqa: E402
import sosdiff  # noqa: E402
from mapbuild import mapops  # noqa: E402

SL = r"D:\UO\golems\Iron\ShatteredLegacy"

# name, x1, y1, x2, y2, source of the rectangle
PLACES = [
    ("New Haven plaza and tutorial marks", 3480, 2550, 3530, 2600, "TutorialCorePlacement.cs:19-29"),
    ("New Haven town (region box)", 3400, 2500, 3640, 2720, "pinned regions.json New Haven, approx."),
    ("Tutorial death/healer spot", 3395, 2605, 3410, 2622, "TutorialCorePlacement.cs:21-24"),
    ("Old Haven ruins", 3600, 2450, 3700, 2700, "ClusterFOldHavenSeeder.cs, approx."),
    ("Rootdeep Burrows (void block)", 5150, 1100, 5260, 1200, "cc-P167/P188 notes, approx."),
    ("Fold void C", 6160, 1832, 6639, 2279, "FoldRegions.cs FoldMirrorRegion"),
    ("Fold isle drawn area", 6170, 1913, 6441, 2057, "cc-P481 design 3.x"),
    ("Blackthorn dungeon (EA 2017)", 6151, 2301, 6563, 2839, "BlackthornDungeon/Region.cs:55"),
    ("Despise revamped (EA)", 5380, 500, 5620, 780, "DespiseRevamped/Setup.cs:74-120"),
    ("Shame revamped (EA)", 5380, 0, 5900, 260, "approx."),
    ("Wrong revamped (EA)", 5630, 500, 5900, 680, "approx."),
    ("Exodus dungeon", 1900, 3640, 2100, 3780, "approx., ExodusSummoningAltar.cs"),
    ("New Magincia", 3640, 2040, 3780, 2280, "approx."),
    ("Britain", 1400, 1500, 1700, 1800, "approx."),
    ("Britain moongate", 1330, 1990, 1342, 2004, "PublicMoongate.cs"),
    ("Moonglow moongate", 4460, 1276, 4474, 1290, "PublicMoongate.cs"),
    ("Yew moongate", 764, 745, 778, 759, "PublicMoongate.cs"),
    ("Minoc moongate", 2694, 685, 2708, 699, "PublicMoongate.cs"),
    ("Nujel'm and the sea east of it", 3500, 1000, 5000, 2100, "change map"),
]


def stats(land_s, z_s, land_o, z_o, ks, ko, kind_s, kind_o, x1, y1, x2, y2):
    s = (slice(x1, x2 + 1), slice(y1, y2 + 1))
    land = int(((land_s[s] != land_o[s]) | (z_s[s] != z_o[s])).sum())

    def in_rect(keys):
        blk, cell = keys >> 30, (keys >> 24) & 63
        x = (blk // sosdiff.BH) * 8 + cell // 8
        y = (blk % sosdiff.BH) * 8 + cell % 8
        return keys[(x >= x1) & (x <= x2) & (y >= y1) & (y <= y2)]

    a, b = in_rect(ks), in_rect(ko)
    return dict(tiles=(x2 - x1 + 1) * (y2 - y1 + 1), landChanged=land, staticsStock=len(a), staticsSos=len(b),
                onlyStock=len(np.setdiff1d(a, b, assume_unique=True)), onlySos=len(np.setdiff1d(b, a, assume_unique=True)),
                dryStock=int((kind_s[s] == 0).sum()), drySos=int((kind_o[s] == 0).sum()))


def main():
    ls, zs = islands.load_land("trammel")
    lo, zo = islands.load_land("sos")
    _, kind_s, _, _, _, _ = islands.build("trammel")
    _, kind_o, _, _, _, _ = islands.build("sos")
    ks, ko = sosdiff.static_keys("trammel"), sosdiff.static_keys("sos")
    rows = []
    for name, x1, y1, x2, y2, src in PLACES:
        d = stats(ls, zs, lo, zo, ks, ko, kind_s, kind_o, x1, y1, x2, y2)
        rows.append(dict(name=name, rect="%d,%d-%d,%d" % (x1, y1, x2, y2), source=src, **d))
        print(name, d)
    with open(os.path.join(sosdiff.OUT, "places.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    # The mapops patch: its blocks, and which of them SoS also changed.
    text = open(os.path.join(SL, "player-package", "vendor", "shattered-legacy-map", "trammel.mapops"), encoding="utf-8").read()
    facet, fps, land_ops, adds, rems = mapops.parse(text)
    blocks = set(fps) | {(x // 8) * sosdiff.BH + (y // 8) for x, y, _, _ in land_ops} | set(adds) | set(rems)
    b = sosdiff.load()
    ch = sosdiff.changed_mask(b)
    out = []
    for blk in sorted(blocks):
        bx, by = blk // sosdiff.BH, blk % sosdiff.BH
        out.append((blk, bx * 8, by * 8, bool(ch[bx, by])))
    with open(os.path.join(sosdiff.OUT, "mapops-blocks.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["block", "x", "y", "sosChangedThisBlock"])
        w.writerows(out)
    xs = [o[1] for o in out]
    ys = [o[2] for o in out]
    print("mapops facet", facet, "blocks", len(out), "land ops", len(land_ops), "adds", sum(len(v) for v in adds.values()),
          "removes", sum(len(v) for v in rems.values()), "bbox", min(xs), min(ys), max(xs) + 7, max(ys) + 7,
          "blocks SoS also changed", sum(1 for o in out if o[3]))
    # Clusters of patch blocks, for naming.
    clusters = {}
    for blk, x, y, c in out:
        key = (x // 128, y // 128)
        clusters.setdefault(key, [0, 0, x, y, x, y])
        cl = clusters[key]
        cl[0] += 1; cl[1] += c
        cl[2], cl[3], cl[4], cl[5] = min(cl[2], x), min(cl[3], y), max(cl[4], x + 7), max(cl[5], y + 7)
    for k, cl in sorted(clusters.items()):
        print("  patch cluster", cl[2:], "blocks", cl[0], "of them changed by SoS", cl[1])


if __name__ == "__main__":
    main()
