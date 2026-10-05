import json,re,sys
p=r"D:/UO/ModernUO-pinned/Distribution/Data/regions.json"
txt=open(p,encoding='utf-8-sig').read()
lines=txt.split('\n')
data=json.loads(txt)
# map name lines
namelines={}
for i,l in enumerate(lines,1):
    m=re.search(r'"Name": "([^"]*)"',l)
    if m: namelines.setdefault(m.group(1),[]).append(i)
used={}
keys=set()
for r in data:
    keys|=set(r.keys())
print("ALL KEYS:",sorted(keys))
dung=[r for r in data if r['$type']=='DungeonRegion']
# also children whose parent is dungeon
dnames={(r['Map'],r['Name']) for r in dung}
from collections import Counter
print(Counter(r['Map'] for r in dung))
for r in sorted(dung,key=lambda r:(r['Map'],r['Name'])):
    n=r['Name']; ln=namelines[n][used.get(n,0)] if n in namelines else '?'
    a=r['Area']
    zs=[(x.get('z1'),x.get('z2')) for x in a if 'z1' in x or 'z2' in x]
    print(f"{r['Map']}|{n}|line {ln}|rects={len(a)}|prio={r.get('Priority')}|parent={r.get('Parent')}|minexp={r.get('MinExpansion')}|maxexp={r.get('MaxExpansion')}|entr={r.get('Entrance')}")
    for x in a: print("    ",x)
print("---- children of dungeons (any type)")
for r in data:
    par=r.get('Parent')
    if par:
        pn=par if isinstance(par,str) else par.get('Name')
        if (r['Map'],pn) in dnames or any(pn==d[1] for d in dnames):
            print(f"{r['Map']}|{r['Name']}|type={r['$type']}|parent={par}|rects={len(r['Area'])}|line {namelines.get(r['Name'])}")
            for x in r['Area']: print("    ",x)
