r"""cc-P688 (SoS swap S15) part 1: the walk between places on the SoS land, by flood fill.

The playbook's walk (section 6: pinned Movement.cs reduced to the map files), over the whole SoS Trammel map at once.
Felucca stands on the same land (P675), so one grid answers both. Per tile, one standing level (the highest, as
P681's sosgrid):
  stand  the Z a walker stands at: the land's centre (pinned GetAverageZ avg, FloorAverage) when the land is neither
         Impassable nor Wet, raised to a Surface static's top (z + CalcHeight; a Bridge counts half its height) that
         starts within 16 above the land (or any surface over water or rock); NONE when an Impassable non-Surface
         static overlaps the 16 above it, or there is nothing to stand on;
  low    what Movement.Check compares the step against on arrival: the land's lowest corner (landZ) for land, the
         surface's itemTop (z + height, a Bridge's z) for a surface;
  top    GetStartZ's zTop on leaving: the land's highest corner, or the surface's z + height, at least stand.
A step from A to a 4-neighbour B is allowed when top[A] + StepHeight 2 >= low[B] (Movement.cs:265 stepTop, :346, :437).
Going down has no limit, so many steps are one way. A diagonal step also needs both side tiles allowed from A (a
player below GameMaster, Movement.cs:146-151).

Mutual steps make walk areas (min-label propagation with pointer jumping); one-way steps and the shipped Trammel
teleporters (teleporters-sos.json, a step onto the source tile) join areas in one direction. A place is reachable
from another when its area is reached from the other's over those joins.

Not modelled (each is said in the notes): doors (decoration, read open), a second level on a tile (the lower of a
bridge over walkable land, a ground floor under an upper floor), the overhead check when stepping far down, mobiles.

    python -P walkgrid.py <code copy>      -> out/places.csv, out/reach.csv, out/groups.txt (and the cache)
"""
import collections
import csv
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # MUTANT copy lives in mutants/
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(NOTES), "scripts"))
import islands  # noqa: E402
from mapbuild import uofiles  # noqa: E402

IMP, WET, SURF, BRIDGE = 0x40, 0x80, 0x200, 0x400
PERSON, STEP = 16, 2
NONE = -32768
W, H = 7168, 4096
OUT = os.path.join(HERE, "out")
CACHE = os.environ.get("P688_CACHE", os.path.join(os.environ.get("TEMP", HERE), "p688-walkgrid.npz"))
DIRS8 = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


def shifted(a, dx, dy, fill):
    """b[x, y] = a[x + dx, y + dy], fill past the edge."""
    b = np.full_like(a, fill)
    w, h = a.shape
    xs, xd = (slice(dx, None), slice(0, w - dx)) if dx >= 0 else (slice(0, w + dx), slice(-dx, None))
    ys, yd = (slice(dy, None), slice(0, h - dy)) if dy >= 0 else (slice(0, h + dy), slice(-dy, None))
    b[xd, yd] = a[xs, ys]
    return b


def build(name="sos", extra=()):
    """stand, low, top as int16 (W, H). extra: (x, y, z, id) statics to add (a test's or a fix's)."""
    land, items = uofiles.read_tiledata(uofiles.CLIENT)
    lflags = np.array([l[0] for l in land], dtype=np.uint64)
    iflags = np.array([it["flags"] for it in items], dtype=np.uint64)
    iheight = np.array([it["height"] for it in items], dtype=np.int32)
    ids, zs = islands.load_land(name)
    sx, sy, sz, sid = islands.load_statics(name)
    if extra:
        ex = np.array(extra, dtype=np.int64).reshape(-1, 4)
        sx, sy, sz, sid = (np.concatenate([a, ex[:, i]]) for i, a in enumerate((sx, sy, sz, sid)))
    z = zs.astype(np.int32)
    r = np.vstack([z[1:, :], z[-1:, :]])          # x + 1
    l = np.hstack([z[:, 1:], z[:, -1:]])          # y + 1
    b = np.vstack([l[1:, :], l[-1:, :]])          # x + 1, y + 1
    landz = np.minimum(np.minimum(z, l), np.minimum(r, b))
    landtop = np.maximum(np.maximum(z, l), np.maximum(r, b))
    avg = np.where(np.abs(z - b) > np.abs(l - r), (l + r) // 2, (z + b) // 2)
    del r, l, b
    lf = lflags[ids]
    land_ok = ((lf & np.uint64(IMP)) == 0) & ((lf & np.uint64(WET)) == 0)
    del lf

    sx, sy, sz = sx.astype(np.int64), sy.astype(np.int64), sz.astype(np.int32)
    sid = np.minimum(sid.astype(np.int64), len(iflags) - 1)
    flat = sx * H + sy
    f = iflags[sid]
    h = iheight[sid]
    is_surf = (f & np.uint64(SURF)) != 0
    is_imp = (f & np.uint64(IMP)) != 0
    is_bridge = (f & np.uint64(BRIDGE)) != 0
    calc = sz + np.where(is_bridge, h // 2, h)          # ourZ on it
    itop = np.where(is_bridge, sz, sz + h)              # itemTop, what stepTop must reach
    full = sz + h                                       # zTop when leaving it
    okf = land_ok.reshape(-1)[flat]
    base = avg.reshape(-1)[flat]
    use = is_surf & ~is_imp & ((~okf) | ((calc >= base) & (sz <= base + PERSON)))

    stand = np.where(land_ok, avg, NONE).astype(np.int32).reshape(-1)
    np.maximum.at(stand, flat[use], calc[use])
    on_surf = np.zeros(W * H, dtype=bool)
    st = stand[flat]
    win = use & (calc == st) & ~(okf & (calc == base))  # the surface that sets the level (land wins a tie)
    on_surf[flat[win]] = True
    low = np.where(land_ok, landz, NONE).astype(np.int32).reshape(-1)
    top = np.where(land_ok, landtop, NONE).astype(np.int32).reshape(-1)
    low[on_surf] = 32767
    top[on_surf] = NONE
    np.minimum.at(low, flat[win], itop[win])
    np.maximum.at(top, flat[win], full[win])
    top = np.maximum(top, stand)

    has = stand != NONE
    tt = stand[flat]
    blk = is_imp & ~is_surf & has[flat] & (sz < tt + PERSON) & (sz + np.maximum(h, 1) > tt)
    # a surface overhead within 16 blocks too (IsOk's ImpassableSurface test), unless it is the one stood on
    blk |= is_surf & has[flat] & (sz < tt + PERSON) & (sz > tt)
    blocked = np.zeros(W * H, dtype=bool)
    blocked[flat[blk]] = True
    ok = has & ~blocked
    stand = np.where(ok, stand, NONE)
    low = np.where(ok, low, NONE)
    top = np.where(ok, top, NONE)
    return (stand.astype(np.int16).reshape(W, H), low.astype(np.int16).reshape(W, H),
            top.astype(np.int16).reshape(W, H))


def load(name="sos"):
    if name == "sos" and os.path.exists(CACHE):
        d = np.load(CACHE)
        return d["stand"], d["low"], d["top"]
    g = build(name)
    if name == "sos":
        np.savez(CACHE, stand=g[0], low=g[1], top=g[2])
    return g


def steps(stand, low, top):
    """can[d][x, y]: a step from (x, y) in DIRS8[d] is allowed."""
    ok = stand != NONE
    reach = stand.astype(np.int32) + STEP   # MUTANT: stand to stand
    low = stand
    out = []
    for dx, dy in DIRS8[:4]:
        nb_low = shifted(low, dx, dy, 32767).astype(np.int32)
        out.append(ok & shifted(ok, dx, dy, False) & (reach >= nb_low))
    for dx, dy in DIRS8[4:]:
        nb_low = shifted(low, dx, dy, 32767).astype(np.int32)
        c = ok & shifted(ok, dx, dy, False) & (reach >= nb_low)
        c &= out[DIRS8.index((dx, 0))] | out[DIRS8.index((0, dy))]   # MUTANT: one side
        out.append(c)
    return out


def areas(can):
    """The walk area of every tile: tiles joined by steps allowed both ways. -1 where nobody stands."""
    w, h = can[0].shape
    n = w * h
    lab = np.arange(n, dtype=np.int32).reshape(w, h)
    mutual = []
    for d, (dx, dy) in enumerate(DIRS8):
        back = DIRS8.index((-dx, -dy))
        mutual.append(can[d] & shifted(can[back], dx, dy, False))
    stood = can[0] | can[1] | can[2] | can[3] | can[4] | can[5] | can[6] | can[7]
    big = np.int32(n)
    it = 0
    while True:
        it += 1
        new = lab.copy()
        for d, (dx, dy) in enumerate(DIRS8):
            np.minimum(new, np.where(mutual[d], shifted(lab, dx, dy, big), big), out=new)
        flat = new.reshape(-1)
        for _ in range(64):                     # pointer jumping to a fixpoint: far fewer rounds than two jumps
            nxt = flat[flat]
            if np.array_equal(nxt, flat):
                break
            flat = nxt
        new = flat.reshape(w, h)
        if np.array_equal(new, lab):
            break
        lab = new
    lab = np.where(stood, lab, -1)
    return lab, mutual, it


def one_way(can, mutual, lab):
    """(from area, to area) for every step allowed only one way, unique."""
    pairs = []
    for d, (dx, dy) in enumerate(DIRS8):
        m = can[d] & ~mutual[d]
        xs, ys = np.nonzero(m)
        if len(xs):
            a = lab[xs, ys]
            b = lab[xs + dx, ys + dy]
            k = a != b
            pairs.append(np.stack([a[k], b[k]], axis=1))
    if not pairs:
        return np.zeros((0, 2), np.int64)
    return np.unique(np.concatenate(pairs).astype(np.int64), axis=0)


# ---- the places ----------------------------------------------------------------------------------------------------

MOONGATES = [  # PMList Trammel and Felucca on SoS (server/patches/PublicMoongate-sos-gates.patch, HavenSpots)
    ("Moonglow", 4467, 1283), ("Britain", 1336, 1997), ("Jhelom", 1499, 3771), ("Yew", 771, 752),
    ("Minoc", 2701, 692), ("Trinsic", 1828, 2948), ("Skara Brae", 643, 2067), ("Magincia", 3563, 2139),
    ("New Haven", 3696, 2570), ("Buccaneer's Den (Felucca)", 2711, 2234),
]


def town_of(regions, x, y):
    for name, rects in regions:
        if any(x1 <= x < x2 and y1 <= y < y2 for x1, y1, x2, y2 in rects):
            return name
    return ""


def places(code):
    """(kind, name, x, y) for every bank, public moongate and dock on the SoS surface."""
    regions = [(r["Name"], [(a["x1"], a["y1"], a["x2"], a["y2"]) for a in r["Area"]])
               for r in json.load(open(os.path.join(code, "server", "data", "regions-trammel.json"), encoding="utf-8"))
               if r.get("$type") in ("TownRegion", "GuardedRegion") and r.get("Name")]
    out = []
    seen = set()
    for r in csv.DictReader(open(os.path.join(NOTES, "cc-P681-tools", "out", "ledger.csv"), encoding="utf-8")):
        if r["facet"] != "Trammel" or r["role"] != "bank" or r["action"] != "keep":
            continue
        x, y = (int(r["nx"]), int(r["ny"])) if r["nx"] else (int(r["x"]), int(r["y"]))
        if (x, y) not in seen:
            seen.add((x, y))
            out.append(("bank", town_of(regions, x, y) or "bank %d,%d" % (x, y), x, y))
    out.append(("bank", "New Haven", 3620, 2617))           # HavenSpots.Bank (S7)
    for p in sorted(os.listdir(os.path.join(code, "server", "data", "Spawns", "sos", "towns"))):
        for s in json.load(open(os.path.join(code, "server", "data", "Spawns", "sos", "towns", p), encoding="utf-8")):
            names = {(e.get("name") or "").lower() for e in s.get("entries", [])}
            if "banker" in names and s.get("map") == "Trammel":
                x, y = s["location"][:2]
                if (x, y) not in seen:
                    seen.add((x, y))
                    out.append(("bank", town_of(regions, x, y) or os.path.splitext(p)[0], x, y))
    for name, x, y in MOONGATES:
        out.append(("moongate", name, x, y))
    for r in csv.DictReader(open(os.path.join(NOTES, "cc-P684-tools", "out", "docks.csv"), encoding="utf-8")):
        out.append(("dock", r["dock"], int(r["x"]), int(r["y"])))
    return out


def teleporters(code):
    t = json.load(open(os.path.join(code, "server", "data", "teleporters-sos.json"), encoding="utf-8"))
    return [(e["src"]["loc"][:2], e["dst"]["loc"][:2]) for e in t
            if e["src"]["map"] == "Trammel" and e["dst"]["map"] == "Trammel"]


def snap(lab, x, y, r=3):
    """The area at (x, y), or the nearest stood tile within r (a banker stands behind a counter)."""
    best = None
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            if 0 <= x + dx < W and 0 <= y + dy < H and lab[x + dx, y + dy] >= 0:
                d = max(abs(dx), abs(dy)) * 10 + abs(dx) + abs(dy)
                if best is None or d < best[0]:
                    best = (d, int(lab[x + dx, y + dy]), x + dx, y + dy)
    return best


LABELS = os.path.splitext(CACHE)[0] + "-areas.npz"


def labelled(g=None):
    """(lab, land, edges, iters): the walk areas, the dry land's masses (every step allowed, heights ignored), and the
    one-way joins. Cached beside the grid when g is the SoS grid."""
    if g is None and os.path.exists(LABELS):
        d = np.load(LABELS)
        return d["lab"], d["land"], d["edges"], int(d["iters"])
    stand, low, top = g if g is not None else load()
    can = steps(stand, low, top)
    lab, mutual, iters = areas(can)
    edges = one_way(can, mutual, lab)
    del can, mutual
    flat = np.where(stand != NONE, np.int16(0), np.int16(NONE))
    land, _, _ = areas(steps(flat, flat, flat))
    if g is None:
        np.savez(LABELS, lab=lab, land=land, edges=edges, iters=iters)
    return lab, land, edges, iters


def survey(code, g=None):
    stand = (g if g is not None else load())[0]
    lab, land, edges, iters = labelled(g)
    tele = []
    for (sx, sy), (dx, dy) in teleporters(code):
        a, b = snap(lab, sx, sy, 1), snap(lab, dx, dy, 1)
        if a and b and a[1] != b[1]:
            tele.append((a[1], b[1]))
    nxt = collections.defaultdict(set)
    for a, b in edges.tolist():
        nxt[a].add(b)
    for a, b in tele:
        nxt[a].add(b)
    size = collections.Counter(lab[lab >= 0].tolist())
    rows = []
    for kind, name, x, y in places(code):
        s = snap(lab, x, y)
        rows.append(dict(kind=kind, name=name, x=x, y=y, area=s[1] if s else -1, sx=s[2] if s else "",
                         sy=s[3] if s else "", z=int(stand[s[2], s[3]]) if s else "", tiles=size.get(s[1], 0) if s else 0,
                         land=int(land[s[2], s[3]]) if s else -1))
    reach = {}
    for a in {r["area"] for r in rows if r["area"] >= 0}:
        seen, q = {a}, collections.deque([a])
        while q:
            c = q.popleft()
            for n in nxt.get(c, ()):
                if n not in seen:
                    seen.add(n)
                    q.append(n)
        reach[a] = seen
    return dict(lab=lab, land=land, rows=rows, reach=reach, iters=iters, edges=len(edges), tele=len(tele), size=size)


def groups(rows, reach):
    """Places that all reach each other on foot, largest first."""
    out, done = [], set()
    for i, r in enumerate(rows):
        if i in done or r["area"] < 0:
            continue
        g = [j for j, s in enumerate(rows) if s["area"] >= 0 and s["area"] in reach[r["area"]]
             and r["area"] in reach[s["area"]]]
        done.update(g)
        out.append(g)
    return sorted(out, key=lambda g: -len(g))


def main():
    code = sys.argv[1]
    res = survey(code)
    rows, reach = res["rows"], res["reach"]
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "places.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(OUT, "reach.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["from_kind", "from", "to_kind", "to", "on_foot"])
        for r in rows:
            for s in rows:
                if r is not s:
                    ok = r["area"] >= 0 and s["area"] in reach.get(r["area"], ())
                    w.writerow([r["kind"], r["name"], s["kind"], s["name"], "yes" if ok else "no"])
    gs = groups(rows, reach)
    with open(os.path.join(OUT, "groups.txt"), "w", encoding="utf-8") as f:
        f.write("label propagation %d rounds; %d one-way joins; %d teleporter joins\n" % (res["iters"], res["edges"], res["tele"]))
        for k, g in enumerate(gs):
            a = rows[g[0]]["area"]
            f.write("\ngroup %d (%d places, area of %d tiles, land mass %d)\n" % (k + 1, len(g), res["size"].get(a, 0),
                                                                          rows[g[0]]["land"]))
            for j in g:
                r = rows[j]
                f.write("  %-8s %-34s %4d,%4d\n" % (r["kind"], r["name"], r["x"], r["y"]))
            more = sorted({rows[j]["name"] for j, s in enumerate(rows) if s["area"] >= 0 and s["area"] in reach.get(a, ())
                           and j not in g})
            if more:
                f.write("  reaches one way: %s\n" % ", ".join(more))
        f.write("\nsame dry land, but no walk between them (a cut to fix, or a fence on purpose):\n")
        cut = 0
        for g1 in gs:
            for g2 in gs:
                a, b = rows[g1[0]], rows[g2[0]]
                if a is not b and a["land"] == b["land"] and b["area"] not in reach.get(a["area"], ()):
                    f.write("  %s (%s) cannot walk to %s (%s)\n" % (a["name"], a["kind"], b["name"], b["kind"]))
                    cut += 1
        if not cut:
            f.write("  none\n")
        bad = [r for r in rows if r["area"] < 0]
        for r in bad:
            f.write("\nnot standable within 3: %s %s %d,%d\n" % (r["kind"], r["name"], r["x"], r["y"]))
    print(open(os.path.join(OUT, "groups.txt"), encoding="utf-8").read())


if __name__ == "__main__":
    main()
