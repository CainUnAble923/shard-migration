# cc-P858: open ground in New Haven's town box (x 3568-3761, y 2460-2712, Trammel) where the wagon, its stair and the
# stall beside it could all stand: a clean 8 x 18 rectangle (flat land at z 0 or within 1, no static), no pinned spawner
# within 3, ranked by distance to the bank square. Read only; prints the best few.
import os, sys
sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\scripts")
from mapbuild import uofiles as U
folder = sys.argv[1] if len(sys.argv) > 1 else r"D:\UO\tool-trials\client-data-copy"
X1, Y1, X2, Y2 = 3568, 2460, 3761, 2712
land = U.MapFile(folder, 1).region(X1, Y1, X2, Y2)
st = set((x, y) for (x, y, z, t) in U.statics_in(folder, 1, X1, Y1, X2, Y2))
SPAWN = [(3575, 2523), (3594, 2595), (3615, 2476), (3618, 2614), (3620, 2617), (3625, 2594), (3628, 2540), (3632, 2573),
 (3633, 2635), (3635, 2625), (3642, 2504), (3645, 2617), (3645, 2661), (3649, 2591), (3650, 2509), (3651, 2627),
 (3652, 2511), (3652, 2619), (3655, 2665), (3661, 2531), (3665, 2581), (3667, 2506), (3668, 2652), (3671, 2615),
 (3673, 2595), (3674, 2624), (3687, 2477), (3693, 2509), (3700, 2699), (3711, 2571), (3711, 2669), (3711, 2679),
 (3711, 2690), (3714, 2651), (3716, 2612), (3716, 2617), (3716, 2624), (3716, 2632), (3725, 2670), (3726, 2647),
 (3727, 2603), (3736, 2512), (3738, 2586), (3738, 2610), (3740, 2692), (3742, 2520), (3744, 2660), (3745, 2585),
 (3751, 2704), (3753, 2705), (3754, 2704)]
ok = {k for k, v in land.items() if abs(v[1]) <= 1 and k not in st}
BANK = (3636, 2627)
out = []
for ox in range(X1 + 2, X2 - 6):
    for oy in range(Y1 + 6, Y2 - 12):
        if all((ox + dx, oy + dy) in ok for dx in range(-2, 6) for dy in range(-6, 12)):
            if all(max(abs(ox + 1 - sx), abs(oy + 3 - sy)) > 3 for sx, sy in SPAWN):
                out.append((max(abs(ox - BANK[0]), abs(oy - BANK[1])), ox, oy))
out.sort()
seen = []
for d, ox, oy in out:
    if all(max(abs(ox - a), abs(oy - b)) > 6 for a, b in seen):
        seen.append((ox, oy))
        print("origin %d,%d  (%d from the stall)" % (ox, oy, d))
    if len(seen) >= 8:
        break
print(len(out), "origins in all")
