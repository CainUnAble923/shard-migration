r"""cc-P481 (Chase 10-25 20:12-20:24): find the islands the Wakening Isle could use, on the stock facets and on the
downloaded custom maps, and render them.

For each map: the land (stock: mapNLegacyMUL.uop from the vanilla 7.0.117.0 client; downloaded: the author's mapN.mul,
copied as data only into scratch\), the statics (staidx/statics .mul), and a radar colour per tile (radarcol.mul: the
topmost static's colour, else the land's). A tile is
  water  when its land tile or its topmost static is Wet in tiledata,
  void   when its land is void (0x0244) or NoDraw (0x0002) and nothing stands on it,
  dry    otherwise.
Islands are the connected dry patches on a 4 x 4 tile grid (a coarse cell is dry when at least half its tiles are),
4-connected, so sizes are good to about 4 tiles. Each is tagged with what borders it (water or void: a void-bordered
patch is a dungeon, a cave or a staff area, not an island), the pinned regions it touches (Distribution/Data/
regions.json; stock maps only) and the teleporters that land on it (teleporters.json).

Read only. Nothing here is shipped or run from D:\\UO\\third-party.
    python -P islands.py survey <map> [--min 400] [--max 90000]   -> scratch\\<map>-islands.csv, scratch\\<map>-overview.png
    python -P islands.py crop <map> <x1> <y1> <x2> <y2> <scale> <out.png>
maps: trammel felucca ilshenar malas tokuno termur sos dungeon4 termur-repl paranoia
"""
import collections
import csv
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))
from mapbuild import uofiles  # noqa: E402

VANILLA = r"D:\UO\UltimaOnlineVanilla"
PINNED = r"D:\UO\ModernUO-pinned\Distribution\Data"
SCRATCH = os.path.join(HERE, "scratch")
os.makedirs(SCRATCH, exist_ok=True)

# name: (kind, folder, file index or (map, staidx, statics) names, width, height, regions.json map name)
MAPS = {
    "felucca": ("uop", VANILLA, 0, 7168, 4096, "Felucca"),
    "trammel": ("uop", VANILLA, 1, 7168, 4096, "Trammel"),
    "ilshenar": ("uop", VANILLA, 2, 2304, 1600, "Ilshenar"),
    "malas": ("uop", VANILLA, 3, 2560, 2048, "Malas"),
    "tokuno": ("uop", VANILLA, 4, 1448, 1448, "Tokuno"),
    "termur": ("uop", VANILLA, 5, 1280, 4096, "TerMur"),
    "sos": ("mul", os.path.join(SCRATCH, "sos"), ("Map1.mul", "Staidx1.mul", "Statics1.mul"), 7168, 4096, None),
    "dungeon4": ("mul", os.path.join(SCRATCH, "dungeon4"), ("map4.mul", "staidx4.mul", "statics4.mul"), 1448, 1448, None),
    "termur-repl": ("mul", os.path.join(SCRATCH, "termur-repl"), ("map5.mul", "staidx5.mul", "statics5.mul"), 1280, 4096, None),
    "paranoia": ("mul", os.path.join(SCRATCH, "paranoia"), ("Map0.mul", "Staidx0.mul", "Statics0.mul"), 6144, 4096, None),
}

COARSE = 4
VOID_IDS = (0x0244, 0x0002)


def load_land(name):
    kind, folder, files, w, h, _ = MAPS[name]
    if kind == "uop":
        return uofiles.load_land(folder, files)
    raw = open(os.path.join(folder, files[0]), "rb").read()
    bw, bh = w >> 3, h >> 3
    n = bw * bh
    assert len(raw) == n * 196, (name, len(raw), n * 196)
    arr = np.frombuffer(raw, dtype=np.uint8).reshape(n, 196)
    cells = arr[:, 4:].reshape(n, 64, 3)
    ids = cells[:, :, 0].astype(np.uint16) | (cells[:, :, 1].astype(np.uint16) << 8)
    zs = cells[:, :, 2].view(np.int8)
    # As uofiles.load_land: [bx][by][cy][cx] -> ids[x, y].
    ids = ids.reshape(bw, bh, 8, 8).transpose(0, 3, 1, 2).reshape(w, h)
    zs = zs.reshape(bw, bh, 8, 8).transpose(0, 3, 1, 2).reshape(w, h)
    return ids, zs


def load_statics(name):
    """Arrays x, y, z, id of every static."""
    kind, folder, files, w, h, _ = MAPS[name]
    if kind == "uop":
        ip, sp = os.path.join(folder, "staidx%d.mul" % files), os.path.join(folder, "statics%d.mul" % files)
    else:
        ip, sp = os.path.join(folder, files[1]), os.path.join(folder, files[2])
    idx = np.frombuffer(open(ip, "rb").read(), dtype="<i4").reshape(-1, 3)
    sta = np.frombuffer(open(sp, "rb").read(), dtype=np.uint8)
    bh = h >> 3
    nb = min(len(idx), (w >> 3) * bh)
    look, ln = idx[:nb, 0].astype(np.int64), idx[:nb, 1].astype(np.int64)
    ok = (look >= 0) & (ln >= 7) & (look + ln <= len(sta))
    blocks = np.nonzero(ok)[0]
    counts = ln[ok] // 7
    total = int(counts.sum())
    starts = np.repeat(look[ok], counts)
    within = np.arange(total) - np.repeat(np.cumsum(counts) - counts, counts)
    off = starts + within * 7
    rows = sta[off[:, None] + np.arange(7)]
    tid = rows[:, 0].astype(np.int64) | (rows[:, 1].astype(np.int64) << 8)
    blk = np.repeat(blocks, counts)
    x = (blk // bh) * 8 + rows[:, 2]
    y = (blk % bh) * 8 + rows[:, 3]
    z = rows[:, 4].view(np.int8).astype(np.int64)
    keep = (rows[:, 2] < 8) & (rows[:, 3] < 8)
    return x[keep], y[keep], z[keep], tid[keep]


def radar_colours():
    raw = np.frombuffer(open(os.path.join(VANILLA, "radarcol.mul"), "rb").read(), dtype="<u2")
    c = raw.astype(np.int64)
    rgb = np.stack([((c >> 10) & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, (c & 31) * 255 // 31], axis=1)
    return rgb.astype(np.uint8)


def flags():
    land, items = uofiles.read_tiledata(VANILLA)
    lf = np.array([f for f, _, _ in land], dtype=np.uint64)
    itf = np.array([i["flags"] for i in items], dtype=np.uint64)
    return lf, itf


def build(name):
    """colour[x, y, 3], kind[x, y] (0 dry, 1 water, 2 void), statics count per tile, unknown-art statics count."""
    kind, folder, files, w, h, _ = MAPS[name]
    ids, zs = load_land(name)
    sx, sy, sz, sid = load_statics(name)
    rad = radar_colours()
    lf, itf = flags()
    wet = int(uofiles.WET)
    colour = rad[ids.astype(np.int64)]
    land_wet = (lf[ids.astype(np.int64)] & np.uint64(wet)) != 0
    void = np.isin(ids, VOID_IDS)
    # The topmost static per tile.
    key = sx * h + sy
    order = np.lexsort((sz, key))
    key_s = key[order]
    last = np.ones(len(key_s), dtype=bool)
    last[:-1] = key_s[1:] != key_s[:-1]
    top = order[last]
    tx, ty, tt = sx[top], sy[top], sid[top]
    colour[tx, ty] = rad[0x4000 + np.minimum(tt, 0xBFFF)]
    top_wet = np.zeros((w, h), dtype=bool)
    top_wet[tx, ty] = (itf[np.minimum(tt, len(itf) - 1)] & np.uint64(wet)) != 0
    has_static = np.zeros((w, h), dtype=bool)
    has_static[tx, ty] = True
    k = np.zeros((w, h), dtype=np.uint8)
    k[land_wet | top_wet] = 1
    k[void & ~has_static] = 2
    count = np.zeros((w, h), dtype=np.int32)
    np.add.at(count, (sx, sy), 1)
    # Art the stock client may not have: an item id past the vanilla tiledata, or a tile with no name and no flags.
    unknown = (sid >= len(itf))
    named = np.array([bool(i["name"]) or bool(i["flags"]) for i in uofiles.read_tiledata(VANILLA)[1]], dtype=bool)
    unknown |= ~named[np.minimum(sid, len(named) - 1)]
    return colour, k, count, sid, unknown, (sx, sy)


def regions_for(name):
    rmap = MAPS[name][5]
    if not rmap:
        return []
    out = []
    for r in json.load(open(os.path.join(PINNED, "regions.json"), encoding="utf-8")):
        if r.get("Map") != rmap:
            continue
        for a in r.get("Area", []):
            out.append((r.get("Name") or r.get("$type"), r.get("$type"), a["x1"], a["y1"], a["x2"], a["y2"]))
    return out


def teleporters_for(name):
    rmap = MAPS[name][5]
    if not rmap:
        return []
    out = []
    try:
        data = json.load(open(os.path.join(PINNED, "teleporters.json"), encoding="utf-8"))
    except OSError:
        return out
    for t in data:
        for end in ("src", "dst"):   # {"src": {"map": "Felucca", "loc": [x, y, z]}, "dst": {...}, "back": bool}
            p = t.get(end)
            if p and p.get("map") == rmap:
                out.append((int(p["loc"][0]), int(p["loc"][1])))
    return out


def components(k):
    """Coarse dry components: list of dicts with bbox (tiles), dry area (coarse cells x 16), borders."""
    w, h = k.shape
    cw, ch = w // COARSE, h // COARSE
    kk = k[:cw * COARSE, :ch * COARSE].reshape(cw, COARSE, ch, COARSE)
    dry = (kk == 0).sum(axis=(1, 3)) >= (COARSE * COARSE) // 2
    wat = (kk == 1).sum(axis=(1, 3))
    vd = (kk == 2).sum(axis=(1, 3))
    label = np.full((cw, ch), -1, dtype=np.int32)
    comps = []
    for cx0, cy0 in zip(*np.nonzero(dry)):
        if label[cx0, cy0] >= 0:
            continue
        cid = len(comps)
        q = collections.deque([(cx0, cy0)])
        label[cx0, cy0] = cid
        n = 0
        x1 = x2 = cx0
        y1 = y2 = cy0
        bw = bv = 0
        edge = False
        while q:
            cx, cy = q.popleft()
            n += 1
            x1, x2, y1, y2 = min(x1, cx), max(x2, cx), min(y1, cy), max(y2, cy)
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if nx < 0 or ny < 0 or nx >= cw or ny >= ch:
                    edge = True
                    continue
                if dry[nx, ny]:
                    if label[nx, ny] < 0:
                        label[nx, ny] = cid
                        q.append((nx, ny))
                else:
                    if wat[nx, ny] >= vd[nx, ny]:
                        bw += 1
                    else:
                        bv += 1
        comps.append(dict(id=cid, cells=n, area=n * COARSE * COARSE, x1=x1 * COARSE, y1=y1 * COARSE,
                          x2=x2 * COARSE + COARSE - 1, y2=y2 * COARSE + COARSE - 1, water=bw, void=bv, edge=edge))
    return comps, label


def survey(name, lo=400, hi=90000):
    colour, k, count, sid, unknown, (sx, sy) = build(name)
    w, h = k.shape
    comps, label = components(k)
    regs = regions_for(name)
    tps = teleporters_for(name)
    rows = []
    for c in comps:
        if not (lo <= c["area"] <= hi):
            continue
        border = c["water"] + c["void"]
        kind = "island" if border and c["water"] / border >= 0.8 else ("void-bordered" if border and c["void"] / border >= 0.8 else "mixed")
        x1, y1, x2, y2 = c["x1"], c["y1"], c["x2"], c["y2"]
        inside = (sx >= x1) & (sx <= x2) & (sy >= y1) & (sy <= y2)
        nst = int(inside.sum())
        nunk = int((inside & unknown).sum())
        touch = sorted({r[0] for r in regs if not (r[4] < x1 or r[2] > x2 or r[5] < y1 or r[3] > y2)})
        ntp = sum(1 for (tx, ty) in tps if x1 <= tx <= x2 and y1 <= ty <= y2)
        rows.append(dict(map=name, id=c["id"], kind=kind, x1=x1, y1=y1, x2=x2, y2=y2, w=x2 - x1 + 1, h=y2 - y1 + 1,
                         dry_tiles=c["area"], statics=nst, unknown_art=nunk, teleporters=ntp,
                         regions="; ".join(touch)))
    rows.sort(key=lambda r: (r["kind"] != "island", -r["dry_tiles"]))
    path = os.path.join(SCRATCH, "%s-islands.csv" % name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["map"])
        wr.writeheader()
        wr.writerows(rows)
    # Overview: one pixel per 4 tiles, islands boxed and numbered.
    s = 4 if w > 3000 else 2
    img = Image.fromarray(colour[::s, ::s].transpose(1, 0, 2).copy())
    d = ImageDraw.Draw(img)
    fnt = font(12)
    for r in rows:
        if r["kind"] != "island":
            continue
        col = (255, 60, 60) if not r["regions"] and not r["teleporters"] else (255, 210, 0)
        d.rectangle([r["x1"] // s, r["y1"] // s, r["x2"] // s, r["y2"] // s], outline=col)
        d.text((r["x2"] // s + 2, r["y1"] // s), str(r["id"]), fill=col, font=fnt)
    img.save(os.path.join(SCRATCH, "%s-overview.png" % name))
    print("%s: %d candidates (%d islands), csv %s" % (name, len(rows), sum(r["kind"] == "island" for r in rows), path))
    return rows


def font(size):
    for p in (r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def crop(name, x1, y1, x2, y2, scale, out):
    colour, k, count, sid, unknown, _ = build(name)
    sub = colour[x1:x2 + 1, y1:y2 + 1].transpose(1, 0, 2).copy()
    img = Image.fromarray(sub).resize(((x2 - x1 + 1) * scale, (y2 - y1 + 1) * scale), Image.NEAREST)
    img.save(out)
    print("wrote", out, img.size)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "survey":
        args = sys.argv[2:]
        lo = int(args[args.index("--min") + 1]) if "--min" in args else 400
        hi = int(args[args.index("--max") + 1]) if "--max" in args else 90000
        survey(args[0], lo, hi)
    elif cmd == "crop":
        n, a, b, c, dd, sc, o = sys.argv[2:9]
        crop(n, int(a), int(b), int(c), int(dd), int(sc), o)
