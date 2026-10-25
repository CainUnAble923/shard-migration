"""Can a player walk down from the Barako platform (679,1757,100) to the ground?

Reads the vseUOAware region dumps (land id/z + statics per tile) and a tiledata.mul, and runs a breadth-first search
using pinned ModernUO's Movement.Check rules (UOContent/Engines/Pathing/Movement.cs:236-470): a move to a tile lands on
the best surface whose top is within StepHeight (2) of the start top, and only if no impassable static on that tile
overlaps [newZ, max(startZ + 16, newZ + 16)). Diagonal moves: tried two ways (see --diag).
"""
import json, re, struct, sys
from collections import deque

TILEDATA = "D:/UO/ClassicUO/ClassicUO/Ultima Online Classic/tiledata.mul"
SURFACE, IMPASSABLE, BRIDGE, WET = 0x200, 0x40, 0x400, 0x80


def load_tiledata(path):
    data = open(path, "rb").read()
    off = 512 * (4 + 32 * 30)  # land table, new format (64-bit flags)
    items = {}
    idx = 0
    while off + 4 <= len(data):
        off += 4
        for _ in range(32):
            if off + 41 > len(data):
                break
            flags = struct.unpack_from("<Q", data, off)[0]
            height = data[off + 20]
            name = data[off + 21:off + 41].split(b"\0")[0].decode("latin-1")
            items[idx] = (flags, height, name)
            idx += 1
            off += 41
    land = {}
    o = 0
    li = 0
    for _ in range(512):
        o += 4
        for _ in range(32):
            flags = struct.unpack_from("<Q", data, o)[0]
            land[li] = flags
            li += 1
            o += 30
    return items, land


def load_dumps(paths):
    tiles = {}
    for p in paths:
        cur = None
        for line in open(p, encoding="utf-8"):
            m = re.match(r"\((\d+), (\d+)\): land 0x([0-9A-F]+) \(\d+\), Z=(-?\d+)", line)
            if m:
                cur = (int(m[1]), int(m[2]))
                tiles[cur] = [int(m[3], 16), int(m[4]), []]
                continue
            m = re.match(r"\s+- tile 0x([0-9A-F]+) \(\d+\), Z=(-?\d+)", line)
            if m and cur:
                tiles[cur][2].append((int(m[1], 16), int(m[2])))
    return tiles


def main():
    diag_mode = sys.argv[1]  # "ortho" | "lenient"
    dumps = sys.argv[2:]
    items, land = load_tiledata(TILEDATA)

    # cross-check against the MCP's reading of the server's tiledata
    for tid, want_flags, want_h in ((0x050A, 0x2601, 0), (0x0093, 0x6050, 0x14), (0x080D, 0x44040, 0x15), (0x21A3, 0x2050, 0x64)):
        f, h, n = items[tid]
        assert (f & 0xFFFFFFFF, h) == (want_flags, want_h), (hex(tid), hex(f), h, n)

    tiles = load_dumps(dumps)

    def calc_h(tid):
        f, h, _ = items[tid]
        return h // 2 if f & BRIDGE else h

    def avg_z(x, y):
        def lz(a, b):
            t = tiles.get((a, b))
            return t[1] if t else None
        top, left, right, bottom = lz(x, y), lz(x, y + 1), lz(x + 1, y), lz(x + 1, y + 1)
        if None in (top, left, right, bottom):
            return None
        if abs(top - bottom) > abs(left - right):
            return (left + right) // 2  # floor like pinned for non-negative z
        return (top + bottom) // 2

    def ok(x, y, our_z, test_top):
        for tid, z in tiles[(x, y)][2]:
            f = items[tid][0]
            if f & IMPASSABLE:  # ImpassableSurface = Impassable | Surface; Surface-only items are not blockers here
                top = z + calc_h(tid)
                if top > our_z and test_top > z:
                    return False
        return True

    def check(x, y, start_z, start_top):
        """Pinned Movement.Check for a player (no swim): the new z, or None."""
        if (x, y) not in tiles:
            return None
        land_id, _, statics = tiles[(x, y)]
        step_top = start_top + 2
        check_top = start_z + 16
        best = None
        for tid, iz in statics:
            f, h, _ = items[tid]
            if not (f & SURFACE) or (f & IMPASSABLE):
                continue
            our_z = iz + calc_h(tid)
            test_top = max(check_top, our_z + 16)
            item_top = iz if f & BRIDGE else iz + h
            if step_top < item_top:
                continue
            if best is not None:
                cmp = abs(our_z - start_z) - abs(best - start_z)
                if cmp > 0 or (cmp == 0 and our_z > best):
                    continue
            if ok(x, y, our_z, test_top):
                best = our_z
        lflags = land.get(land_id, 0)
        land_center = avg_z(x, y)
        if land_center is not None and not (lflags & IMPASSABLE) and land_id != 2 and step_top >= land_center:
            test_top = max(check_top, land_center + 16)
            should = True
            if best is not None:
                cmp = abs(land_center - start_z) - abs(best - start_z)
                if cmp > 0 or (cmp == 0 and land_center > best):
                    should = False
            if should and ok(x, y, land_center, test_top):
                best = land_center
        return best

    start = (679, 1757, 100)
    seen = {start}
    q = deque([start])
    down = []
    while q:
        x, y, z = q.popleft()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                nz = check(x + dx, y + dy, z, z)
                if nz is None:
                    continue
                if dx and dy:
                    a = check(x + dx, y, z, z)
                    b = check(x, y + dy, z, z)
                    if diag_mode == "ortho" or (a is None and b is None):
                        continue
                n = (x + dx, y + dy, nz)
                if n not in seen:
                    seen.add(n)
                    q.append(n)
                    if nz < 90:
                        down.append(((x, y, z), n))
    zs = sorted({p[2] for p in seen})
    xs = [p[0] for p in seen]
    ys = [p[1] for p in seen]
    print(f"{diag_mode}: reached {len(seen)} positions, z values {zs}, x {min(xs)}-{max(xs)}, y {min(ys)}-{max(ys)}")
    edge = [p for p in seen if any((p[0] + a, p[1] + b) not in tiles for a in (-1, 0, 1) for b in (-1, 0, 1))]
    print(f"positions on the dump's edge (search may continue past it): {len(edge)}", sorted(edge)[:20])
    print("first steps below z 90:", down[:10])


main()
