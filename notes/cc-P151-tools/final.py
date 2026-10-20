import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import uomap, survey
GATES = {1: [("Moonglow",4467,1283),("Britain",1336,1997),("Jhelom",1499,3771),("Yew",771,752),("Minoc",2701,692),("Trinsic",1828,2948),("Skara Brae",643,2067),("Magincia",3563,2139),("New Haven",3450,2677)],
         0: [("Moonglow",4467,1283),("Britain",1336,1997),("Jhelom",1499,3771),("Yew",771,752),("Minoc",2701,692),("Trinsic",1828,2948),("Skara Brae",643,2067),("Magincia",3563,2139),("Buccaneer's Den",2711,2234)],
         3: [("Luna",1015,527),("Umbra",1997,1386)], 4: [("Isamu-Jima",1169,998),("Makoto-Jima",802,1204),("Homare-Jima",270,628)], 5: [("Royal City",850,3525)]}
def banks(f):
    return [(s[0],s[1]) for s in survey.SPAWNERS[survey.MAPNAME[f]] if "Banker" in s[3]]
def d(a,b): return max(abs(a[0]-b[0]),abs(a[1]-b[1]))
PICKS = [
 ("League HQ",1,(1320,1586,1366,1665)),("League HQ alt courtyard",1,(1362,1584,1381,1607)),
 ("Warriors",1,(1352,3696,1376,3720)),("Arcane",1,(4278,915,4336,1017)),("Healers",1,(623,816,647,856)),
 ("Rangers",1,(608,2112,632,2144)),("Miners",1,(2416,520,2440,536)),("Smiths",1,(3018,3372,3045,3399)),
 ("Tinkers",1,(2880,736,2904,752)),("Thieves",1,(2655,2072,2681,2096)),("Dojo",4,(744,1170,765,1191)),
 ("Keepers",3,(1983,1351,1999,1365)),("Foresters",1,(544,808,567,831)),("Tailors",1,(3760,1184,3783,1207)),
 ("Maritime (Fel)",0,(3600,2496,3616,2512)),("Maritime (Tram Old Haven)",1,(3600,2496,3616,2512)),("Merchants",1,(3704,2170,3725,2191)),("Bards",1,(1440,1576,1460,1600)),
 ("Artificers",5,(790,3424,803,3441)),("Alembic",1,(5638,3240,5651,3253)),("Custodians",1,(1448,1702,1473,1716))]
f0, f1 = uomap.Facet(0), uomap.Facet(1)
for name, f, r in PICKS:
    c = ((r[0]+r[2])//2, (r[1]+r[3])//2)
    g = min(GATES[f], key=lambda g: d(c, g[1:]))
    b = min(banks(f), key=lambda b: d(c, b))
    fel = ""
    if f in (0, 1):
        other = f0 if f == 1 else f1
        me = f1 if f == 1 else f0
        diff = sum(1 for x in range(r[0], r[2]+1) for y in range(r[1], r[3]+1)
                   if sorted(me.statics(x, y)) != sorted(other.statics(x, y)) or me.land(x, y) != other.land(x, y))
        osp = [s[:4] for s in survey.SPAWNERS["Felucca" if f == 1 else "Trammel"] if r[0]-3 <= s[0] <= r[2]+3 and r[1]-3 <= s[1] <= r[3]+3]
        fel = f"other-facet tiles differing {diff}; other-facet spawners {osp}"
    print(f"{name}: centre {c}; gate {g[0]} {g[1]},{g[2]} d={d(c,g[1:])}; bank {b} d={d(c,b)}; {fel}")
