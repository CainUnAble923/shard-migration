# First-draft XP curve for F-12 (levels 1-1000, loops). Not part of the server tree.
import math
CAPS = [50, 100, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000]  # loop 0..13 (F-12 overseer ladder)
C = 40.0      # XP to next level = C * L^1.5
XPK = 5.0     # XP per kill = XPK * creature level
LOOP_BONUS = 0.20   # +20% XP per completed loop
ECHO = 2.0    # x2 XP on levels already reached in an earlier loop

def xp_next(L): return int(C * L ** 1.5)
def xp_total(N): return sum(xp_next(L) for L in range(1, N))

print("| level | XP to next | total XP to reach |")
for L in (1, 2, 5, 10, 25, 50, 100, 150, 200, 300, 400, 500, 750, 1000):
    print(f"| {L} | {xp_next(L):,} | {xp_total(L):,} |")

def loop_hours(loop, kills_per_hour, level_ratio, content_top=None):
    cap = CAPS[loop]; prev = CAPS[loop - 1] if loop > 0 else 0
    mult_base = 1 + LOOP_BONUS * loop
    hours = 0.0
    for L in range(1, cap):
        cl = max(1.0, level_ratio * L)
        if content_top: cl = min(cl, content_top)
        m = mult_base * (ECHO if L < prev else 1.0)
        hours += xp_next(L) / (kills_per_hour * XPK * cl * m)
    return hours

A = dict(name="A: steady, at-level", kph=120, ratio=1.0)
B = dict(name="B: cautious, 75% of own level, half the kill rate", kph=60, ratio=0.75)
print()
print("| loop | cap | hours A | hours B | hours A if content tops at level 300 | cumulative A | cumulative B |")
ca = cb = 0
for i, cap in enumerate(CAPS):
    ha = loop_hours(i, A["kph"], A["ratio"]); hb = loop_hours(i, B["kph"], B["ratio"])
    ht = loop_hours(i, A["kph"], A["ratio"], content_top=300)
    ca += ha; cb += hb
    print(f"| {i} | {cap} | {ha:.0f} | {hb:.0f} | {ht:.0f} | {ca:.0f} | {cb:.0f} |")
