import math
vals=[125,140,155,170,185,200]
eff=[150,225,250,500]
def mana_rate(Int,med,focus,meditating,regen=0):
    mp=(Int+med*3)*(0.025 if med<100 else 0.0275)
    fp=focus*0.05
    t=fp+mp+(min(mp,13.0) if meditating else 0)
    t+=min(regen,18)
    t=math.floor(t)
    return 0.1*(2+t)  # mana per second
print("Mana regen (mana/s) Med120 Focus120 not-med / med ; Med300 Focus300 not-med / med ; MR18 Med120")
for i in vals+eff:
    print(i, round(mana_rate(i,120,120,False),2), round(mana_rate(i,120,120,True),2),
          round(mana_rate(i,300,300,False),2), round(mana_rate(i,300,300,True),2),
          round(mana_rate(i,120,120,False,18),2))
print("Int share of medPoints at Med120:", [round(i*0.0275,2) for i in vals+eff])
print("HitsMax pinned AOS Str/2+50+25:", [(s, s//2+50+25) for s in vals+eff])
print("Backpack/MaxWeight human 100+3.5S / other 40+3.5S:", [(s, 100+int(3.5*s), 40+int(3.5*s)) for s in vals+eff])
print("Meditation start window: deficit must be < skill+25. ManaMax=Int+150mimic")
for i in vals+eff:
    mm=i+150
    for sk in (120,300):
        print(" Int",i,"ManaMax",mm,"skill",sk,"window",sk+25,"share %.0f%%"%(100*min(1,(sk+25)/mm)), "chance@empty",round((50+(sk-mm)*2)/100,2))
print("Bless offset raw*(1+E/10)/100:")
for r in vals:
    print(r, int(r*0.13), int(r*0.31))
print("Greater str potion 20*(100+EP)/100 EP=50+alch*10/33:", [(a, int(20*(100+50+int(a*10/33))/100)) for a in (100,120,200,300)])
