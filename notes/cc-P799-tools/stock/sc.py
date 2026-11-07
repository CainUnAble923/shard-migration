import sys,re
from collections import defaultdict,Counter
import hallbase as H
F=H.Facet(1)
x0,y0,x1,y1=map(int,sys.argv[1:5])
K=re.compile(sys.argv[5] if len(sys.argv)>5 else '.',re.I)
h=defaultdict(list)
for bx in range(x0>>3,(x1>>3)+1):
  for by in range(y0>>3,(y1>>3)+1):
    for sid,sx,sy,sz,hue in F.block(bx,by):
      x,y=bx*8+sx,by*8+sy
      if x0<=x<=x1 and y0<=y<=y1:
        n=H.iname(sid)
        if K.search(n): h[n+' 0x%04X'%sid].append((x,y,sz))
for n in sorted(h):
  p=h[n]; xs=[a[0] for a in p]; ys=[a[1] for a in p]
  print('%-30s %4d x %d-%d y %d-%d %s'%(n,len(p),min(xs),max(xs),min(ys),max(ys),' '.join('%d,%d,%d'%a for a in p[:6])))
