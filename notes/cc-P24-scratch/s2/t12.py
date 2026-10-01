from render import *
import collections, numpy as np
land_n, items = load_tiledata_names(D+'/tiledata.mul')
st=area_statics(idx,mul,3380,2420,3800,2780)
RU=[s for s in st if items[s[2]][1] in ('ruined wall','ruined bed','ruined bookcase','stone ruins','debris','broken barrel','broken chair','broken furniture','broken armoire','broken dresser','damaged books','broken clock')]
pts=[(x,y) for x,y,t,z,h in RU if items[t][1]=='ruined wall']
# cluster by 4-tile linking
pts=list(set(pts)); S=set(pts); seen=set(); cl=[]
for p in pts:
    if p in seen: continue
    q=[p]; seen.add(p); comp=[]
    while q:
        a=q.pop(); comp.append(a)
        for dx in range(-4,5):
            for dy in range(-4,5):
                b=(a[0]+dx,a[1]+dy)
                if b in S and b not in seen: seen.add(b); q.append(b)
    cl.append(comp)
cl.sort(key=lambda c:-len(c))
door_kw=('door',)
for i,c in enumerate(cl):
    xs=[p[0] for p in c]; ys=[p[1] for p in c]
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    inside=[s for s in st if x0<=s[0]<=x1 and y0<=s[1]<=y1]
    names=collections.Counter(items[s[2]][1] for s in inside)
    roof=sum(v for k,v in names.items() if 'roof' in k or 'shingle' in k)
    doors=sum(v for k,v in names.items() if 'door' in k)
    print(i,'ruined-wall tiles',len(c),'bbox',x0,y0,x1,y1,'size',x1-x0+1,'x',y1-y0+1,'roof',roof,'doors',doors, names.most_common(8))
import json; json.dump([[min(p[0] for p in c),min(p[1] for p in c),max(p[0] for p in c),max(p[1] for p in c),len(c)] for c in cl],open('ruins.json','w'))
