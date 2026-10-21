# cc-P237 (a copy of cc-P267-tools/bankbase.py, two paths changed) read-only map tools: one loader for every facet (the server's own client
# files, classic-client-7.0.117.0), the pinned z rules (Map.GetAverageZ, GetTopSurfaceZ, CanFit's blocked test), the
# protected tiles (doors by pinned DoorGenerator's scan, door swings by BaseDoor.GetOffset, spawners, decoration cfg
# items, teleporters, banker paths) and the client-view renderer (P34's uorender geometry, per-facet sizes).
# Nothing here writes a world, a save or a client file. ASCII only.
import os, sys, json, glob, re, struct, collections
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, 'D:/UO/golems/Bronze/shard-migration/scripts')
from mapbuild import uofiles  # noqa: E402

CLIENT = uofiles.CLIENT = 'D:/UO/tool-trials/client-data-copy'  # cc-P237: map, statics and art are SHA-256 equal to the shard's classic-client-7.0.117.0 (tool-trials/hashes-*-after.txt); its tiledata is the package's (ours added; stock records equal but 0x0F3F)
PINNED = 'D:/UO/ModernUO-pinned'
FACET = {'Felucca': 0, 'Trammel': 1, 'Ilshenar': 2, 'Malas': 3, 'Tokuno': 4, 'TerMur': 5}
FNAME = {v: k for k, v in FACET.items()}
IMP, WET, SURF, BRIDGE, WALL, DOOR, ROOF, BG = 0x40, 0x80, 0x200, 0x400, 0x10, 1 << 29, 1 << 28, 1
LAND, ITEMS = uofiles.read_tiledata(CLIENT)


def iflags(i): return ITEMS[i]['flags']
def iheight(i): return ITEMS[i]['height']
def iname(i): return ITEMS[i]['name'].strip()
def lname(i): return LAND[i][2].strip()
def calch(i): return iheight(i) // 2 if iflags(i) & BRIDGE else iheight(i)


def flagstr(f):
    out = []
    for n, b in (('imp', IMP), ('wall', WALL), ('wet', WET), ('surf', SURF), ('bridge', BRIDGE), ('door', DOOR), ('roof', ROOF)):
        if f & b: out.append(n)
    return '|'.join(out) or '-'


class Facet:
    """Land and statics of one facet, by tile."""
    def __init__(self, fi):
        self.fi = fi
        self.name, self.w, self.h = uofiles.FACETS[fi]
        self.mf = uofiles.MapFile(CLIENT, fi)
        self.idx, self.sta = uofiles.load_statics_index(CLIENT, fi)
        self.bh = self.h >> 3
        self._blocks = {}

    def land(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h): return (0, 0)
        return self.mf.get(x, y)

    def landz(self, x, y): return self.land(x, y)[1]

    def block(self, bx, by):
        k = (bx, by)
        if k not in self._blocks:
            self._blocks[k] = uofiles.block_statics(self.idx, self.sta, bx * self.bh + by)
        return self._blocks[k]

    def statics(self, x, y):
        """[(id, z)] on the tile."""
        return [(sid, sz) for (sid, cx, cy, sz, hue) in self.block(x >> 3, y >> 3) if (cx, cy) == (x & 7, y & 7)]

    # pinned Server/Maps/Map.cs GetAverageZ
    def avgz(self, x, y):
        t, l, r, b = self.landz(x, y), self.landz(x, y + 1), self.landz(x + 1, y), self.landz(x + 1, y + 1)
        def fa(a, c):
            v = a + c
            if v < 0: v -= 1
            return int(v / 2)
        return fa(l, r) if abs(t - b) > abs(l - r) else fa(t, b)

    @staticmethod
    def ignored_land(i): return i == 2 or i == 0x1DB or 0x1AE <= i <= 0x1B5

    def top_surface(self, x, y, pz=127):
        """pinned Map.GetTopSurfaceZ: the highest surface at or below pz (land or a Surface/Wet static top)."""
        s = None
        lid, _ = self.land(x, y)
        if not self.ignored_land(lid):
            a = self.avgz(x, y)
            if a <= pz: s = a
        for sid, sz in self.statics(x, y):
            f = iflags(sid)
            if f & SURF or f & WET:
                tz = sz + calch(sid)
                if (s is None or tz > s) and tz <= pz: s = tz
        return s

    def blocked(self, x, y, z):
        """An Impassable static in the way of something standing at z (CanFit, PersonHeight 16)."""
        for sid, sz in self.statics(x, y):
            f = iflags(sid)
            if f & IMP and sz < z + 16 and sz + calch(sid) > z: return '0x%04X(%s)' % (sid, iname(sid))
        return ''

    def wall_at(self, x, y, z):
        return any(iflags(s) & WALL and z - 3 <= sz <= z + 3 for s, sz in self.statics(x, y))

    def wall_ids_at(self, x, y, z):
        return [(s, sz) for s, sz in self.statics(x, y) if iflags(s) & WALL and z - 3 <= sz <= z + 3]

    def roof_over(self, x, y, z):
        return any(iflags(s) & ROOF and sz > z for s, sz in self.statics(x, y))

    def describe(self, x, y):
        return ' '.join('0x%04X@%d+%d[%s](%s)' % (s, sz, iheight(s), flagstr(iflags(s)), iname(s)) for s, sz in self.statics(x, y)) or 'none'


WALK_LAND = ('dirt', 'cobblestone', 'flagstone', 'road', 'sand stone', 'marble', 'brick', 'stone', 'paving')
WALK_STATIC = ('road', 'path', 'planks', 'dock', 'pier', 'boards', 'cobblestone', 'flagstone', 'paving', 'tile', 'floor', 'marble', 'brick')


def walkway(F, x, y, z):
    """A road or plaza tile (P34's rule): road-like land at z, or a floor/path static top at z."""
    ln = lname(F.land(x, y)[0]).lower()
    if F.top_surface(x, y, z + 2) is not None and any(w in ln for w in WALK_LAND) and abs(F.avgz(x, y) - z) <= 2: return 'land:' + ln
    for sid, sz in F.statics(x, y):
        n = iname(sid).lower()
        if abs(sz + calch(sid) - z) <= 2 and any(w in n for w in WALK_STATIC): return 'static:' + n
    return ''


# ------------------------------------------------------------------ doors: pinned UOContent/Misc/DoorGenerator.cs
_SOUTH = [0x0006, 0x0008, 0x000B, 0x001A, 0x001B, 0x001F, 0x0038, 0x0057, 0x0059, 0x005B, 0x005D, 0x0080, 0x0081, 0x0082, 0x0084, 0x0090, 0x0091, 0x0094, 0x0096, 0x0099, 0x00A6, 0x00A7, 0x00AA, 0x00AE, 0x00B0, 0x00B3, 0x00C7, 0x00C9, 0x00F8, 0x00FA, 0x00FD, 0x00FE, 0x0100, 0x0103, 0x0104, 0x0106, 0x0109, 0x0127, 0x0129, 0x012B, 0x012D, 0x012F, 0x0131, 0x0132, 0x0134, 0x0135, 0x0137, 0x0139, 0x013B, 0x014C, 0x014E, 0x014F, 0x0151, 0x0153, 0x0155, 0x0157, 0x0158, 0x015A, 0x015D, 0x015E, 0x015F, 0x0162, 0x01CF, 0x01D1, 0x01D4, 0x01FF, 0x0204, 0x0206, 0x0208, 0x020A]
_NORTH = [0x0006, 0x0008, 0x000D, 0x001A, 0x001B, 0x0020, 0x003A, 0x0057, 0x0059, 0x005B, 0x005D, 0x0080, 0x0081, 0x0082, 0x0084, 0x0090, 0x0091, 0x0094, 0x0096, 0x0099, 0x00A6, 0x00A7, 0x00AC, 0x00AE, 0x00B0, 0x00C7, 0x00C9, 0x00F8, 0x00FA, 0x00FD, 0x00FE, 0x0100, 0x0103, 0x0104, 0x0106, 0x0109, 0x0127, 0x0129, 0x012B, 0x012D, 0x012F, 0x0131, 0x0132, 0x0134, 0x0135, 0x0137, 0x0139, 0x013B, 0x014C, 0x014E, 0x014F, 0x0151, 0x0153, 0x0155, 0x0157, 0x0158, 0x015A, 0x015D, 0x015E, 0x015F, 0x0162, 0x01CF, 0x01D1, 0x01D4, 0x01FF, 0x0201, 0x0204, 0x0208, 0x020A]
_EAST = [0x0007, 0x000A, 0x001A, 0x001C, 0x001E, 0x0037, 0x0058, 0x0059, 0x005C, 0x005E, 0x0080, 0x0081, 0x0082, 0x0084, 0x0090, 0x0092, 0x0095, 0x0097, 0x0098, 0x00A6, 0x00A8, 0x00AB, 0x00AE, 0x00AF, 0x00B2, 0x00C7, 0x00C8, 0x00EA, 0x00F8, 0x00F9, 0x00FC, 0x00FE, 0x00FF, 0x0102, 0x0104, 0x0105, 0x0108, 0x0127, 0x0128, 0x012B, 0x012C, 0x012E, 0x0130, 0x0132, 0x0133, 0x0135, 0x0136, 0x0138, 0x013A, 0x014C, 0x014D, 0x014F, 0x0150, 0x0152, 0x0154, 0x0156, 0x0158, 0x0159, 0x015C, 0x015E, 0x0160, 0x0163, 0x01CF, 0x01D0, 0x01D3, 0x01FF, 0x0203, 0x0205, 0x0207, 0x0209]
_WEST = [0x0007, 0x000C, 0x001A, 0x001C, 0x0021, 0x0039, 0x0058, 0x0059, 0x005C, 0x005E, 0x0080, 0x0081, 0x0082, 0x0084, 0x0090, 0x0092, 0x0095, 0x0097, 0x0098, 0x00A6, 0x00A8, 0x00AD, 0x00AE, 0x00AF, 0x00B5, 0x00C7, 0x00C8, 0x00EA, 0x00F8, 0x00F9, 0x00FC, 0x00FE, 0x00FF, 0x0102, 0x0104, 0x0105, 0x0108, 0x0127, 0x0128, 0x012C, 0x012E, 0x0130, 0x0132, 0x0133, 0x0135, 0x0136, 0x0138, 0x013A, 0x014C, 0x014D, 0x014F, 0x0150, 0x0152, 0x0154, 0x0156, 0x0158, 0x0159, 0x015C, 0x015E, 0x0160, 0x0163, 0x01CF, 0x01D0, 0x01D3, 0x01FF, 0x0200, 0x0203, 0x0207, 0x0209]
_SOUTH, _NORTH, _EAST, _WEST = set(_SOUTH), set(_NORTH), set(_EAST), set(_WEST)
# pinned BaseDoor.m_Offsets by DoorFacing (P34 copied them; Items/Construction/Doors/BaseDoor.cs:13-28)
SWING = {'WestCW': (-1, 1), 'EastCCW': (1, 1), 'WestCCW': (-1, 0), 'EastCW': (1, -1), 'SouthCW': (1, 1),
         'NorthCCW': (1, -1), 'SouthCCW': (0, 0), 'NorthCW': (0, -1)}
# Maps the generator runs on (DoorGenerator.Generate): Trammel and Felucca (its regions), Ilshenar, Malas. Not Tokuno,
# not Ter Mur: their doors are either decoration cfg items (tokuno.cfg) or map statics with the Door flag.
DOORGEN_MAPS = {0, 1, 2, 3}


def _frame_at(F, x, y, z, frames):
    for sid, sz in F.statics(x, y):
        if sid in frames and -1 <= sz - z <= 1: return True, sz
    return False, None


def _can_fit(F, x, y, z):
    """pinned Map.CanFit(x, y, z, 16, false, false) reduced to the files: no impassable static (walls included) and no
    surface static crossing z..z+16 on the tile, and the land not impassable. The generator's AddDoor refuses a door
    where this fails (DoorGenerator.cs:481-485), which is what keeps a continuous wall of frame-listed pieces from
    becoming a row of doors."""
    lid, lz = F.land(x, y)
    if LAND[lid][0] & IMP: return False
    for sid, sz in F.statics(x, y):
        f = iflags(sid)
        if (f & IMP or f & SURF) and sz < z + 16 and sz + calch(sid) > z: return False
    return True


def generated_doors(F, x0, y0, x1, y1):
    """[(x, y, z, facing)] the pinned DoorGenerator scan would place inside the box (the four Britain exceptions left
    out: a door it would refuse there is still a doorway nobody should decorate)."""
    out = []
    if F.fi not in DOORGEN_MAPS: return out
    def add(x, y, z, facing):
        if _can_fit(F, x, y, z): out.append((x, y, z, facing))
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for sid, z in F.statics(x, y):
                if sid in _WEST:
                    ok, nz = _frame_at(F, x + 2, y, z, _EAST)
                    if ok: add(x + 1, y, min(z, nz), 'WestCW'); continue
                    ok, nz = _frame_at(F, x + 3, y, z, _EAST)
                    if ok: add(x + 1, y, min(z, nz), 'WestCW'); add(x + 2, y, min(z, nz), 'EastCCW')
                elif sid in _NORTH:
                    ok, nz = _frame_at(F, x, y + 2, z, _SOUTH)
                    if ok: add(x, y + 1, min(z, nz), 'SouthCW'); continue
                    ok, nz = _frame_at(F, x, y + 3, z, _SOUTH)
                    if ok: add(x, y + 1, min(z, nz), 'NorthCCW'); add(x, y + 2, min(z, nz), 'SouthCW')
    return sorted(set(out))


def static_doors(F, x0, y0, x1, y1):
    """Map statics flagged Door (Ter Mur, some Tokuno): [(x, y, z, id)]."""
    out = []
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for sid, z in F.statics(x, y):
                if iflags(sid) & DOOR: out.append((x, y, z, sid))
    return out


# ------------------------------------------------------------------ pinned world data in a box
_SPAWNS = None
def spawns():
    global _SPAWNS
    if _SPAWNS is None:
        _SPAWNS = []
        for sub in ('shared', 'post-uoml'):   # Core.SA: AdminGump.cs:4031 picks post-uoml, and shared always
            for f in glob.glob(PINNED + '/Distribution/Data/Spawns/%s/**/*.json' % sub, recursive=True):
                try: d = json.load(open(f, encoding='utf-8-sig'))
                except Exception: continue
                for e in d if isinstance(d, list) else []:
                    loc = e.get('location')
                    if not loc: continue
                    names = [x.get('name') for x in (e.get('entries') or [])]
                    _SPAWNS.append((e.get('map'), loc[0], loc[1], loc[2], e.get('homeRange', 0), names, os.path.relpath(f, PINNED + '/Distribution/Data')))
    return _SPAWNS


def spawns_in(fname, x0, y0, x1, y1):
    return [s for s in spawns() if s[0] == fname and x0 <= s[1] <= x1 and y0 <= s[2] <= y1]


DECOR_FOLDERS = {0: ['Britannia', 'Felucca'], 1: ['Britannia', 'Trammel'], 2: ['Ilshenar'], 3: ['Malas'], 4: ['Tokuno'], 5: []}
_DECOR = {}
def decoration(fi):
    """[(x, y, z, type, id, file)] from pinned Data/Decoration for the facet (Decorate.cs:37-42 says which folders)."""
    if fi in _DECOR: return _DECOR[fi]
    out = []
    for folder in DECOR_FOLDERS[fi]:
        for f in glob.glob(PINNED + '/Distribution/Data/Decoration/%s/*.cfg' % folder):
            head = None
            for line in open(f, encoding='latin1'):
                line = line.strip()
                if not line or line.startswith('#'): continue
                m = re.match(r'^(\d+)\s+(\d+)\s+(-?\d+)', line)
                if m and head:
                    out.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), head[0], head[1], os.path.basename(f)))
                elif re.match(r'^[A-Za-z]', line):
                    parts = line.split()
                    head = (parts[0], parts[1] if len(parts) > 1 else '')
    _DECOR[fi] = out
    return out


def decoration_in(fi, x0, y0, x1, y1):
    return [d for d in decoration(fi) if x0 <= d[0] <= x1 and y0 <= d[1] <= y1]


_TELE = None
def teleporters_in(fname, x0, y0, x1, y1):
    global _TELE
    if _TELE is None: _TELE = json.load(open(PINNED + '/Distribution/Data/teleporters.json'))
    out = []
    for t in _TELE:
        for end in ('src', 'dst'):
            e = t[end]
            if e['map'] == fname and x0 <= e['loc'][0] <= x1 and y0 <= e['loc'][1] <= y1:
                out.append((e['loc'][0], e['loc'][1], e['loc'][2], end))
    return out


# ------------------------------------------------------------------ the renderer (P34's uorender geometry)
_src = open('D:/UO/golems/Bronze/ShatteredLegacy/design/registrar-office/uorender.py').read()
_src = _src.replace("os.path.expanduser('~/mnt/ShatteredLegacy/client-data/classic-client')", repr(CLIENT))
_RNS = {}
exec(compile(_src.split('def render(')[0], 'uor', 'exec'), _RNS)
Art = _RNS['Art']
_ART = None
def art():
    global _ART
    if _ART is None: _ART = Art()
    return _ART


def persp_coeffs(src, dst):
    A = []; B = []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def _sitem(sid, x, y, z, seq, new=False):
    fl = iflags(sid); hg = iheight(sid)
    pz = z
    if fl & 1: pz -= 1
    if hg > 0: pz += 1
    return (x + y, pz, 1, seq, ('S', sid, x, y, z, new))


def render(F, x0, y0, x1, y1, extra=(), marks=(), grid=5, out='out.png', scale=1, hide_roofs_above=None, label=None):
    """Client-view picture of the box. extra: [(id, x, y, z)] items drawn in; marks: [(label, x, y, z, colour)].
    hide_roofs_above: leave out roof and wall statics whose z is above this (to see inside a building)."""
    A = art()
    items = []; seq = 0
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            tid, z = F.land(x, y)
            zr, zb, zl = F.landz(x + 1, y), F.landz(x + 1, y + 1), F.landz(x, y + 1)
            items.append((x + y, (z + zr + zb + zl) // 4 - 1, 0, seq, ('L', x, y, tid, z, zr, zb, zl))); seq += 1
    for bx in range(x0 >> 3, (x1 >> 3) + 1):
        for by in range(y0 >> 3, (y1 >> 3) + 1):
            for (sid, sx, sy, sz, hue) in F.block(bx, by):
                x = bx * 8 + sx; y = by * 8 + sy
                if not (x0 <= x <= x1 and y0 <= y <= y1): continue
                if hide_roofs_above is not None and sz > hide_roofs_above and (iflags(sid) & (ROOF | WALL) or iheight(sid) >= 15 or iflags(sid) & SURF):
                    continue
                items.append(_sitem(sid, x, y, sz, seq)); seq += 1
    for (sid, x, y, z) in extra:
        items.append(_sitem(sid, x, y, z, seq, True)); seq += 1
    items.sort(key=lambda a: (a[0], a[1], a[2], a[3]))
    def scr(x, y, z): return ((x - y) * 22, (x + y) * 22 - z * 4)
    xs = [scr(x, y, 0)[0] for x, y in [(x0, y1), (x1, y0)]]
    ys = [scr(x0, y0, 0)[1], scr(x1, y1, 0)[1]]
    ox = -xs[0] + 60; oy = -ys[0] + 300
    Wc = xs[1] - xs[0] + 120; Hc = ys[1] - ys[0] + 420
    can = Image.new('RGBA', (Wc, Hc), (0, 0, 0, 255))
    for it in items:
        k = it[4]
        if k[0] == 'L':
            _, x, y, tid, z, zr, zb, zl = k
            im = A.land(tid)
            if im is None: continue
            sx, sy = scr(x, y, 0); sx += ox; sy += oy
            pts = [(sx, sy - z * 4), (sx + 22, sy + 22 - zr * 4), (sx, sy + 44 - zb * 4), (sx - 22, sy + 22 - zl * 4)]
            if z == zr == zb == zl:
                can.alpha_composite(im, (sx - 22, sy - z * 4))
            else:
                minx = min(p[0] for p in pts); miny = min(p[1] for p in pts)
                maxx = max(p[0] for p in pts); maxy = max(p[1] for p in pts)
                w = maxx - minx + 1; h = maxy - miny + 1
                if w <= 0 or h <= 0 or h > 600: continue
                dst = [(p[0] - minx, p[1] - miny) for p in pts]
                src = [(22, 0), (44, 22), (22, 44), (0, 22)]
                try:
                    c = persp_coeffs(src, dst)
                    tim = im.transform((w, h), Image.PERSPECTIVE, c, Image.BILINEAR)
                    mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).polygon(dst, fill=255)
                    a = np.array(tim); a[..., 3] = np.minimum(a[..., 3], np.array(mask))
                    can.alpha_composite(Image.fromarray(a), (minx, miny))
                except Exception: pass
        else:
            _, sid, x, y, z, new = k
            im = A.static(sid)
            if im is None: continue
            sx, sy = scr(x, y, z); sx += ox; sy += oy
            px, py = sx - im.width // 2, sy + 44 - im.height
            if px < -im.width or py < -im.height or px > Wc or py > Hc: continue
            can.alpha_composite(im, (max(px, 0), max(py, 0)), (max(-px, 0), max(-py, 0)))
    d = ImageDraw.Draw(can)
    try: f = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 13)
    except Exception: f = ImageFont.load_default()
    if grid:
        for x in range(x0 - x0 % grid, x1 + 1, grid):
            for y in range(y0 - y0 % grid, y1 + 1, grid):
                if x < x0 or y < y0: continue
                z = F.landz(x, y); sx, sy = scr(x, y, z); sx += ox; sy += oy + 22
                d.ellipse((sx - 3, sy - 3, sx + 3, sy + 3), fill=(255, 255, 0, 255))
                d.text((sx + 5, sy - 7), '%d,%d' % (x, y), fill=(255, 255, 0, 255), font=f, stroke_width=2, stroke_fill=(0, 0, 0, 255))
    for (lab, x, y, z, col) in marks:
        sx, sy = scr(x, y, z); sx += ox; sy += oy + 22
        d.ellipse((sx - 6, sy - 6, sx + 6, sy + 6), outline=col, width=3)
        if lab: d.text((sx + 8, sy - 20), lab, fill=col, font=f, stroke_width=2, stroke_fill=(0, 0, 0, 255))
    if label:
        try: f2 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 20)
        except Exception: f2 = f
        d.text((12, 10), label, fill=(255, 255, 255, 255), font=f2, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    can = can.convert('RGB')
    if scale != 1: can = can.resize((int(can.width * scale), int(can.height * scale)), Image.LANCZOS)
    can.save(out, optimize=True)
    return can.size


def floormap(F, x0, y0, x1, y1, fz, protected=None, marks=None):
    """ASCII map of one floor: # wall, D door, t blocking furniture, . floor, ~ ground, ' ' nothing; P protected, * mark."""
    protected = protected or {}
    marks = marks or {}
    lines = ['      ' + ''.join(str((x // 10) % 10) if x % 10 == 0 else (str(x % 10) if x % 5 == 0 else ' ') for x in range(x0, x1 + 1))]
    for y in range(y0, y1 + 1):
        line = ''
        for x in range(x0, x1 + 1):
            st = F.statics(x, y)
            w = [s for s, z in st if iflags(s) & WALL and fz - 3 <= z <= fz + 3]
            dr = [s for s, z in st if iflags(s) & DOOR and fz - 3 <= z <= fz + 3]
            tb = [s for s, z in st if iflags(s) & IMP and not iflags(s) & WALL and fz - 3 <= z <= fz + 6]
            fl = [s for s, z in st if iflags(s) & SURF and fz - 3 <= z + calch(s) <= fz + 3]
            ln = abs(F.avgz(x, y) - fz) <= 2
            c = 'D' if dr else ('#' if w else ('t' if tb else ('.' if fl else ('~' if ln else ' '))))
            if (x, y) in marks: c = marks[(x, y)]
            elif (x, y) in protected and c in '.~': c = 'P'
            line += c
        lines.append('%5d %s' % (y, line))
    return '\n'.join(lines)
