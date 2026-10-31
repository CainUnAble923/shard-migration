import sys
sys.path.insert(0, r"D:/UO/golems/Iron/shard-migration/scripts")
from mapbuild import uofiles
import numpy as np
from PIL import Image

STOCK = r"D:/UO/UltimaOnlineVanilla"
SOS = r"D:/UO/golems/Iron/shard-migration/notes/cc-P675-tools/sos-base"
x1, y1, x2, y2 = 6100, 2260, 6620, 2900
ids, zs = uofiles.load_land(STOCK, 1)
occ = ids[x1:x2 + 1, y1:y2 + 1] != uofiles.VOID
for s in uofiles.statics_in(STOCK, 1, x1, y1, x2, y2):
    occ[s[0] - x1, s[1] - y1] = True
img = np.zeros(occ.T.shape + (3,), np.uint8)
img[occ.T] = (220, 220, 220)
# region box outline
for x in range(6151, 6564):
    img[2301 - y1, x - x1] = img[2839 - y1, x - x1] = (255, 0, 0)
for y in range(2301, 2840):
    img[y - y1, 6151 - x1] = img[y - y1, 6563 - x1] = (255, 0, 0)
Image.fromarray(img).save("occ-stock.png")

from collections import deque
W,H=occ.shape
seen=np.zeros_like(occ,dtype=np.int32);n=0
R=3
for sx in range(W):
  for sy in range(H):
    if occ[sx,sy] and not seen[sx,sy]:
      n+=1;q=deque([(sx,sy)]);seen[sx,sy]=n;cnt=0;mnx=mxx=sx;mny=mxy=sy
      while q:
        x,y=q.popleft();cnt+=1;mnx=min(mnx,x);mxx=max(mxx,x);mny=min(mny,y);mxy=max(mxy,y)
        for dx in range(-R,R+1):
          for dy in range(-R,R+1):
            a,b=x+dx,y+dy
            if 0<=a<W and 0<=b<H and occ[a,b] and not seen[a,b]:
              seen[a,b]=n;q.append((a,b))
      if cnt>=50: print(n,cnt,"x",x1+mnx,x1+mxx,"y",y1+mny,y1+mxy)
