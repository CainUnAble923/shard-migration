r"""cc-P669: what the Siege of Sosaria Trammel map (Zigholtul, 3.0) changes against stock Trammel, measured.

Read only. Stock Trammel is map1LegacyMUL.uop + staidx1/statics1.mul of the vanilla 7.0.117.0 client
(D:\UO\UltimaOnlineVanilla); SoS is the author's Map1/Staidx1/Statics1.mul, read only through P481's data copies in
notes\cc-P481-tools\scratch\sos\ (never from D:\UO\third-party). Both are 7168 x 4096. The readers are P481's
(islands.load_land, load_statics, build), which use scripts\mapbuild\uofiles.

    python -P sosdiff.py blocks              -> scratch\blocks.npz, out\summary.json, art\sos-survey\change-map.png,
                                                art\sos-survey\sos-overview.png, art\sos-survey\stock-overview.png
    python -P sosdiff.py areas               -> out\areas.csv (connected changed areas, largest first)
    python -P sosdiff.py spots               -> out\spots.csv (every author go-menu spot: changed or stock around it)
    python -P sosdiff.py regions             -> out\stock-regions.csv (each stock Trammel region: share of it changed)
    python -P sosdiff.py points <csv>        -> out\<name>-checked.csv (any x,y list: changed within 8 tiles or not)
    python -P sosdiff.py rect x1 y1 x2 y2    -> land, statics and kinds in a rectangle, both maps (printed)

A block is 8 x 8 tiles. Land differs on a tile when its id or Z differs. Statics differ when the set of
(x, y, z, id) on the block differs (hue is ignored; duplicates of one exact static count once).
"""
import collections
import csv
import json
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
import islands  # noqa: E402

SCRATCH = os.path.join(HERE, "scratch")
OUT = os.path.join(HERE, "out")
ART = os.path.join(NOTES, "art", "sos-survey")
for d in (SCRATCH, OUT, ART):
    os.makedirs(d, exist_ok=True)
W, H = 7168, 4096
BW, BH = W // 8, H // 8
NPZ = os.path.join(SCRATCH, "blocks.npz")


def static_keys(name):
    sx, sy, sz, sid = islands.load_statics(name)
    blk = (sx // 8) * BH + (sy // 8)
    cell = (sx % 8) * 8 + (sy % 8)
    key = (blk.astype(np.int64) << 30) | (cell.astype(np.int64) << 24) | ((sz.astype(np.int64) + 128) << 16) | sid.astype(np.int64)
    return np.unique(key)


def blocks():
    print("loading land", flush=True)
    sid_, sz_ = islands.load_land("trammel")
    oid, oz = islands.load_land("sos")
    land_cell = (sid_ != oid) | (sz_ != oz)
    land_blk = land_cell.reshape(BW, 8, BH, 8).sum(axis=(1, 3))
    print("loading statics", flush=True)
    ks, ko = static_keys("trammel"), static_keys("sos")
    only_s = np.setdiff1d(ks, ko, assume_unique=True)
    only_o = np.setdiff1d(ko, ks, assume_unique=True)
    rem = np.bincount((only_s >> 30).astype(np.int64), minlength=BW * BH).reshape(BW, BH)
    add = np.bincount((only_o >> 30).astype(np.int64), minlength=BW * BH).reshape(BW, BH)
    cnt_s = np.bincount((ks >> 30).astype(np.int64), minlength=BW * BH).reshape(BW, BH)
    cnt_o = np.bincount((ko >> 30).astype(np.int64), minlength=BW * BH).reshape(BW, BH)
    print("kinds and colours", flush=True)
    col_s, kind_s, _, sid_s, unk_s, _ = islands.build("trammel")
    col_o, kind_o, _, sid_o, unk_o, (ux, uy) = islands.build("sos")
    unk_blk = np.zeros((BW, BH), dtype=np.int32)
    np.add.at(unk_blk, (ux[unk_o] // 8, uy[unk_o] // 8), 1)
    dry_s = (kind_s == 0).reshape(BW, 8, BH, 8).sum(axis=(1, 3))
    dry_o = (kind_o == 0).reshape(BW, 8, BH, 8).sum(axis=(1, 3))
    np.savez_compressed(NPZ, land=land_blk.astype(np.int16), add=add.astype(np.int32), rem=rem.astype(np.int32),
                        cnt_s=cnt_s.astype(np.int32), cnt_o=cnt_o.astype(np.int32), unk=unk_blk,
                        dry_s=dry_s.astype(np.int16), dry_o=dry_o.astype(np.int16))
    stat = (add + rem) > 0
    landd = land_blk > 0
    real_blocks = BW * BH
    # Only the part of the map that is a world: stock Trammel's dungeons and the rest live east of x 5120.
    summary = {
        "blocks": int(real_blocks),
        "blocksLandDiffer": int(landd.sum()),
        "blocksStaticsDiffer": int(stat.sum()),
        "blocksEitherDiffer": int((landd | stat).sum()),
        "blocksBothDiffer": int((landd & stat).sum()),
        "landTilesDiffer": int(land_cell.sum()),
        "landTiles": int(W * H),
        "staticsStock": int(len(ks)), "staticsSos": int(len(ko)),
        "staticsOnlyStock": int(len(only_s)), "staticsOnlySos": int(len(only_o)),
        "dryTilesStock": int((kind_s == 0).sum()), "dryTilesSos": int((kind_o == 0).sum()),
        "newDryTiles": int(((kind_s != 0) & (kind_o == 0)).sum()),
        "lostDryTiles": int(((kind_s == 0) & (kind_o != 0)).sum()),
        "sosStaticsWithArtStockLacks": int(unk_o.sum()), "stockStaticsWithArtStockLacks": int(unk_s.sum()),
        "unknownArtIds": sorted(set(int(v) for v in sid_o[unk_o]))[:200],
    }
    for half, (a, b) in {"west of x 5120 (the surface)": (0, 640), "x 5120 and east (dungeons, staff areas)": (640, BW)}.items():
        summary["blocksEitherDiffer " + half] = int((landd | stat)[a:b].sum())
        summary["blocks " + half] = int((b - a) * BH)
    json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != "unknownArtIds"}, indent=1))
    # Overviews at 1/4 (1792 x 1024) and the change map at 1/4 with blocks painted.
    for name, col in (("stock-overview.png", col_s), ("sos-overview.png", col_o)):
        im = Image.fromarray(col[::4, ::4].transpose(1, 0, 2).copy())
        im.save(os.path.join(ART, name), optimize=True)
    base = (col_s[::4, ::4].astype(np.float32) * 0.35 + 40).astype(np.uint8).transpose(1, 0, 2).copy()
    paint = np.zeros((BW, BH, 3), dtype=np.uint8)
    newdry = (dry_o - dry_s) > 16
    lostdry = (dry_s - dry_o) > 16
    m_both = landd & stat
    paint[stat & ~landd] = (240, 200, 40)
    paint[landd & ~stat] = (60, 140, 255)
    paint[m_both] = (230, 60, 60)
    paint[newdry] = (60, 220, 90)
    paint[lostdry] = (180, 80, 230)
    painted = (landd | stat | newdry | lostdry)
    big = np.repeat(np.repeat(paint, 2, axis=0), 2, axis=1).transpose(1, 0, 2)
    pm = np.repeat(np.repeat(painted, 2, axis=0), 2, axis=1).T
    base[pm] = big[pm]
    im = Image.fromarray(base)
    d = ImageDraw.Draw(im)
    legend = [((230, 60, 60), "land and statics differ"), ((60, 140, 255), "land only"), ((240, 200, 40), "statics only"),
              ((60, 220, 90), "new dry land (was water or void)"), ((180, 80, 230), "dry land gone (now water or void)")]
    for i, (c, t) in enumerate(legend):
        d.rectangle([10, 10 + i * 18, 24, 24 + i * 18], fill=c)
        d.text((30, 10 + i * 18), t, fill=(255, 255, 255))
    d.text((10, 10 + len(legend) * 18 + 4), "SoS 3.0 vs stock Trammel, one 2x2 px square per 8x8 block; grey = identical", fill=(255, 255, 255))
    for gx in range(0, W, 512):
        d.text((gx // 4 + 2, H // 4 - 12), str(gx), fill=(160, 160, 160))
    for gy in range(0, H, 512):
        d.text((2, gy // 4 + 2), str(gy), fill=(160, 160, 160))
    im.save(os.path.join(ART, "change-map.png"), optimize=True)


def load():
    return dict(np.load(NPZ))


def changed_mask(b, min_statics=1):
    return (b["land"] > 0) | ((b["add"] + b["rem"]) >= min_statics)


def parse_spots():
    """Author go-menu spots from notes\\sos-map-author-spots.md: (group, name, x, y, z)."""
    out, group = [], ""
    for line in open(os.path.join(NOTES, "sos-map-author-spots.md"), encoding="utf-8"):
        if line.startswith("## Named regions"):
            break
        if line.startswith("### "):
            group = line[4:].strip()
        m = re.match(r"^- (.+?): (-?\d+), (-?\d+), (-?\d+)\s*$", line)
        if m and group:
            out.append((group, m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))))
    return out


def around(b, x, y, r=8):
    """Changed land tiles, statics added, removed in the blocks within r tiles of x, y."""
    x1, x2 = max(0, (x - r) // 8), min(BW - 1, (x + r) // 8)
    y1, y2 = max(0, (y - r) // 8), min(BH - 1, (y + r) // 8)
    s = (slice(x1, x2 + 1), slice(y1, y2 + 1))
    return int(b["land"][s].sum()), int(b["add"][s].sum()), int(b["rem"][s].sum()), int(b["cnt_s"][s].sum()), int(b["cnt_o"][s].sum())


def spots():
    b = load()
    rows = []
    for g, n, x, y, z in parse_spots():
        land, add, rem, cs, co = around(b, x, y)
        if x >= W or y >= H:
            verdict = "off map"
        elif land == 0 and add == 0 and rem == 0:
            verdict = "stock"
        elif add > 0.5 * max(co, 1) or land > 64:
            verdict = "new or rebuilt"
        else:
            verdict = "touched"
        rows.append([g, n, x, y, z, verdict, land, add, rem, cs, co])
    with open(os.path.join(OUT, "spots.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["group", "name", "x", "y", "z", "verdict", "landTilesChanged", "staticsAdded", "staticsRemoved", "staticsStock", "staticsSos"])
        w.writerows(rows)
    print(collections.Counter(r[5] for r in rows))
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        by[r[0].split(" / ")[1] if " / " in r[0] else r[0]][r[5]] += 1
    for k, v in by.items():
        print(k, dict(v))


def areas(min_blocks=4):
    """Connected areas of changed blocks (8-connected on the block grid, after closing gaps of one block)."""
    b = load()
    m = changed_mask(b)
    grown = m.copy()
    grown[1:, :] |= m[:-1, :]; grown[:-1, :] |= m[1:, :]; grown[:, 1:] |= m[:, :-1]; grown[:, :-1] |= m[:, 1:]
    lab = np.zeros(m.shape, dtype=np.int32)
    n = 0
    for (i, j) in zip(*np.nonzero(grown)):
        if lab[i, j]:
            continue
        n += 1
        st = [(i, j)]
        lab[i, j] = n
        while st:
            a, c = st.pop()
            for da in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    p, q = a + da, c + dc
                    if 0 <= p < BW and 0 <= q < BH and grown[p, q] and not lab[p, q]:
                        lab[p, q] = n
                        st.append((p, q))
    sp = parse_spots()
    rows = []
    for k in range(1, n + 1):
        sel = (lab == k) & m
        nb = int(sel.sum())
        if nb < min_blocks:
            continue
        xs, ys = np.nonzero(sel)
        x1, x2, y1, y2 = int(xs.min()) * 8, int(xs.max()) * 8 + 7, int(ys.min()) * 8, int(ys.max()) * 8 + 7
        names = sorted({s[1] if s[0].endswith(s[1]) else s[0].split(" / ")[-1] + ": " + s[1]
                        for s in sp if x1 <= s[2] <= x2 and y1 <= s[3] <= y2})
        rows.append([nb, x1, y1, x2, y2, int(b["land"][sel].sum()), int(b["add"][sel].sum()), int(b["rem"][sel].sum()),
                     int((b["dry_o"][sel].astype(int) - b["dry_s"][sel]).sum()), int(b["unk"][sel].sum()),
                     "; ".join(names)[:400]])
    rows.sort(key=lambda r: -r[0])
    with open(os.path.join(OUT, "areas.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["blocks", "x1", "y1", "x2", "y2", "landTilesChanged", "staticsAdded", "staticsRemoved", "dryTilesGained", "unknownArtStatics", "authorSpotsInside"])
        w.writerows(rows)
    print(len(rows), "areas of", min_blocks, "or more blocks;", sum(r[0] for r in rows), "blocks in them")
    for r in rows[:40]:
        print(r[:10], r[10][:120])


def regions():
    """Every stock Trammel region in pinned regions.json: how much of its area changed."""
    b = load()
    m = changed_mask(b)
    data = json.load(open(os.path.join(islands.PINNED, "regions.json")))
    rows = []
    for r in data:
        if r.get("Map") != "Trammel":
            continue
        tiles = changed = 0
        for a in r.get("Area", []):
            x1, y1 = a["x1"], a["y1"]
            x2, y2 = a["x2"], a["y2"]
            bx1, bx2, by1, by2 = max(0, x1 // 8), min(BW - 1, x2 // 8), max(0, y1 // 8), min(BH - 1, y2 // 8)
            if bx2 < bx1 or by2 < by1:
                continue
            sub = m[bx1:bx2 + 1, by1:by2 + 1]
            tiles += sub.size
            changed += int(sub.sum())
        rows.append([r.get("$type", ""), r.get("Name", ""), tiles, changed, round(100.0 * changed / tiles, 1) if tiles else 0])
    with open(os.path.join(OUT, "stock-regions.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["type", "name", "blocks", "blocksChanged", "percentChanged"])
        w.writerows(rows)
    for r in sorted(rows, key=lambda r: -r[4]):
        print(r)


def points(path):
    """A CSV with columns name,x,y (any extra columns kept): adds the change around each point."""
    b = load()
    rows = list(csv.reader(open(path, newline="", encoding="utf-8")))
    head, body = rows[0], rows[1:]
    ix, iy = head.index("x"), head.index("y")
    out = os.path.join(OUT, os.path.splitext(os.path.basename(path))[0] + "-checked.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(head + ["landTilesChanged", "staticsAdded", "staticsRemoved", "verdict"])
        for r in body:
            x, y = int(r[ix]), int(r[iy])
            land, add, rem, _, _ = around(b, x, y)
            w.writerow(r + [land, add, rem, "stock" if land == add == rem == 0 else "changed"])
    print(out)


def rect(x1, y1, x2, y2):
    b = load()
    s = (slice(x1 // 8, x2 // 8 + 1), slice(y1 // 8, y2 // 8 + 1))
    for k in ("land", "add", "rem", "cnt_s", "cnt_o", "dry_s", "dry_o", "unk"):
        print(k, int(b[k][s].sum()))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "blocks":
        blocks()
    elif cmd == "areas":
        areas(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    elif cmd == "spots":
        spots()
    elif cmd == "regions":
        regions()
    elif cmd == "points":
        points(sys.argv[2])
    elif cmd == "rect":
        rect(*(int(v) for v in sys.argv[2:6]))
