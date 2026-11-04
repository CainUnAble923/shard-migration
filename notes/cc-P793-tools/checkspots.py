r"""cc-P793: for each meadow spot, the share of tiles standable in its home range, the land there, the nearest towns by
region rectangle, and a walk over the land to the nearest town's edge. Read only. python -P checkspots.py"""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P678-tools"))
import soswalk
SHARD = os.path.join(os.path.dirname(os.path.dirname(NOTES)), "ShatteredLegacy")
regs = json.load(open(os.path.join(SHARD, "server/data/regions-trammel.json"), encoding="utf-8"))
SPOTS = [("a", 1878, 2076), ("b", 1986, 2244)]
R = (1450, 1500, 2350, 2950)
w = soswalk.Walk(R)
print("surveyed")
for n, x, y in SPOTS:
    tiles = [(i, j) for i in range(x-12, x+13) for j in range(y-12, y+13)]
    ok = sum(1 for t in tiles if w.stand.get(t) is not None)
    print(n, x, y, "stand z", w.stand.get((x, y)), "open", ok, "of", len(tiles))
    q = collections.deque([(x, y)]); dist = {(x, y): 0}
    while q:
        p = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            t = (p[0]+dx, p[1]+dy)
            if t in dist or w.stand.get(t) is None or abs(w.stand[t]-w.stand[p]) > 2: continue
            dist[t] = dist[p]+1; q.append(t)
    print(" reachable tiles", len(dist))
    hits = []
    for r in regs:
        if r.get("$type") not in ("GuardedRegion", "TownRegion"): continue
        for a in r["Area"]:
            cx, cy = (a["x1"]+a["x2"])//2, (a["y1"]+a["y2"])//2
            best = min((dist[t] for t in dist if a["x1"] <= t[0] <= a["x2"] and a["y1"] <= t[1] <= a["y2"]), default=None)
            if best is not None:
                hits.append((best, r["Name"], cx, cy))
    print(" towns by foot", sorted(hits)[:5])
