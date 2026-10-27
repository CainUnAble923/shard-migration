"""Print a coarse land/sea strip south of the SoS Haven town (3614-3722, 2516-2657). Map1.mul only, read-only."""
import sys

path = sys.argv[1]
W, H = 7168, 4096
data = open(path, "rb").read()
WATER = set(range(0xA8, 0xAC)) | {0x136, 0x137} | set(range(0x5797, 0x579C)) | set(range(0x746E, 0x7486))


def cell(x, y):
    b = (x // 8) * (H // 8) + (y // 8)
    o = b * 196 + 4 + ((y % 8) * 8 + (x % 8)) * 3
    tid = data[o] | (data[o + 1] << 8)
    z = data[o + 2] - 256 if data[o + 2] > 127 else data[o + 2]
    return tid, z


x1, x2, y1, y2 = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
step = int(sys.argv[6]) if len(sys.argv) > 6 else 4
print("     " + "".join(str((x // 10) % 10) if x % 40 == 0 else " " for x in range(x1, x2, step)))
for y in range(y1, y2, step):
    row = ""
    for x in range(x1, x2, step):
        tid, z = cell(x, y)
        row += "~" if tid in WATER else ("." if tid in (0x244, 0x2) else "#")
    print("%4d %s" % (y, row))
