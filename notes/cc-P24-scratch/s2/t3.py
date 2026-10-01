import numpy as np
L={v:np.load('land_%s.npy'%v) for v in ('117','114')}
O={v:np.load('occ_%s.npy'%v) for v in ('117','114')}
Z={v:np.load('z_%s.npy'%v) for v in ('117','114')}
H,W=L['117'].shape
e117=(L['117']==0x244)&(O['117']==0)
e114=(L['114']==0x244)&(O['114']==0)
both=e117&e114
diffland=(L['117']!=L['114']); diffocc=(O['117']!=O['114'])
print('land diff tiles', diffland.sum(), 'occ diff tiles', diffocc.sum())
ys,xs=np.nonzero(diffland|diffocc)
# bounding summary by 512 chunk
import collections
c=collections.Counter(zip((xs//512)*512,(ys//512)*512))
print(sorted(c.items()))
np.save('empty_both.npy', both)
# largest empty square ending at each cell
def sq(m):
    d=np.zeros(m.shape,np.int32)
    for y in range(m.shape[0]):
        row=m[y]; prev=d[y-1] if y else np.zeros(m.shape[1],np.int32)
        cur=np.zeros(m.shape[1],np.int32)
        for x in np.nonzero(row)[0]:
            cur[x]=1+min(prev[x], cur[x-1] if x else 0, prev[x-1] if x else 0)
        d[y]=cur
    return d
d=sq(both)
np.save('sq.npy',d)
print('max square', d.max())
