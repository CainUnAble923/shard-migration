r"""cc-P670 part 3: does each of Zigholtul's redrawn statics sit where the stock art does?

Read only. Stock art: art.mul/artidx.mul unpacked from the vanilla 7.0.117.0 client (MAPBUILD_ART), tiledata and
animdata from the client (MAPBUILD_CLIENT). The PNGs: the vendored copies (player-package\vendor\zigholtul-redrawn-statics\
art\<id>.png) or, before vendoring, any folder given as the first argument.

The client draws a static's image centred on its tile and standing on the tile's foot: x = tile x - (w >> 1) + 22,
y = tile y - h + 44 (ClassicUO's static and item views). So two images sit the same when, measured from that anchor
(image centre column w >> 1, bottom row h), their content's lowest row and its base (the opaque pixels of the bottom
four rows of content) start, end and centre in the same place. Content is alpha >= 16 in the PNG (TazUO clears fainter
alpha, FixPNGAlpha) and non-black in the stock art.

    python -P fit.py [<png folder>]   -> out\fit.csv, out\fit-summary.txt (printed)

Verdict per ID (the rules were set from renders of the real map, preview.py; first pass in the notes):
  ok          fits by its kind's rule:
                structural (tiledata Wall or Door, or a name with wall, door, window, arch, stair, floor, roof, post,
                  pillar, column): bottom within 1 px, base left, right and centre within 1 px
                a tree set (a run of trunk IDs, a tree, palm, cactus or other foliage piece, and the canopy IDs
                  after it: leaves, needles, blossoms, fronds): the whole set or none. The author redrew trees as
                  sets, fuller and about 1.7 times the stock size, with the trunk, its slices (a big tree is drawn
                  as 45 px columns on several tiles) and the crown matched to each other, not to stock; per-piece
                  numbers mean nothing for them. A set ships when every member the stock client has art for is in
                  the pack; the renders (preview-*.jpg, every redraw) show such sets standing on their tiles. A set
                  with any member missing is left out whole: mixing a redrawn trunk with a stock crown, or a few
                  redrawn columns of a big tree, is exactly what looks crooked (the first pass's preview-orchard.jpg
                  and preview-yew-trees.jpg, "only those that fit"). A blank PNG in a set (3449, 3455) is the author
                  hiding a stock slice his fuller tree covers, and ships with its set
                anything else: bottom within 2 px, base centre within 4 px
  shifted     outside its kind's rule: would stand off its tile or float: left out of the package
  water       a water static: left out whatever its fit; the redraws are another blue than stock water land, so the
              sea draws as a patchwork of squares (preview-yew-forest.jpg)
  partial set a tree set the pack covers only in part: left out whole
  no stock    the stock client has no art for the ID (nothing to redraw): left out
  ours        the ID is in our own art registry (registry.csv) or a UI skin's target: left out, ours wins
  animated    an animated static (tiledata Animation flag) whose animdata frames are not all redrawn: left out, or
              the animation would flicker between two styles
Structural pieces (tiledata Wall, Door, or a name with wall, door, window, arch, stair, floor, roof) are held to
1 px on the base; everything else to 2 px.
"""
import csv
import os
import re
import struct
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
DOCS = os.path.dirname(NOTES)
sys.path.insert(0, os.path.join(DOCS, "scripts"))
from mapbuild import isorender, uofiles  # noqa: E402

SL = r"D:\UO\golems\Iron\ShatteredLegacy"
VENDOR = os.path.join(SL, "player-package", "vendor", "zigholtul-redrawn-statics", "art")
CLIENT = os.environ.get("MAPBUILD_CLIENT", r"D:\UO\UltimaOnlineVanilla")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

WALL, DOOR, ANIMATION, LIGHT = 0x10, 0x20000000, 0x01000000, 0x00800000
STRUCT_WORDS = re.compile(r"wall|door|window|arch|stair|floor|roof|post|pillar|column", re.I)


FOLIAGE = 0x00020000
CANOPY_WORDS = re.compile(r"leaves|needles|blossom|frond|foliage|branches", re.I)
TRUNK_WORDS = re.compile(r"tree|palm|cactus|trunk|log|stump|bamboo", re.I)


def kind_of(name, flags, structural):
    n = name or ""
    if re.search(r"\bwater\b", n, re.I) and not re.search(r"waterfall", n, re.I):
        return "water"
    if structural:
        return "structural"
    if CANOPY_WORDS.search(n):
        return "canopy"
    if TRUNK_WORDS.search(n) or flags & FOLIAGE:
        return "trunk"
    return "other"


def content(a):
    """(bottom, base_left, base_right) of an RGBA array's content, or None. bottom = rows below the lowest content
    row; base = the bottom four content rows."""
    mask = a[:, :, 3] >= 16
    rows = np.nonzero(mask.any(axis=1))[0]
    if not len(rows):
        return None
    low = rows[-1]
    base = mask[max(0, low - 3):low + 1].any(axis=0)
    cols = np.nonzero(base)[0]
    return a.shape[0] - 1 - low, int(cols[0]), int(cols[-1])


def stock_rgba(art, tid):
    im = art.static(tid)
    if im is None:
        return None
    a = np.array(im.convert("RGBA"))
    # The stock reader marks colour 0 transparent already; keep its alpha as is (translucent items are 150).
    return a


def animdata_frames(client):
    d = open(os.path.join(client, "animdata.mul"), "rb").read()

    def frames(tid):
        off = (tid >> 3) * (4 + 8 * 68) + 4 + (tid & 7) * 68
        if off + 68 > len(d):
            return []
        fr = struct.unpack_from("<64b", d, off)
        count = d[off + 65]
        return [tid + fr[i] for i in range(min(count, 64))]
    return frames


def registry_ids():
    ids = set()
    p = os.path.join(SL, "player-package", "vendor", "shattered-legacy-art", "registry.csv")
    for line in open(p, encoding="utf-8"):
        m = re.match(r"^\s*(\d+)\s*,", line)
        if m:
            ids.add(int(m.group(1)))
    # UI skins: the scroll skin remaps item IDs 7981-8044 (patch 0005's SlSkins table); their targets are ours too.
    skins = open(os.path.join(SL, "client", "patches", "0005-ui-skins-appearance.patch"), encoding="utf-8").read()
    for a, b in re.findall(r"\[(\d+)\] = (\d+)", skins[skins.index('"scroll", "magic-scrolls"'):]):
        ids.add(int(a))
        ids.add(int(b))
    return ids


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else VENDOR
    art = isorender.Art()
    _, items = uofiles.read_tiledata(CLIENT)
    frames = animdata_frames(CLIENT)
    ours = registry_ids()
    pngs = {int(f[:-4]): os.path.join(folder, f) for f in os.listdir(folder) if re.fullmatch(r"\d+\.png", f)}
    covered = set(pngs)
    rows = []
    for tid in sorted(pngs):
        t = items[tid] if tid < len(items) else {"flags": 0, "height": 0, "name": ""}
        flags, name = t["flags"], t.get("name", "")
        structural = bool(flags & (WALL | DOOR)) or bool(STRUCT_WORDS.search(name or ""))
        im = Image.open(pngs[tid]).convert("RGBA")
        a = np.array(im)
        s = stock_rgba(art, tid)
        row = dict(id=tid, hex="0x%04X" % tid, name=name, height=t.get("height", 0), structural=structural,
                   wall=bool(flags & WALL), door=bool(flags & DOOR), light=bool(flags & LIGHT), animated=bool(flags & ANIMATION),
                   pngW=im.width, pngH=im.height, stockW="", stockH="", dBottom="", dLeft="", dRight="", dCentre="", kind="", set="", verdict="")
        if tid in ours:
            row["verdict"] = "ours"
        elif s is None:
            row["verdict"] = "no stock"
        else:
            row["stockW"], row["stockH"] = s.shape[1], s.shape[0]
            cp, cs = content(a), content(s)
            if cp is None and kind_of(name, flags, structural) in ("trunk", "canopy"):
                # A blank slice of a tree set: the author hides that stock piece because his fuller tree covers it.
                row["kind"] = kind_of(name, flags, structural)
                row["verdict"] = "tree"
            elif cp is None or cs is None:
                row["verdict"] = "shifted"
            else:
                hp, hs = a.shape[1] >> 1, s.shape[1] >> 1
                db = cp[0] - cs[0]
                dl, dr = (cp[1] - hp) - (cs[1] - hs), (cp[2] - hp) - (cs[2] - hs)
                dc = ((cp[1] + cp[2]) / 2 - hp) - ((cs[1] + cs[2]) / 2 - hs)
                row.update(dBottom=db, dLeft=dl, dRight=dr, dCentre=round(dc, 1))
                kind = kind_of(name, flags, structural)
                row["kind"] = kind
                if kind == "water":
                    row["verdict"] = "water"
                elif kind == "structural":
                    good = abs(db) <= 1 and abs(dl) <= 1 and abs(dr) <= 1 and abs(dc) <= 1
                    row["verdict"] = "ok" if good else "shifted"
                elif kind in ("trunk", "canopy"):
                    row["verdict"] = "tree"
                else:
                    row["verdict"] = "ok" if abs(db) <= 2 and abs(dc) <= 4 else "shifted"
            if row["verdict"] == "ok" and row["animated"]:
                fr = frames(tid)
                missing = [f for f in fr if f not in covered]
                if missing:
                    row["verdict"] = "animated"
                    row["name"] = (name or "") + " (frames not redrawn: " + ",".join(str(m) for m in missing[:6]) + ")"
        rows.append(row)
    # Tree sets over every stock ID (not only the redrawn ones): a run of trunks, then the canopies after it.
    sets, cur, phase = [], [], None
    for tid in range(0x4000):
        t2 = items[tid] if tid < len(items) else {"flags": 0, "name": ""}
        k = kind_of(t2.get("name", ""), t2["flags"], False) if art.static(tid) is not None else None
        if k not in ("trunk", "canopy"):
            if cur:
                sets.append(cur)
            cur, phase = [], None
            continue
        if k == "trunk" and phase == "canopy":
            sets.append(cur)
            cur = []
        cur.append(tid)
        phase = k
    if cur:
        sets.append(cur)
    by = {r["id"]: r for r in rows}
    for s in sets:
        mine = [by[i] for i in s if i in by and by[i]["verdict"] == "tree"]
        if not mine:
            continue
        whole = all(i in covered for i in s)
        for r in mine:
            r["verdict"] = "ok" if whole else "partial set"
            r["set"] = "%d-%d" % (s[0], s[-1])
    with open(os.path.join(OUT, "fit.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    c = Counter(r["verdict"] for r in rows)
    lines = ["%d PNGs; %s" % (len(rows), dict(c)),
             "size same as stock: %d; larger: %d; smaller: %d" % (
                 sum(1 for r in rows if r["stockW"] != "" and (r["pngW"], r["pngH"]) == (r["stockW"], r["stockH"])),
                 sum(1 for r in rows if r["stockW"] != "" and r["pngW"] * r["pngH"] > r["stockW"] * r["stockH"]),
                 sum(1 for r in rows if r["stockW"] != "" and r["pngW"] * r["pngH"] < r["stockW"] * r["stockH"])),
             "structural: %d (ok %d); light sources %d; animated %d" % (
                 sum(r["structural"] for r in rows), sum(1 for r in rows if r["structural"] and r["verdict"] == "ok"),
                 sum(r["light"] for r in rows), sum(r["animated"] for r in rows))]
    open(os.path.join(OUT, "fit-summary.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
