import math
S=[125,140,155,170,185,200]; E=[150,225,500]
ALL=S+E
def row(name,f):
    print(f"{name:40s}"+" ".join(f"{str(f(s)):>8s}" for s in ALL))
print(f"{'formula':40s}"+" ".join(f"{('s'+str(s)) if s in S else ('e'+str(s)):>8s}" for s in ALL))
row("HitsMax AOS Str/2+50+25", lambda s: s//2+50+25)
row("HitsMax no bonus Str/2+50", lambda s: s//2+50)
row("StamMax Dex(+0)", lambda s: s)
row("ManaMax Int(+0, human)", lambda s: s)
row("MaxWeight human 100+3.5Str", lambda s: 100+int(3.5*s))
row("MaxWeight elf/garg 40+3.5Str", lambda s: 40+int(3.5*s))
row("pinned backpack cap (ML)", lambda s: min(550, 100+int(3.5*s)))
# mana regen AOS: medPoints=(Int+Med*3)*0.0275 (Med 120); focus 120*0.05=6; RegenMana capped 18
def mana(s,med=120.0,focus=120.0,mr=18,meditating=False):
    mp=(s+med*3)*(0.025 if med<100 else 0.0275)
    tot=focus*0.05+mp+((13.0 if mp>13 else mp) if meditating else 0)+mr
    tot=math.floor(tot)
    rate=1.0/(0.1*(2+tot))
    return f"{1/rate:.1f}/s"
row("Mana regen/s (Med120,Foc120,MR18)", lambda s: mana(s))
row("Mana regen/s meditating", lambda s: mana(s,meditating=True))
row("Mana regen/s MR0 not med", lambda s: mana(s,mr=0))
# fill time empty->full not meditating, MR18
def fill(s,meditating=False):
    mp=(s+360)*0.0275; tot=math.floor(6+mp+((13 if mp>13 else mp) if meditating else 0)+18)
    return f"{s/(0.1*(2+tot)):.0f}s"
row("Mana empty->full secs (MR18)", lambda s: fill(s))
# meditation entry chance at empty mana, skill 120
row("Meditate chance, mana 0, med120", lambda s: f"{max(0,min(1,(50+(120-s)*2)/100)):.2f}")
row("Meditate chance, mana half", lambda s: f"{max(0,min(1,(50+(120-s/2)*2)/100)):.2f}")
# poison lethal AOS: 1+Hits*0.35 clamp 20..50 at full hits
row("Lethal poison tick @full HP", lambda s: max(20,min(50,1+int((s//2+75)*0.35))))
row("Lethal tick as % of HitsMax", lambda s: f"{max(20,min(50,1+int((s//2+75)*0.35)))/(s//2+75)*100:.0f}%")
row("Deadly poison tick @full HP", lambda s: max(16,min(30,1+int((s//2+75)*0.30))))
# DeathExplosion HitsMax/5
row("DeathExplosion dmg HitsMax/5", lambda s: (s//2+75)//5)
row("PlagueBeast gain ceil(.75*HitsMax)", lambda s: math.ceil((s//2+75)*0.75))
row("MeerEternal dmg 0.75*Hits(1 tgt)", lambda s: int((s//2+75)*0.75))
row("Meraktus/Rikktor clamp(.6*Hits,10,75)", lambda s: max(10,min(75,int((s//2+75)*0.6))))
# fatigue on damage std: dmg*Stam/Hits -5 with dmg 40, full pools, Str=Dex=s
row("FatigueOnDamage dmg40 Str=Dex=s", lambda s: max(0,int(40*(100.0/(s//2+75))*(s/100)-5)))
row("  as % of StamMax", lambda s: f"{max(0,int(40*(100.0/(s//2+75))*(s/100)-5))/s*100:.0f}%")
# running: 1 stam per 17 steps (steps>16) ; tiles of running from full
row("Run steps from full stam (unmounted)", lambda s: s*17)
# overweight stam loss per step: 5 + over/25
# anatomy plateau
row("Anatomy strMod min(s/10,10)", lambda s: min(10,s//10))
# 0x11 packet fields
row("short(Str) ok?", lambda s: s<=32767)
# Regen hits/stam (live = pinned): no stat input; refill time grows with pool
hp_rate=1/(10.0/(1+18))   # HPR capped 18 incl human +2
st_rate=0.1*(2+12+24)     # Focus 120 -> 12, RegenStam cap 24
row("HP refill 0->max secs (HPR18)", lambda s: f"{(s//2+75)/hp_rate:.0f}s")
row("Stam refill 0->max secs (Foc120,SR24)", lambda s: f"{s/st_rate:.0f}s")
