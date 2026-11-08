import json,sys,re,os,struct
sys.path.insert(0,os.path.dirname(sys.argv[0]))
CD="D:/UO/tool-trials/client-data-copy"
td=open(CD+"/tiledata.mul","rb").read()
LAND=512*(4+32*30);G=4+32*41
def nm(i):
    g,r=divmod(i,32);o=LAND+g*G+4+r*41
    return td[o+21:o+41].split(b"\0")[0].decode("latin-1")
d=json.load(open(sys.argv[1]))
CODE="D:/UO/third-party/code"
PAT=re.compile(r"(?:AddComplexComponent\s*\(\s*\(?\s*BaseAddon\s*\)?\s*this\s*,|AddComplexComponent\s*\(\s*this\s*,|new\s+AddonComponent\s*\(|new\s+Static\s*\(|base\s*\(|ItemID\s*=)\s*(0x[0-9A-Fa-f]+|\d+)")
TABLE=re.compile(r"\{\s*(\d+)\s*,\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*\}")
for f,r in d.items():
    ids={}
    for c in r["cs"]:
        t=open(os.path.join(CODE,f,c),encoding="utf-8",errors="replace").read()
        for v in PAT.findall(t)+TABLE.findall(t):
            i=int(v,16) if v.lower().startswith("0x") else int(v)
            if 0<i<0x10000: ids[i]=ids.get(i,0)+1
    hi=sorted(i for i in ids if i>=0x4000)
    print(f, "| hi:", "; ".join(f"{hex(i)} {nm(i)}" for i in hi[:14]))
