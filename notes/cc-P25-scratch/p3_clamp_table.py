# P25 Part 3: what each effective clamp does at max level 200 (raw 200). Formulas cited in the notes.
import math
cols=[("OSI 150",150),("raw only 200",200),("eff 225",225),("eff 250",250),("eff 500",500)]
def hits(e): return e//2+50+25                        # PlayerMobile.cs:548-577, BonusHits cap 25
def selfband(e):                                      # Bandage.cs:493, Timer 8ms floor Timer.TimerWheel.cs:174-179
    s=5.0+0.5*((120-e)/10); return "8ms" if s<=0 else f"{s:.2f}s"
def swing(speed,ssi,stam):                            # BaseWeapon.cs:1428-1449
    t=math.floor((speed*4-stam//30)*(100.0/(100+ssi))); return max(t,5)*0.25
def strmult(e): return 1+(e*0.3+5)/100+0.65+0.8125+1.0  # BaseWeapon.cs:2556, :2502-2512; Anat/Tac 120, DI 100
def fs_pvp(e):                                        # Spell.cs:219-257 Inscr 120 Eval 120 SDI 15, dice avg 51
    d=51*100; d=d*(100+11+e//10+15)//100; d=d*138//100; return d//100
def throw(e): return 8+(e-60)//((140-60)//3)          # BaseThrown.cs:24, SoulGlaive (design max 11)
def carry(e): return 100+int(3.5*e)                   # PlayerMobile.cs:237 via ClusterFBackpack.cs:33-42
def medmin(pool,med=120):                             # Meditation.cs:83 ours; chance>0 needs deficit < med+25
    return max(0,pool-(med+25)+1)
rows=[("HitsMax",lambda e:hits(e)),
("Self-bandage delay",selfband),
("Bow 4.25 SSI60 swing, Stam=Dex",lambda e:f"{swing(4.25,60,e):.2f}s"),
("Bow 4.25 SSI60 swing, Stam=Dex+150 mimic",lambda e:f"{swing(4.25,60,e+150):.2f}s"),
("H.xbow 5.0 SSI0 swing, Stam=Dex",lambda e:f"{swing(5.0,0,e):.2f}s"),
("Melee damage multiplier",lambda e:f"{strmult(e):.3f}"),
("Flame Strike PvP avg",fs_pvp),
("Soul Glaive range",throw),
("Carry (human)",carry),
("Mana pool (no items)",lambda e:e),
("Min mana to meditate, Med 120",lambda e:medmin(e)),
("Mind Blast (Magery 120)",lambda e:min((120+e)//5,60)),
]
print("| formula | "+" | ".join(c for c,_ in cols)+" |"); print("|---"*(len(cols)+1)+"|")
for n,f in rows: print(f"| {n} | "+" | ".join(str(f(e)) for _,e in cols)+" |")
