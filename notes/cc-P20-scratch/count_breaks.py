import re,glob
for f in sorted(glob.glob("s2-*.md")):
    sec=None; res={}
    for line in open(f,encoding="ascii"):
        if line.startswith("## "):
            sec=line[3:].strip(); res.setdefault(sec,[False,False,False,False,0])
            continue
        if sec and line.startswith("|") and not set(line.strip())<=set("|-: "):
            cells=[c.strip().lower() for c in line.strip().strip("|").split("|")]
            if len(cells)>=8 and cells[0] not in ("use","use (what reads the skill)"):
                r=res[sec]; r[4]+=1
                for i,col in enumerate(cells[3:7]):
                    if "break" in col: r[i]=True
    print("==",f)
    for s,r in res.items():
        if r[4]: print(f"  {s[:60]:60} rows={r[4]:2} 120={'B' if r[0] else '-'} 300={'B' if r[1] else '-'} 500={'B' if r[2] else '-'} 1000={'B' if r[3] else '-'}")
