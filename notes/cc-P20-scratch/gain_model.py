# Model of pinned SkillCheck.CheckSkill gain chance (UOContent/Skills/SkillCheck.cs:112-124, AOS branch)
# plus ClusterFSkillGain (3 attempts, 5x amount). Not part of the server tree.
def gc(base, cap, total, totalcap, chance, success):
    g = (totalcap - total) / totalcap
    g += (cap - base) / cap
    g /= 2
    g += (1.0 - chance) * (0.5 if success else 0.0)
    g /= 2
    return max(g, 0.01)

def expected_gc(base, cap, total, totalcap, chance):
    return chance * gc(base, cap, total, totalcap, chance, True) + (1 - chance) * gc(base, cap, total, totalcap, chance, False)

def per_use_points(base, cap, total, totalcap, chance, attempts=3, amount=5):
    # expected skill points per use: up to `attempts` gain rolls, each gain = amount * 0.1
    p = expected_gc(base, cap, total, totalcap, chance)
    return attempts * p * amount * 0.1

levels = [50, 100, 120, 200, 300, 500, 1000]
for label, cap in (("live cap 300 (total cap 58*300=17400)", 300.0), ("cap 1000 (total cap 58*1000=58000)", 1000.0)):
    totalcap = 58 * cap
    print("##", label)
    print("| skill | A=(C-T)/C | B=(cap-base)/cap | gc easy (90%) | gc hard (50%) | pts/use easy | pts/use hard |")
    for b in levels:
        if b > cap: continue
        total = 7 * b  # assume 7 skills at this value
        A = (totalcap - total) / totalcap
        B = (cap - b) / cap
        e = expected_gc(b, cap, total, totalcap, 0.9)
        h = expected_gc(b, cap, total, totalcap, 0.5)
        print(f"| {b} | {A:.3f} | {B:.3f} | {e:.3f} | {h:.3f} | {per_use_points(b,cap,total,totalcap,0.9):.3f} | {per_use_points(b,cap,total,totalcap,0.5):.3f} |")
    print()

# OSI reference: cap 100, total cap 700, 7 skills
print("## OSI reference (cap 100/120, total 700, no ClusterF boost)")
for b in (50, 90, 100, 110):
    cap = 120.0 if b > 100 else 100.0
    total = min(700, 7 * b)
    A = (700 - total) / 700
    print(b, "A", round(A,3), "gc easy", round(expected_gc(b, cap, total, 700, 0.9),3), "gc hard", round(expected_gc(b, cap, total, 700, 0.5),3))

# uses to climb 0 -> cap for a use that always sits at a given success chance (difficulty tracks the player)
def uses_to_cap(cap, chance, start=0.0):
    totalcap = 58 * cap
    b = start; uses = 0
    while b < cap:
        b += per_use_points(b, cap, 7 * b, totalcap, chance)
        uses += 1
    return uses
print()
for cap in (50, 100, 120, 300, 500, 1000):
    print("cap", cap, "uses 0->cap easy", uses_to_cap(cap, 0.9), "hard", uses_to_cap(cap, 0.5))
