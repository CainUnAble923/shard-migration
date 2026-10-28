r"""cc-P678: open, flat, uncovered ground in SoS Haven for the tutorial's training yard and trades yard.
A candidate is a tile whose 7 x 5 block (x-3..x+3, y-2..y+2) is all reachable on foot from the start (soswalk), within
one Z of the centre, uncovered (no roof: buildings.find), not a stock tile, an NPC home or a HavenSpots spot, and inside
the town box. Prints the best few by distance from the start, then the farmhouse porch: the reachable uncovered tiles
next to the vet farmhouse (3704-3712, 2584-2592).
    python -P yards.py
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import buildings  # noqa: E402
import placer  # noqa: E402
import soswalk  # noqa: E402

START = (3634, 2586)
BOX = (3568, 2460, 3761, 2712)


def main():
    w = soswalk.Walk(BOX)
    reach = w.flood(START)
    cov, _ = buildings.find(*BOX)
    keep = placer.stock_tiles() | {(int(r["x"]), int(r["y"])) for r in csv.DictReader(open(os.path.join(HERE, "out", "homes.csv")))}
    roads = set()   # a road is fine for a yard's edge; the centre row stays off stock tiles only
    good = []
    for (x, y) in reach:
        z = w.stand[(x, y)]
        block = [(x + dx, y + dy) for dx in range(-3, 4) for dy in range(-2, 3)]
        if all(p in reach and abs(w.stand[p] - z) <= 1 and p not in cov and p not in keep for p in block):
            d = abs(x - START[0]) + abs(y - START[1])
            good.append((d, x, y, z))
    good.sort()
    print("yard candidates (distance from the start, x, y, z):")
    for g in good[:40]:
        print(*g)
    print("farmhouse porch candidates:")
    for x in range(3702, 3715):
        for y in range(2582, 2595):
            p = (x, y)
            if p in reach and p not in cov and any(n in cov for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                print(x, y, w.stand[p])
    del roads


if __name__ == "__main__":
    main()
