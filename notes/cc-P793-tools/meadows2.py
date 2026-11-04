r"""cc-P793: second pass. The mainland reachable on foot from meadow (1986, 2244), then 16x16 open grass blocks on it,
outside every region and fence by 10 tiles. Read only. python -P meadows2.py"""
import collections, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P678-tools"))
import soswalk
SHARD = os.path.join(os.path.dirname(os.path.dirname(NOTES)), "ShatteredLegacy")
R = (500, 1000, 2500, 3000)
w = soswalk.Walk(R)
f = soswalk.files()
land = f["land"]; ids = f["ids"]
regs = json.load(open(os.path.join(SHARD, "server/data/regions-trammel.json"), encoding="utf-8"))
rects = [(a["x1"], a["y1"], a["x2"], a["y2"]) for r in regs for a in r["Area"]]
fence = open(os.path.join(SHARD, "server/customizations/Regions/SosFenceRegions.cs"), encoding="utf-8").read()
rects += [tuple(map(int, m)) for m in re.findall(r"\((\d+), (\d+), (\d+), (\d+)\)", fence)]
q = collections.deque([(1986, 2244)]); seen = {(1986, 2244)}
while q:
    p = q.popleft()
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        t = (p[0]+dx, p[1]+dy)
        if t in seen or w.stand.get(t) is None or abs(w.stand[t]-w.stand[p]) > 2: continue
        seen.add(t); q.append(t)
print("mainland tiles", len(seen))
S = 16; out = []
for x in range(R[0], R[2]-S, 4):
    for y in range(R[1], R[3]-S, 4):
        tiles = [(i, j) for i in range(x, x+S) for j in range(y, y+S)]
        if not all(t in seen for t in tiles): continue
        if any(a-10 <= x+S and x <= c+10 and b-10 <= y+S and y <= d+10 for a, b, c, d in rects): continue
        g = sum(1 for i, j in tiles if land[int(ids[i, j])][2] == "grass")
        if g < .95 * len(tiles): continue
        st = sum(len(w.sts.get(t, ())) for t in tiles)
        out.append((st, x+S//2, y+S//2, w.stand[(x+S//2, y+S//2)]))
out.sort(); print(len(out), "blocks"); kept = []
for o in out:
    if all(abs(o[1]-p[1])+abs(o[2]-p[2]) > 120 for p in kept): kept.append(o)
for o in kept[:15]: print(o)
