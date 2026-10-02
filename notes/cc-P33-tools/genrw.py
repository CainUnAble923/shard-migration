import re, os, json
exec(open("gen.py").read().split("cd=open")[0])  # builds cands
src=open("D:/UO/ServUO-pub57/Scripts/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs").read().splitlines()
renames={"ScrollOfAlacrity":"ScrollofAlacrity"}
out=[];miss=[]
n=0
for ln,l in enumerate(src,1):
    m=re.search(r'Rewards\.Add\(new CollectionItem\(typeof\((\w+)\),\s*(0x[0-9A-Fa-f]+),\s*(\d+),\s*(0x[0-9A-Fa-f]+|\d+),\s*(\d+)\)\)',l)
    if not m: continue
    n+=1
    t,g,cl,h,pr=m.groups()
    nm=renames.get(t,t)
    c=[x for x in cands.get(nm,[]) if x[0]]
    if c:
        pick=[x for x in c if x[0]=="Server.Items"] or c
        note=f" (ServUO {t}; pinned spells it {nm})" if nm!=t else ""
        out.append(f"        new(typeof(global::{pick[0][0]}.{nm}), {g}, {cl}, {h}, {pr}), // :{ln}{note}")
    else:
        out.append(f"        // MISSING :{ln} {t} {g} {cl} {h} {pr}")
        miss.append((ln,t,int(pr)))
print(n,len(miss))
open("rewards.cs.txt","w").write("\n".join(out))
json.dump(miss,open("missing-rewards.json","w"))
