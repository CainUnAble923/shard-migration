import math
S=[125,140,155,170,185,200,150,225,500]
def scale(i,p): return int(i*p/100) if i>=0 else -int(-i*p/100)
def aosdmg(avgdice_total, Int, sdi, insc=1200, ev=1200):
    d=avgdice_total*100
    ib=(insc+1000*(insc//1000))//200
    d=scale(d,100+ib+Int//10+sdi)
    d=scale(d,30+9*ev//100)
    return d//100
print("Spell.cs intBonus, damageBonus, FlameStrike avg(51) PvP sdi15 / PvM sdi35, EBolt avg(43) PvP")
for s in S:
    print(s, s//10, 11+s//10+15, aosdmg(51,s,15), aosdmg(51,s,35), aosdmg(43,s,15))
print("MindBlast AOS min(int((120+Int)/5),60)")
for s in S: print(s, min(int((120+s)/5),60))
print("Bless/Curse eval120: buff 13% raw; curse 8% (resist120) 20%(resist0)")
for s in S: print(s, int(s*0.13), int(s*0.08), int(s*0.20))
print("Mana regen AOS/ML (ours=pinned w/o armor): Med120 Focus120 MR18")
def regen(Int,med=120,focus=120,mr=18,medit=False):
    mp=(Int+med*3)*(0.025 if med<100 else 0.0275)
    t=focus*0.05+mp+((min(mp,13.0)) if medit else 0)+min(mr,18)
    t=math.floor(t)
    return mp,t,0.1*(2+t)
for s in S:
    a=regen(s);b=regen(s,medit=True);c=regen(s,mr=0,focus=0);d=regen(s,mr=0,focus=0,medit=True)
    print(s, "medPts %.2f tot %d mps %.1f | medit tot %d mps %.1f | naked(no MR/focus) %.1f / medit %.1f"%(a[0],a[1],a[2],b[1],b[2],c[2],d[2]))
print("Meditation active chance at Mana=0, skill 120 and 200; ManaMax=Int(+0 bonus)")
for s in S:
    for sk in (120,200):
        ch=(50+(sk-(s-0))*2)/100
        need=max(0,s-(sk+25))
        print(s, sk, "chance@empty %.2f"%max(0,ch), "min mana for >0 chance", need, end=" | ")
    print()
print("Peacemaking/BaseInstrument difficulty vs player, all stats=s, BonusHits25, skills 720")
for s in S:
    hm=s//2+50+25
    v=hm*1.6+s+s+720
    if v>700: v=700+int((v-700)*3/11)
    print(s, v/10)
print("Time to refill ManaMax=Int from 0 (s) at regen above, not meditating")
for s in S:
    print(s, round(s/regen(s)[2],1))
