import xml.etree.ElementTree as ET, json, numpy as np
from numpy.lib.stride_tricks import sliding_window_view
E=np.load('empty_both.npy'); R=np.load('regmask.npy').copy(); Pm=np.load('ptmask.npy')
root=ET.parse('D:/UO/ServUO-pub57/Data/Regions.xml').getroot()
n=0
for facet in root.findall('Facet'):
    if facet.get('name')!='Trammel': continue
    for reg in facet.iter('region'):
        for rect in reg.findall('rect'):
            g=rect.get
            if g('x') is None or g('width') is None: continue
            x,y=int(g('x')),int(g('y')); R[y:y+int(g('height')), x:x+int(g('width'))]=True; n+=1
print('servuo trammel rects',n)
R[3041-32:3619+32, 6144:]=True  # 114/117 diff zone plus margin
free=E&~R&~Pm
H,W=free.shape
B=free.reshape(H//8,8,W//8,8).all(axis=(1,3))
Bp=np.pad(B,2,constant_values=False)
Be=sliding_window_view(Bp,(5,5)).all(axis=(2,3))   # 16-tile buffer
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

out=[]
for lo,hi in ((5120,6144),(6144,7168)):
    M=Be.copy(); M[:, :lo//8]=False; M[:, hi//8:]=False
    for i in range(8):
        (sc,area),(bx,by,bw,bh)=maxrect(M)
        if sc*8<80: break
        r=[int(bx*8),int(by*8),int(bx*8+bw*8-1),int(by*8+bh*8-1)]
        out.append(r); print(lo,'cand',r,'size',bw*8,'x',bh*8)
        M[max(0,by-2):by+bh+2, max(0,bx-2):bx+bw+2]=False
json.dump(out,open('cands_strict.json','w'))
