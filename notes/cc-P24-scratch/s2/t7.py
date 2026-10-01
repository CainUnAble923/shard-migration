from render import *
import numpy as np
E=np.load('empty_both.npy'); R=np.load('regmask.npy')
C={'A':(5128,1120,5255,1271),'B':(5520,1416,5623,1527),'C':(6152,1816,6647,2303),'D':(6488,1544,6807,1799),'E':(6664,768,7159,1151)}
for k,(a,b,c,d) in C.items():
    sub=E[b:d+1,a:c+1]; print(k, 'size',c-a+1,'x',d-b+1,'all empty both versions', sub.all(), 'region tiles', R[b:d+1,a:c+1].sum())
    pad=40 if c-a<200 else 120
    sc=3 if c-a<200 else 1
    render(a-pad,b-pad,c+pad+1,d+pad+1,'cand_%s.png'%k,scale=sc,boxes=[(a,b,c,d,(0,255,0),'cand '+k)],grid=50 if sc>1 else 100)
