import re, os, json
SV="D:/UO/ServUO-pub57/Scripts"
roots=["D:/UO/ModernUO-pinned/Projects/UOContent","D:/ShatteredLegacy/server/customizations"]
cands={}
for root in roots:
  for dp,dn,fn in os.walk(root):
    for f in fn:
      if not f.endswith(".cs"): continue
      p=os.path.join(dp,f).replace("\\","/")
      s=open(p,encoding="utf-8",errors="ignore").read()
      code=re.sub(r'//[^\n]*','',s)
      code=re.sub(r'/\*.*?\*/','',code,flags=re.S)
      nss=[(m.start(),m.group(1)) for m in re.finditer(r'\bnamespace\s+([\w.]+)',code)]
      for m in re.finditer(r'^([ \t]*)(?:public|internal)?\s*(?:sealed\s+|abstract\s+|static\s+|partial\s+)*class\s+(\w+)',code,re.M):
        ns=None
        for pos,n in nss:
          if pos<m.start(): ns=n
        cands.setdefault(m.group(2),[]).append((ns,p,len(m.group(1).expandtabs(4))))
cd=open(SV+"/Services/PointsSystems/CleanUpBritanniaData.cs").read()
lines=[(i+1,l) for i,l in enumerate(cd.splitlines()) if re.search(r'Entries\[typeof',l) and not l.strip().startswith("//")]
renames={"MetallicClothDyeTub":"MetallicClothDyetub"}
out=[];missing=[];amb=[]
for ln,l in lines:
  t,v=re.search(r'Entries\[typeof\((\w+)\)\]\s*=\s*([\d.]+);',l).groups()
  n=renames.get(t,t)
  c=[x for x in cands.get(n,[]) if x[0]]
  if not c: missing.append(t); out.append((ln,t,v,None,None)); continue
  nsset=sorted(set(x[0] for x in c))
  if len(nsset)>1: amb.append((t,nsset))
  pick=[x for x in c if x[0]=="Server.Items"] or c
  if pick[0][2]>4: print("nested?",t,pick[0])
  out.append((ln,t,v,pick[0][0]+"."+n,pick[0][1].split("/Projects/")[-1].split("/server/")[-1]))
print(len(out),len(missing)); print("amb",amb)
json.dump(out,open("table.json","w"),indent=0)
