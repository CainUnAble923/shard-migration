import os,sys
def idx(root):
    r={}
    for dp,dn,fn in os.walk(root):
        for f in fn:
            p=os.path.join(dp,f); rel=os.path.relpath(p,root).replace(os.sep,'/')
            r[rel]=os.path.getsize(p)
    return r
a=idx(sys.argv[1]); b=idx(sys.argv[2])
skip=('Data/','LegionScripts/','Cache/','ExternalImages/','Fonts/','settings','Logs/')
bo={k:v for k,v in b.items() if not k.startswith(skip)}
print('built',len(a),sum(a.values()),'shipped(no user dirs)',len(bo),sum(bo.values()))
only_a=sorted(set(a)-set(bo)); only_b=sorted(set(bo)-set(a))
print('only built',len(only_a),only_a[:15]); print('only shipped',len(only_b),only_b[:30])
both=set(a)&set(bo)
print('same size',sum(a[k]==bo[k] for k in both),'of',len(both))
print(sorted((k,a[k],bo[k]) for k in both if a[k]!=bo[k])[:25])
