import math
V=[125,140,155,170,185,200,150,225,500]
def hdr(t): print("\n== "+t); print("stat: "+" ".join(f"{v:>7}" for v in V))
def row(name,f): print(f"{name:<28}"+" ".join(f"{f(v):>7}" for v in V))

hdr("ML swing delay seconds (Stam=value, full stam). BaseWeapon.cs:1428-1451")
def swing(speed,stam,ssi):
    st=stam//30
    t=math.floor((speed*4-st)*(100.0/(100+ssi)))
    return max(t,5)*0.25
for sp in [2.0,2.5,3.0,3.5,4.25,5.0]:
    for ssi in [0,30,60]:
        row(f"speed {sp} SSI {ssi}", lambda v,sp=sp,ssi=ssi: f"{swing(sp,v,ssi):.2f}")
print("\nStam needed to hit 1.25s floor:")
for sp in [2.0,2.5,3.0,3.5,4.25,5.0]:
    out=[]
    for ssi in [0,30,60]:
        s=next(s for s in range(0,2000) if swing(sp,s,ssi)==1.25)
        out.append(f"SSI{ssi}:{s}")
    print(f"  speed {sp}: "+", ".join(out))

hdr("AOS melee damage multiplier, Tactics120 Anat120 DI100, non-axe. BaseWeapon.cs:2556-2602")
def strb(s): return (s*0.3+(5 if s>=100 else 0))/100
an=(120*0.5+5)/100; ta=(120*0.625+6.25)/100
row("str bonus %", lambda v: f"{strb(v)*100:.1f}")
row("total multiplier x", lambda v: f"{1+strb(v)+an+ta+1.0:.3f}")
row("vs Str125 (%)", lambda v: f"{((1+strb(v)+an+ta+1)/(1+strb(125)+an+ta+1)-1)*100:+.1f}")
lj=(100*0.2+10)/100
row("axe LJ100 multiplier x", lambda v: f"{1+strb(v)+an+ta+lj+1.0:.3f}")

hdr("Force of Nature SA damage scalar. ForceOfNature.cs:106")
row("scalar", lambda v: f"{(100+min(100,max(50,v-50)))/100:.2f}")

hdr("Weapon hit-spell damage (Int/10 % bonus, SDI0, Inscr0). BaseWeapon.cs:2265,3642")
row("Int bonus %", lambda v: v//10)
row("HitLightning avg dmg", lambda v: f"{25.5*(100+v//10)/100:.1f}")
row("HitLightning avg SDI15", lambda v: f"{25.5*(100+v//10+15)/100:.1f}")

hdr("Self bandage delay s (AOS). Bandage.cs:491")
row("self", lambda v: f"{5.0+0.5*((120-v)/10):.2f}")
hdr("Other bandage delay s (AOS, alive). Bandage.cs:500-507")
row("other", lambda v: f"{(3.2-math.sin(v/130)*2.5) if v<204 else 0.7:.2f}")

hdr("Thrown weapon max range. BaseThrown.cs:24")
for n,mtr,req in [("Boomerang",4,25),("Cyclone",6,40),("SoulGlaive",8,60)]:
    base=mtr+3
    def r(v,base=base,req=req):
        return base-3+int((v-req)/((140-req)//3))
    row(f"{n} (OSI-max {base} @140)", r)

hdr("Parry dex factor. BaseWeapon.cs:1535,1574")
row("factor", lambda v: f"{((20+v)/100 if v<80 else 1.0):.2f}")

hdr("ThrowingDagger. ThrowingDagger.cs:57,61")
row("hit% vs target Dex", lambda v: f"{max(0,1-math.sqrt(v/100)*0.8)*100:.1f}")
row("dmg range (Str)", lambda v: f"5-{5+v//10-1}")

hdr("PlayerMobile HitsMax AOS (BonusHits 25). context only")
row("HitsMax", lambda v: v//2+50+25)
