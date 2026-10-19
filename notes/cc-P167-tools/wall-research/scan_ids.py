# scan a facet's statics for given item ids; print clusters (8x8 blocks) with counts
import sys, struct, collections
import numpy as np
sys.path.insert(0, r'D:\UO\shard-migration\notes\cc-P36-tools')
import uodata
folder = uodata.NEW
fi = int(sys.argv[1])
ids = [int(a, 16) for a in sys.argv[2:]]
idx, sta = uodata.load_statics_index(folder, fi)
name, w, h = uodata.FACETS[fi]
bh = h >> 3
arr = np.frombuffer(sta[:len(sta)//7*7], dtype=np.dtype([('id','<u2'),('x','u1'),('y','u1'),('z','i1'),('hue','<i2')]))
blocks = collections.Counter()
for b in range(len(idx)):
    look, ln, _ = idx[b]
    if look < 0 or ln <= 0: continue
    seg = arr[look//7:(look+ln)//7]
    m = np.isin(seg['id'], ids)
    if m.any():
        blocks[b] += int(m.sum())
# merge adjacent blocks into clusters
seen=set(); clusters=[]
for b in sorted(blocks):
    if b in seen: continue
    stack=[b]; comp=[]
    while stack:
        c=stack.pop()
        if c in seen: continue
        seen.add(c); comp.append(c)
        bx,by=divmod(c,bh)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                n=(bx+dx)*bh+(by+dy)
                if n in blocks and n not in seen: stack.append(n)
    xs=[divmod(c,bh)[0]*8 for c in comp]; ys=[divmod(c,bh)[1]*8 for c in comp]
    clusters.append((sum(blocks[c] for c in comp), min(xs), min(ys), max(xs)+7, max(ys)+7, len(comp)))
clusters.sort(reverse=True)
print(name, 'blocks with hits', len(blocks), 'clusters', len(clusters))
for n,x1,y1,x2,y2,nb in clusters[:40]:
    print('%5d pieces  x %4d-%4d  y %4d-%4d  (%d blocks)' % (n,x1,x2,y1,y2,nb))
