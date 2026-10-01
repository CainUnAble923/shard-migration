import numpy as np, json
E=np.load('empty_both.npy'); R=np.load('regmask.npy'); Pm=np.load('ptmask.npy')
free=E&~R&~Pm
H,W=free.shape
# block-level: block free if all 64 tiles free
B=free.reshape(H//8,8,W//8,8).all(axis=(1,3))
# margin: require 1-block (8 tile) buffer of free blocks around -> erode
from numpy.lib.stride_tricks import sliding_window_view
Bp=np.pad(B,1,constant_values=False)
Be=sliding_window_view(Bp,(3,3)).all(axis=(2,3))
def maxrect(M):
    best=(0,None); h=np.zeros(M.shape[1],int)
    for y in range(M.shape[0]):
        h=np.where(M[y],h+1,0)
        st=[]
        for x in range(M.shape[1]+1):
            cur=h[x] if x<M.shape[1] else 0
            start=x
            while st and st[-1][1]>=cur:
                s,hh=st.pop()
                # prefer squarish: score = min(w,h)^2 bonus
                w=x-s; area=w*hh; sc=min(w,hh)
                if (sc,area)>best[0] if isinstance(best[0],tuple) else True:
                    best=((sc,area),(s,y-hh+1,w,hh))
                start=s
            st.append((start,cur))
    return best
import sys
lo,hi=int(sys.argv[1]),int(sys.argv[2])
M=Be.copy(); M[:, :lo//8]=False; M[:, hi//8:]=False
out=[]
for i in range(12):
    (sc,area),(bx,by,bw,bh)=maxrect(M)
    if sc*8<64: break
    out.append([int(bx*8),int(by*8),int(bw*8),int(bh*8)])
    print('cand', i, 'x',bx*8,'-',bx*8+bw*8-1,'y',by*8,'-',by*8+bh*8-1,'size',bw*8,'x',bh*8)
    M[max(0,by-2):by+bh+2, max(0,bx-2):bx+bw+2]=False
json.dump(out,open('cands_%d_%d.json'%(lo,hi),'w'))
