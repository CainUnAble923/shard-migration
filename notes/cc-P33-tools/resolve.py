import re, os, sys, json
SV="D:/UO/ServUO-pub57/Scripts"
PIN="D:/UO/ModernUO-pinned/Projects"
OURS="D:/ShatteredLegacy/server/customizations"
def index(root):
    idx={}
    alias={}
    for dp,dn,fn in os.walk(root):
        for f in fn:
            if not f.endswith(".cs"): continue
            p=os.path.join(dp,f)
            try: s=open(p,encoding="utf-8",errors="ignore").read()
            except: continue
            for m in re.finditer(r'\b(?:class|struct|interface|enum|record)\s+(\w+)',s):
                idx.setdefault(m.group(1),p)
            for m in re.finditer(r'TypeAlias\(([^)]*)\)',s):
                for a in re.findall(r'"([^"]+)"',m.group(1)):
                    alias.setdefault(a.split('.')[-1],p)
    return idx,alias
pin,pinal=index(PIN); ours,oural=index(OURS)
def res(t):
    if t in ours: return "ours",ours[t]
    if t in pin: return "pinned",pin[t]
    if t in oural: return "ours-alias",oural[t]
    if t in pinal: return "pinned-alias",pinal[t]
    return "MISSING",""
rw=open(SV+"/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs").read()
rewards=re.findall(r'Rewards\.Add\(new CollectionItem\(typeof\((\w+)\),\s*(0x[0-9A-Fa-f]+),\s*(\d+),\s*(0x[0-9A-Fa-f]+|\d+),\s*(\d+)\)\)',rw)
print("rewards",len(rewards))
out=[]
for i,(t,g,cl,h,price) in enumerate(rewards):
    w,p=res(t); out.append((i+1,t,price,w,p.replace("\\","/")))
json.dump(out,open("rewards.json","w"),indent=0)
for o in out: 
    if o[3]=="MISSING" or "alias" in o[3]: print(o)
print("missing rewards",sum(1 for o in out if o[3]=="MISSING"))
cd=open(SV+"/Services/PointsSystems/CleanUpBritanniaData.cs").read()
ents=re.findall(r'Entries\[typeof\((\w+)\)\]\s*=\s*([\d.]+);',cd)
# exclude commented
lines=[l for l in cd.splitlines() if re.search(r'Entries\[typeof',l) and not l.strip().startswith("//")]
ents=[re.search(r'Entries\[typeof\((\w+)\)\]\s*=\s*([\d.]+);',l).groups() for l in lines]
print("entries",len(ents), "distinct", len(set(e[0] for e in ents)))
eo=[]
for t,v in ents:
    w,p=res(t); eo.append((t,v,w,p.replace("\\","/")))
json.dump(eo,open("entries.json","w"),indent=0)
print("missing entries",sum(1 for e in eo if e[2]=="MISSING"))
from collections import Counter
print(Counter(e[2] for e in eo))
