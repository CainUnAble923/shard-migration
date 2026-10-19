"""cc-P180: an isometric renderer that draws a map region, a house multi or a hand-made scene the way the classic
client lays tiles out, so renders can be judged for wall placement.

Why not vseUOAware's render_map_region: it anchored every static's art bottom at the land diamond's centre
(sy + 22 - height); the client anchors it at the diamond's bottom (ClassicUO View.cs: TILE_CENTER_OFFSET 22,
TILE_HEIGHT_OFFSET 44, applied as x -= width/2 - 22, y -= height - 44, with land drawn at (posX, posY)). Half a tile
of error moved every wall off its line in P167's renders. cc-P180 fixed vseUOAware's copy too (MapEditorTools.cs);
this module also draws sloped land, which vseUOAware does not (it drew flat art diamonds at each Z, leaving black
seams at every ring step).

Geometry (ClassicUO Land.UpdateZ / LandView.Draw, TazUO src/ClassicUO.Client/Game/GameObjects):
  screen x = (x - y) * 22, screen y = (x + y) * 22 - z * 4; the land diamond's corners are
  top (x,y), right (x+1,y), bottom (x+1,y+1), left (x,y+1), each at its own tile's Z; a tile whose four corners share
  one Z draws its 44x44 art diamond, otherwise the texmap of tiledata's TexID stretched over the four corners.
  A static's art is centred on the tile and bottom-aligned to the diamond bottom, raised by its Z.
Draw order: by x + y, land before statics, statics by Z. Hues are not applied (map statics carry none here).

    python -P isorender.py map <folder> <facet> x1 y1 x2 y2 out.png     (folder holds mapN uop, staticsN, staidxN)
    python -P isorender.py multi <multiId hex> <zmax> out.png            (components with z <= zmax; land = marble)
"""
import os, struct, sys, json
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, r'D:\UO\shard-migration\notes\cc-P36-tools')
import uodata  # noqa: E402

CLIENT = uodata.NEW                                   # tiledata, texmaps, multis: read only
ART_FOLDER = r'D:\UO\cc-p167-work\scratch-client'     # art.mul / artidx.mul unpacked by P167's uop2art.py
BH = 512
TRANSLUCENT = 1 << 3
FLAG_WALL = 1 << 4


def rgb555(px):
    return ((px >> 10 & 31) * 255 // 31, (px >> 5 & 31) * 255 // 31, (px & 31) * 255 // 31)


class Art:
    """Classic art.mul/artidx.mul, texmaps.mul/texidx.mul and tiledata, cached."""

    def __init__(self, art_folder=ART_FOLDER, client=CLIENT):
        self.idx = open(os.path.join(art_folder, 'artidx.mul'), 'rb').read()
        self.mul = open(os.path.join(art_folder, 'art.mul'), 'rb').read()
        self.tidx = open(os.path.join(client, 'texidx.mul'), 'rb').read()
        self.tmul = open(os.path.join(client, 'texmaps.mul'), 'rb').read()
        self.land_data, self.item_data = uodata.read_tiledata(client)
        self.cache = {}

    def static(self, tid):
        key = ('s', tid)
        if key in self.cache:
            return self.cache[key]
        look, ln, extra = struct.unpack_from('<iii', self.idx, (0x4000 + tid) * 12)
        im = None
        if look >= 0 and ln > 0:
            d = self.mul[look:look + ln]
            flag, w, h = struct.unpack_from('<IHH', d, 0)
            lut = struct.unpack_from('<%dH' % h, d, 8)
            base = 8 + 2 * h
            arr = np.zeros((h, w, 4), dtype=np.uint8)
            for y in range(h):
                p = base + lut[y] * 2
                x = 0
                while True:
                    xo, rl = struct.unpack_from('<HH', d, p)
                    p += 4
                    if xo == 0 and rl == 0:
                        break
                    x += xo
                    run = np.frombuffer(d, dtype='<u2', count=rl, offset=p)
                    p += 2 * rl
                    n = min(rl, w - x)
                    if n > 0:
                        seg = run[:n].astype(np.uint32)
                        arr[y, x:x + n, 0] = (seg >> 10 & 31) * 255 // 31
                        arr[y, x:x + n, 1] = (seg >> 5 & 31) * 255 // 31
                        arr[y, x:x + n, 2] = (seg & 31) * 255 // 31
                        arr[y, x:x + n, 3] = np.where(seg != 0, 255, 0)
                    x += rl
            im = Image.fromarray(arr, 'RGBA')
            if self.item_data[tid]['flags'] & TRANSLUCENT:
                a = np.array(im)
                a[:, :, 3] = (a[:, :, 3].astype(np.uint16) * 150 // 255).astype(np.uint8)
                im = Image.fromarray(a, 'RGBA')
        self.cache[key] = im
        return im

    def land(self, tid):
        key = ('l', tid)
        if key in self.cache:
            return self.cache[key]
        look, ln, extra = struct.unpack_from('<iii', self.idx, tid * 12)
        im = None
        if look >= 0 and ln > 0:
            d = self.mul[look:look + ln]
            arr = np.zeros((44, 44, 4), dtype=np.uint8)
            p = 0
            for y in range(44):
                n = (y + 1) * 2 if y < 22 else (44 - y) * 2
                x0 = 22 - n // 2
                run = np.frombuffer(d, dtype='<u2', count=n, offset=p).astype(np.uint32)
                p += 2 * n
                arr[y, x0:x0 + n, 0] = (run >> 10 & 31) * 255 // 31
                arr[y, x0:x0 + n, 1] = (run >> 5 & 31) * 255 // 31
                arr[y, x0:x0 + n, 2] = (run & 31) * 255 // 31
                arr[y, x0:x0 + n, 3] = 255
            im = Image.fromarray(arr, 'RGBA')
        self.cache[key] = im
        return im

    def texmap(self, texid):
        key = ('t', texid)
        if key in self.cache:
            return self.cache[key]
        im = None
        if texid > 0 and (texid + 1) * 12 <= len(self.tidx):
            look, ln, extra = struct.unpack_from('<iii', self.tidx, texid * 12)
            if look >= 0 and ln > 0:
                size = 64 if ln == 0x2000 else 128
                run = np.frombuffer(self.tmul, dtype='<u2', count=size * size, offset=look).astype(np.uint32)
                arr = np.zeros((size, size, 4), dtype=np.uint8)
                arr[:, :, 0] = ((run >> 10 & 31) * 255 // 31).reshape(size, size)
                arr[:, :, 1] = ((run >> 5 & 31) * 255 // 31).reshape(size, size)
                arr[:, :, 2] = ((run & 31) * 255 // 31).reshape(size, size)
                arr[:, :, 3] = 255
                im = Image.fromarray(arr, 'RGBA')
        self.cache[key] = im
        return im


class Scene:
    """land: {(x, y): (tileId, z)}; statics: [(x, y, z, tileId), ...]."""

    def __init__(self, land=None, statics=None):
        self.land = land or {}
        self.statics = statics or []

    @staticmethod
    def from_map(folder, fi, x1, y1, x2, y2, pad=1):
        """Read the rect (plus a pad for corner heights) from mapN LegacyMUL uop + staticsN/staidxN in folder."""
        name, w, h = uodata.FACETS[fi]
        bh = h >> 3
        path = os.path.join(folder, 'map%dLegacyMUL.uop' % fi)
        ver, ents, data, allents = uodata.uop_by_name(path, 'map%dlegacymul' % fi, '.dat', 0x14000, 8)
        starts = []
        pos = 0
        for i in sorted(ents):
            e = ents[i]
            starts.append((pos, pos + e['dl'], e['off'] + e['hl']))
            pos += e['dl']

        def block_offset(b):
            off = b * 196
            for s, e_, fo in starts:
                if s <= off < e_:
                    return fo + (off - s)
            raise ValueError(b)
        land = {}
        for bx in range((x1 - pad) >> 3, ((x2 + pad) >> 3) + 1):
            for by in range((y1 - pad) >> 3, ((y2 + pad) >> 3) + 1):
                if bx < 0 or by < 0 or bx >= (w >> 3) or by >= bh:
                    continue
                fo = block_offset(bx * bh + by) + 4
                for cy in range(8):
                    for cx in range(8):
                        x, y = bx * 8 + cx, by * 8 + cy
                        if x1 - pad <= x <= x2 + pad and y1 - pad <= y <= y2 + pad:
                            tid, z = struct.unpack_from('<Hb', data, fo + (cy * 8 + cx) * 3)
                            land[(x, y)] = (tid, z)
        idx, sta = uodata.load_statics_index(folder, fi)
        statics = []
        for bx in range(x1 >> 3, (x2 >> 3) + 1):
            for by in range(y1 >> 3, (y2 >> 3) + 1):
                for (tid, cx, cy, z, hue) in uodata.block_statics(idx, sta, bx * bh + by):
                    x, y = bx * 8 + cx, by * 8 + cy
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        statics.append((x, y, z, tid))
        return Scene(land, statics)

    @staticmethod
    def from_multi(mid, zmax=None, land_tile=0x0486, pad=2):
        """A house multi from MultiCollection.uop (pinned MultiData.LoadUOP's record layout), on flat land at Z 0."""
        import zlib
        ver, ents, data, allents = uodata.uop_by_name(os.path.join(CLIENT, 'MultiCollection.uop'), 'multicollection', '.bin', 0x2000, 6)
        e = ents[mid]
        d = data[e['off'] + e['hl']:e['off'] + e['hl'] + e['cl']]
        if e['flag'] == 1:
            d = zlib.decompress(d)
        count = struct.unpack_from('<I', d, 4)[0]
        p = 8
        statics = []
        for i in range(count):
            tid, x, y, z, fl = struct.unpack_from('<HhhhH', d, p)
            p += 10
            n = struct.unpack_from('<I', d, p)[0]
            p += 4 + 4 * n
            if zmax is None or z <= zmax:
                statics.append((x, y, z, tid))
        xs = [s[0] for s in statics]
        ys = [s[1] for s in statics]
        land = {(x, y): (land_tile, 0) for x in range(min(xs) - pad, max(xs) + pad + 2) for y in range(min(ys) - pad, max(ys) + pad + 2)}
        return Scene(land, statics)


def _perspective(src_pts, dst_pts):
    """PIL transform coefficients mapping dst -> src (8 unknowns, 4 point pairs)."""
    A, b = [], []
    for (sx, sy), (dx, dy) in zip(src_pts, dst_pts):
        A.append([dx, dy, 1, 0, 0, 0, -sx * dx, -sx * dy])
        A.append([0, 0, 0, dx, dy, 1, -sy * dx, -sy * dy])
        b += [sx, sy]
    M = np.array(A, dtype=float)
    if abs(np.linalg.det(M)) < 1e-9:
        return None   # a collapsed quad (a cliff whose corners fold over): the caller draws the flat art instead
    return np.linalg.solve(M, np.array(b, dtype=float))


def render(scene, x1, y1, x2, y2, art=None, margin=8, background=(0, 0, 0, 255), shade=True):
    """Draw the tiles x1..x2, y1..y2 of the scene. Returns a PIL RGBA image."""
    art = art or Art()
    land = scene.land
    zs = lambda c, d: land[c][1] if c in land else d
    draws = []   # (x + y, layer, z, left, top, image)
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if (x, y) not in land:
                continue
            tid, z = land[(x, y)]
            sx, sy = (x - y) * 22, (x + y) * 22
            z_r, z_l, z_b = zs((x + 1, y), z), zs((x, y + 1), z), zs((x + 1, y + 1), z)
            flat = z == z_r == z_l == z_b
            tex = None if flat else art.texmap(art.land_data[tid][1])
            if flat or tex is None:
                im = art.land(tid)
                if im is not None:
                    draws.append((x + y, 0, z, sx, sy - z * 4, im))
            else:
                top, right, bottom, left = (22, -z * 4), (44, 22 - z_r * 4), (22, 44 - z_b * 4), (0, 22 - z_l * 4)
                pts = [top, right, bottom, left]
                minx, miny = min(p[0] for p in pts), min(p[1] for p in pts)
                maxx, maxy = max(p[0] for p in pts), max(p[1] for p in pts)
                W, H = maxx - minx + 1, maxy - miny + 1
                dst = [(px - minx, py - miny) for px, py in pts]
                n = tex.width
                coeffs = _perspective([(0, 0), (n, 0), (n, n), (0, n)], dst)
                if coeffs is None:
                    im = art.land(tid)
                    if im is not None:
                        draws.append((x + y, 0, z, sx, sy - z * 4, im))
                    continue
                warped = tex.transform((W, H), Image.Transform.PERSPECTIVE, tuple(coeffs), Image.Resampling.BILINEAR)
                mask = Image.new('L', (W, H), 0)
                ImageDraw.Draw(mask).polygon(dst, fill=255)
                if shade:
                    # light from the north-west, as the client's: faces rising toward +x/+y (toward the viewer) darken
                    rise_x = (z_r + z_b - z - z_l) / 2.0
                    rise_y = (z_l + z_b - z - z_r) / 2.0
                    k = max(0.55, min(1.25, 1.0 - 0.06 * (rise_x + rise_y)))
                    if k != 1.0:
                        a = np.array(warped).astype(np.float32)
                        a[:, :, :3] = np.clip(a[:, :, :3] * k, 0, 255)
                        warped = Image.fromarray(a.astype(np.uint8), 'RGBA')
                warped.putalpha(mask)
                draws.append((x + y, 0, z, sx + minx, sy + miny, warped))
    for i, (x, y, z, tid) in enumerate(scene.statics):
        if not (x1 <= x <= x2 and y1 <= y <= y2):
            continue
        im = art.static(tid)
        if im is None:
            continue
        sx, sy = (x - y) * 22, (x + y) * 22
        h = art.item_data[tid]['height']
        draws.append((x + y, 1, z * 2 + (1 if h else 0), sx + 22 - im.width // 2, sy + 44 - im.height - z * 4, im))
    if not draws:
        return Image.new('RGBA', (1, 1), background)
    minx = min(d[3] for d in draws) - margin
    miny = min(d[4] for d in draws) - margin
    maxx = max(d[3] + d[5].width for d in draws) + margin
    maxy = max(d[4] + d[5].height for d in draws) + margin
    canvas = Image.new('RGBA', (maxx - minx, maxy - miny), background)
    draws.sort(key=lambda d: (d[0], d[1], d[2]))
    for depth, layer, z, left, top, im in draws:
        canvas.alpha_composite(im, (left - minx, top - miny))
    canvas.info['origin'] = (minx, miny)   # tile (x, y) is at ((x - y) * 22 - minx, (x + y) * 22 - miny)
    return canvas


def tile_px(im, x, y):
    """Pixel position of tile (x, y)'s diamond top corner in an image from render()."""
    ox, oy = im.info['origin']
    return (x - y) * 22 - ox + 22, (x + y) * 22 - oy


def save(im, path, colors=256):
    out = im.convert('RGB')
    if colors:
        out = out.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    out.save(path, optimize=True)
    return os.path.getsize(path)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'map':
        folder, fi, x1, y1, x2, y2, out = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), sys.argv[8]
        sc = Scene.from_map(folder, fi, x1, y1, x2, y2)
        print(out, save(render(sc, x1, y1, x2, y2), out))
    elif mode == 'multi':
        mid, zmax, out = int(sys.argv[2], 16), int(sys.argv[3]), sys.argv[4]
        sc = Scene.from_multi(mid, zmax)
        xs = [c[0] for c in sc.land]
        ys = [c[1] for c in sc.land]
        print(out, save(render(sc, min(xs), min(ys), max(xs) - 1, max(ys) - 1), out))
