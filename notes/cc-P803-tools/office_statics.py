import sys
sys.path.insert(0, r"D:/UO/golems/Iron/shard-migration/scripts/mapbuild")
import uofiles
import os
C = os.environ.get("MAPFOLDER", r"D:/UO/tool-trials/client-data-copy")
x1,y1,x2,y2 = map(int, sys.argv[1:5])
skip = set(a.lower() for a in sys.argv[5:])
land, items = uofiles.read_tiledata(r"D:/UO/tool-trials/client-data-copy")
from collections import Counter
cnt = Counter()
for (x,y,z,t) in sorted(uofiles.statics_in(C, 1, x1, y1, x2, y2), key=lambda s:(s[1],s[0],s[2])):
    n = items[t]["name"]
    if any(k in n.lower() for k in skip):
        cnt[n]+=1; continue
    print(f"{x},{y},{z} 0x{t:04X} h{items[t]['height']} {n}")
print("skipped:", dict(cnt))
