"""The junction sheet (cc-P185; notes/map-building-playbook.md section 4): every wall end, L-corner, T-junction,
cross, mixed-set join, wall-to-rock join and mounted wall item of a build, found from the wall layer and cropped from
a render at full size with its coordinates, in grids of 48 (junctions-1.png, junctions-2.png, ...). The builder
reviews every crop before a render goes to Chase, and the notes say how many crops were checked and what was fixed.

    find_junctions(wall_tiles, rock_tiles, statics)  -> [dict(kind, x, y, role, set, note)]
    sheets(folder, junctions, out_prefix, art=None)  -> [(path, count)]

wall_tiles: {(x, y): wallSetName} for every tile carrying an item wall (ring tiles and walled pillars);
rock_tiles: the cave ring tiles (rock); statics: [(x, y, z, id, why)] of the build (for the mounted items).
"""
import collections, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mapbuild import walls as W  # noqa: E402

MOUNTS = set(range(0x09FB, 0x0A0F))          # wall sconces, torches and torch holders (tiledata names)
ORTH = ((0, -1, "N"), (1, 0, "E"), (0, 1, "S"), (-1, 0, "W"))


def find_junctions(wall_tiles, rock_tiles, statics):
    Wt = lambda c: c in wall_tiles
    rock = set(rock_tiles)
    out = []
    for (x, y) in sorted(wall_tiles):
        nb = {d: (x + a, y + b) for a, b, d in ORTH}
        w = {d: Wt(c) for d, c in nb.items()}
        n = sum(w.values())
        role = W.wall_role(Wt, x, y)
        st = wall_tiles[(x, y)]
        if n == 1:
            kind = "end"
        elif n == 2 and not ((w["N"] and w["S"]) or (w["E"] and w["W"])):
            kind = "L"
        elif n == 3:
            kind = "T"
        elif n == 4:
            kind = "cross"
        elif n == 0:
            kind = "lone"
        else:
            kind = None
        if kind:
            out.append(dict(kind=kind, x=x, y=y, role=role, set=st, note="walls " + "".join(d for d in "NESW" if w[d])))
        # a wall-to-rock join: a free end, an L or a lone tile with cave rock on a side no wall continues to (a wall
        # merely running along a cave ring, two opposite wall neighbours, is not a junction)
        rocks = [d for d, c in nb.items() if c in rock and not w[d]] if kind in ("end", "L", "lone") else []
        if rocks:
            out.append(dict(kind="rock", x=x, y=y, role=role, set=st, note="rock " + "".join(rocks)))
        for d, c in nb.items():
            if c in wall_tiles and wall_tiles[c] != st and d in ("E", "S"):
                out.append(dict(kind="mixed", x=x, y=y, role=role, set=st, note="%s to %s %s" % (st, wall_tiles[c], d)))
    for s in statics:
        if s[3] in MOUNTS:
            out.append(dict(kind="mount", x=s[0], y=s[1], role="0x%04X z %d" % (s[3], s[2]), set="", note=str(s[4]) if len(s) > 4 else ""))
    return out


def summary(junctions):
    c = collections.Counter(j["kind"] for j in junctions)
    return ", ".join("%s %d" % kv for kv in sorted(c.items()))


def sheets(folder, junctions, out_prefix, art=None, per=48, cols=8, around=3, scale=0.8, fi=1):
    """Render a crop round every junction and lay them out in grids. Returns [(path, count)]."""
    from PIL import Image, ImageDraw
    from mapbuild import isorender
    from mapbuild.isorender import Scene, render, save, tile_px
    art = art or isorender.Art()
    crops = []
    for j in junctions:
        x, y = j["x"], j["y"]
        x1, y1, x2, y2 = x - around, y - around - 1, x + around, y + around
        sc = Scene.from_map(folder, fi, x1, y1, x2, y2)
        im = render(sc, x1, y1, x2, y2, art)
        d = ImageDraw.Draw(im)
        px, py = tile_px(im, x, y)
        d.polygon([(px, py), (px + 22, py + 22), (px, py + 44), (px - 22, py + 22)], outline=(255, 40, 40, 255))
        # trim the empty top (tall walls beyond the crop) to the drawn content
        bbox = im.convert("RGB").getbbox()
        if bbox:
            im = im.crop((0, max(0, bbox[1] - 4), im.width, im.height))
        if scale != 1.0:
            im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
        title = "%s %d,%d %s %s %s" % (j["kind"], x, y, j["set"], j["role"], j["note"])
        crops.append((title, im))
    out = []
    for k in range(0, len(crops), per):
        batch = crops[k:k + per]
        cw = max(im.width for t, im in batch)
        ch = max(im.height for t, im in batch) + 16
        rows = (len(batch) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (cw + 6) + 6, rows * (ch + 6) + 6), (40, 40, 44))
        d = ImageDraw.Draw(sheet)
        for i, (title, im) in enumerate(batch):
            r, c = divmod(i, cols)
            ox, oy = 6 + c * (cw + 6), 6 + r * (ch + 6)
            d.text((ox + 2, oy + 2), title, fill=(255, 230, 120))
            sheet.paste(im.convert("RGB"), (ox, oy + 16))
        path = "%s-%d.png" % (out_prefix, k // per + 1)
        size = save(sheet, path)
        out.append((path, len(batch), size))
    return out
