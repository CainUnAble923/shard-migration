from catrender import *
import collections
crops={'E1_second_bank':(3602,2597),'E2_blacksmith_block':(3630,2600),'E3_southeast_shore':(3634,2630),'E4_provisioners':(3655,2575)}
for k,(x0,y0) in crops.items():
    crender(x0,y0,x0+40,y0+40,'bldg_%s.png'%k,sc=14)
    st=area_statics(idx,mul,x0,y0,x0+40,y0+40)
    print(k,'statics',len(st), collections.Counter(cat(s[2]) for s in st).most_common())
    near=[p for p in pts if x0<=p[1]<x0+40 and y0<=p[2]<y0+40]
    print('  refs',len(near), collections.Counter(p[0].split(':')[0] for p in near).most_common())
