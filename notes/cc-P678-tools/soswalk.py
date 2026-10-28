r"""cc-P678: the playbook's walk (cc-P188 build_way_in.Walk: pinned Movement.cs's rules reduced to the map files) over
the SoS Trammel files, for a rectangle. Land Impassable or Wet blocks; an Impassable non-Surface static that overlaps
the walker's PersonHeight 16 above the standing Z blocks; a Surface raises the standing Z; a step up over StepHeight 2
blocks. Doors are decoration items, not statics, so a doorway reads open.
    python -P soswalk.py x1 y1 x2 y2 sx sy gx gy     -> the path length from (sx, sy) to (gx, gy), or why not
Use from python: w = Walk(rect); w.stand[(x, y)] is the standing Z or None; w.why[(x, y)] the reason it blocks.
Read only.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(NOTES), "scripts"))
import islands  # noqa: E402
from mapbuild import uofiles  # noqa: E402

IMP, WET, SURF = 0x40, 0x80, 0x200
PERSON, STEP = 16, 2

_files = {}


def files():
    if not _files:
        ids, zs = islands.load_land("sos")
        sx, sy, sz, sid = islands.load_statics("sos")
        land, items = uofiles.read_tiledata(uofiles.CLIENT)
        _files.update(ids=ids, zs=zs, sx=sx, sy=sy, sz=sz, sid=sid, land=land, items=items)
    return _files


class Walk:
    def __init__(self, rect, extra=()):
        """extra: (x, y, z, id) statics to add (a hatch, a ladder) before the walk is surveyed."""
        f = files()
        self.rect = x1, y1, x2, y2 = rect
        m = (f["sx"] >= x1 - 1) & (f["sx"] <= x2 + 1) & (f["sy"] >= y1 - 1) & (f["sy"] <= y2 + 1)
        self.sts = collections.defaultdict(list)
        for x, y, z, i in zip(f["sx"][m], f["sy"][m], f["sz"][m], f["sid"][m]):
            self.sts[(int(x), int(y))].append((int(z), int(i)))
        for x, y, z, i in extra:
            self.sts[(x, y)].append((z, i))
        self.why, self.stand = {}, {}
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.why[(x, y)], self.stand[(x, y)] = self._tile(x, y)

    def _avgz(self, x, y):
        """pinned Map.GetAverageZ (Map.cs:243-285): the diagonal with the smaller slope, halved toward zero."""
        zs = files()["zs"]
        t, l, r, b = int(zs[x, y]), int(zs[x, y + 1]), int(zs[x + 1, y]), int(zs[x + 1, y + 1])
        return int((l + r) / 2) if abs(t - b) > abs(l - r) else int((t + b) / 2)

    def _tile(self, x, y):
        f = files()
        lid = int(f["ids"][x, y])
        lf = f["land"][lid][0]
        items = f["items"]
        sts = self.sts.get((x, y), [])
        z = self._avgz(x, y)
        top = None if (lf & IMP or lf & WET) else z
        for sz, i in sts:            # a surface over water or rock (a dock, a floor) stands the walker on it
            it = items[i]
            if it["flags"] & SURF and (top is None or (sz + it["height"] >= top and sz <= top + PERSON)):
                top = sz + it["height"] if top is None else max(top, sz + it["height"])
        if top is None:
            return ("water" if lf & WET else "land impassable"), None
        for sz, i in sts:
            it = items[i]
            if (it["flags"] & IMP) and not (it["flags"] & SURF) and sz < top + PERSON and sz + max(it["height"], 1) > top:
                return "static 0x%04X %s z%d" % (i, it["name"], sz), None
        return None, top

    def flood(self, start):
        q = collections.deque([start])
        prev = {start: None}
        while q:
            c = q.popleft()
            cz = self.stand[c]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c[0] + dx, c[1] + dy)
                if n in prev or self.stand.get(n) is None or self.stand[n] - cz > STEP:
                    continue
                prev[n] = c
                q.append(n)
        return prev

    def path(self, start, goal):
        prev = self.flood(start)
        if goal not in prev:
            return None
        out, c = [], goal
        while c is not None:
            out.append(c)
            c = prev[c]
        return out[::-1]


if __name__ == "__main__":
    a = [int(v) for v in sys.argv[1:9]]
    w = Walk(tuple(a[:4]))
    s, g = (a[4], a[5]), (a[6], a[7])
    print("start", s, w.stand[s], w.why[s], "goal", g, w.stand[g], w.why[g])
    p = w.path(s, g)
    print("no path" if p is None else "path %d tiles" % len(p))
