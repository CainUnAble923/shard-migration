import json,re
t=json.load(open("table.json"))
cd=open("D:/UO/ServUO-pub57/Scripts/Services/PointsSystems/CleanUpBritanniaData.cs").read().splitlines()
# section comments from ServUO, keyed by line
out=[]; missing=[]
lastsec=None
for ln,typ,val,fq,src in t:
    # find nearest preceding // comment line within the InitializeEntries body
    sec=None
    for j in range(ln-2,185,-1):
        s=cd[j].strip()
        if s.startswith("//") and "Entries[" not in s:
            sec=s[2:].strip(); break
        if s.startswith("public void InitializeEntries"): break
    if sec!=lastsec:
        out.append("")
        out.append(f"        // {sec}" if sec else "        // (no heading)")
        lastsec=sec
    v=val if "." in val else val+".0"
    if fq:
        out.append(f"        Add(typeof(global::{fq}), {v}); // :{ln}")
    else:
        out.append(f"        // MISSING :{ln} {typ} = {v}")
        missing.append(f"{typ} {v} :{ln}")
open("entries.cs.txt","w").write("\n".join(out))
open("missing-entries.txt","w").write("\n".join(missing))
print(len(out),len(missing))
