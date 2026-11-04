r"""cc-P793: find temperate meadows on the SoS land (Trammel): 24x24 blocks of grass land with almost no statics, flat,
outside every named region of server/data/regions-trammel.json and every SosFenceRegion rectangle. Read only.
    python -P meadows.py
"""
import json, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P678-tools"))
import soswalk
f = soswalk.files()
ids, zs = np.asarray(f["ids"]), np.asarray(f["zs"])
print("land shape", ids.shape)
land = f["land"]
sample = land[3] if not isinstance(land, np.ndarray) else land[3]
print("land[3]", sample)
W, H = 7168, 4096
if ids.shape == (H, W):
    ids = ids.T; zs = zs.T
GRASS = {i for i, t in enumerate(land) if i < 0x4000 and t[2] == "grass"}
print("grass ids", len(GRASS))
isgrass = np.isin(ids, sorted(GRASS))
sc = np.zeros((W, H), dtype=np.int32)
np.add.at(sc, (np.asarray(f["sx"]).astype(int), np.asarray(f["sy"]).astype(int)), 1)
SHARD = os.path.join(os.path.dirname(os.path.dirname(NOTES)), "ShatteredLegacy")
regions = json.load(open(os.path.join(SHARD, "server/data/regions-trammel.json"), encoding="utf-8"))
rects = []
def walk(o):
    if isinstance(o, dict):
        if all(k in o for k in ("x1", "y1", "x2", "y2")):
            rects.append((o["x1"], o["y1"], o["x2"], o["y2"]))
        for k, v in o.items():
            if k == "area" and isinstance(v, list):
                for a in v:
                    if isinstance(a, dict) and "x1" in a: pass
            walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(regions)
print("region rects", len(rects), "sample", json.dumps(regions[0])[:300] if isinstance(regions, list) else list(regions)[:5])
fence = open(os.path.join(SHARD, "server/customizations/Regions/SosFenceRegions.cs"), encoding="utf-8").read()
fr = [tuple(map(int, m)) for m in re.findall(r"\((\d+), (\d+), (\d+), (\d+)\)", fence)]
print("fence rects", len(fr))
blocked = np.zeros((W, H), bool)
for x1, y1, x2, y2 in rects + fr:
    blocked[max(0,x1-10):x2+11, max(0,y1-10):y2+11] = True
S = 24
out = []
for x in range(0, 4096 - S, 6):      # Britannia proper
    for y in range(0, 4096 - S, 6):
        g = isgrass[x:x+S, y:y+S]
        if g.mean() < .97 or blocked[x:x+S, y:y+S].any():
            continue
        z = zs[x:x+S, y:y+S]
        s = sc[x:x+S, y:y+S].sum()
        if z.max() - z.min() > 8 or s > 12:
            continue
        out.append((int(s), int(z.max() - z.min()), x + S//2, y + S//2, int(zs[x+S//2, y+S//2])))
out.sort()
print(len(out), "blocks")
seen = []
for o in out:
    if all(abs(o[2]-p[2]) + abs(o[3]-p[3]) > 100 for p in seen):
        seen.append(o)
for o in seen[:40]:
    print(o)
