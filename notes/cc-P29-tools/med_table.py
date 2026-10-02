# cc-P29 Part B: Meditation start chance before (OSI, absolute deficit) and after (deficit scaled to a 150 pool
# above 150), as ours Meditation.StartChance computes it. A human with no Mana Increase: ManaMax = Int.
import math
def osi(skill, mana, mx): return (50 + (skill - (mx - mana)) * 2) / 100
def ours(skill, mana, mx):
    d = mx - mana
    if mx > 150: d = d * 150 / mx
    return (50 + (skill - d) * 2) / 100
def clamp(c): return max(0.0, min(1.0, c))
def least(f, skill, mx):
    for mana in range(mx + 1):
        if f(skill, mana, mx) > 0: return mana
    return None
print('| Int (= ManaMax) | Med | chance at 0 mana, before -> after | at half, before -> after | least mana for any chance, before -> after |')
print('|---|---|---|---|---|')
for i in (100, 125, 200, 500):
    for m in (50, 100, 120):
        print(f'| {i} | {m} | {clamp(osi(m,0,i)):.2f} -> {clamp(ours(m,0,i)):.2f} | {clamp(osi(m,i//2,i)):.2f} -> {clamp(ours(m,i//2,i)):.2f} | {least(osi,m,i)} -> {least(ours,m,i)} |')
