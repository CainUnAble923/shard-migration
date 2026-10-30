"""cc-P734: the six practice builds, laid by the rules of notes/guides/building-and-decorating.md.

Every wall set, window, roof and gable piece is read from an OSI house multi of that material (kit()), never typed by
hand, and placed by the rules the multis follow (stair-survey.txt, roof-survey.txt):

  - walls: post at the NW tile, the "south" run piece along the north and south rows, the "east" run piece along the
    west and east columns, the L corner at the SE tile; a door or window replaces the run piece on its tile;
  - floor: at the wall Z, inside plus under the south row and the east column;
  - roof: lowest course at wall Z + 20, from one tile in from the NW corner to one tile past the SE corner (x0+1..x1+1,
    y0+1..y1+1), pitched along y: west slope, east slope, ridge, +3 Z per course; the gable on the south wall's row;
  - doors in a south (east-west) wall: DarkWoodDoor WestCCW, which folds back along the wall (guide 2.4);
  - wall-mounted lights on the floor tile in front of a north or west wall at floor + 13 (guide 3).

Writes, for each build: <code>/server/data/Decoration/Builds/practice-<name>.cfg (relative to the plot's NW corner),
notes/cc-P734-review/placed-<name>.md lines, and an isorender preview notes/cc-P734-review/render-<name>.jpg.
Usage (from shard-migration, PYTHONPATH=scripts;notes/cc-P734-tools): python -P notes/cc-P734-tools/gen_builds.py [name ...]
"""
import collections
import os
import sys

import stair_survey as S
from mapbuild import isorender

CODE = os.environ.get('SL_CODE', r'D:\UO\golems\Iron\ShatteredLegacy')
OUT_CFG = os.path.join(CODE, 'server', 'data', 'Decoration', 'Builds')
OUT_REV = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cc-P734-review')
GRASS = 0x0003   # plain grass land for the previews
OVERLAY = os.environ.get('P734_OVERLAY', r'D:\UO\golems\Iron\p734-proof\overlay')   # this branch's map (the dock's lake)


def kit(mid):
    """A wall-and-roof kit read from house multi `mid`: post, corner, south/east run pieces, S/E windows, roof
    west/east/ridge, gable, door Z."""
    cs = S.comps(mid)
    walls = [c for c in cs if S.items[c[3]]['height'] >= 19]
    z0 = min(w[2] for w in walls)
    base = [w for w in walls if w[2] == z0 and 'door' not in S.name(w[3])]
    x0 = min(b[0] for b in base); x1 = max(b[0] for b in base)
    y0 = min(b[1] for b in base); y1 = max(b[1] for b in base)
    at = {(b[0], b[1]): b[3] for b in base}
    k = {'post': at[(x0, y0)], 'corner': at[(x1, y1)]}
    s_run = collections.Counter(); e_run = collections.Counter(); s_win = collections.Counter(); e_win = collections.Counter()
    for (x, y), t in at.items():
        win = 'window' in S.name(t)
        if y in (y0, y1) and x0 < x < x1:
            (s_win if win else s_run)[t] += 1
        elif x in (x0, x1) and y0 < y < y1:
            (e_win if win else e_run)[t] += 1
    k['south'] = s_run.most_common(1)[0][0]
    k['east'] = e_run.most_common(1)[0][0]
    k['swin'] = s_win.most_common(1)[0][0] if s_win else k['south']
    k['ewin'] = e_win.most_common(1)[0][0] if e_win else k['east']
    roofs = [c for c in cs if 'roof' in S.name(c[3]) or 'shingle' in S.name(c[3])]
    rz = min(r[2] for r in roofs)
    low = [r for r in roofs if r[2] == rz]
    k['roof_w'] = collections.Counter(r[3] for r in low if r[0] == min(l[0] for l in low)).most_common(1)[0][0]
    k['roof_e'] = collections.Counter(r[3] for r in low if r[0] == max(l[0] for l in low)).most_common(1)[0][0]
    top = max(r[2] for r in roofs if r[2] < rz + 20)
    k['ridge'] = collections.Counter(r[3] for r in roofs if r[2] == top).most_common(1)[0][0]
    gab = collections.Counter(c[3] for c in cs if c[2] >= z0 + 20 and S.items[c[3]]['height'] <= 5 and 'roof' not in S.name(c[3]) and 'shingle' not in S.name(c[3]) and 'wall' in S.name(c[3]))
    k['gable'] = gab.most_common(1)[0][0] if gab else None
    k['mid'] = mid
    return k


class Build:
    def __init__(self, name, title):
        self.name, self.title = name, title
        self.lists = collections.OrderedDict()   # type line -> [(x, y, z)]
        self.placed = []                         # (section, line)
        self.statics = []                        # preview (x, y, z, art)
        self.section = ''

    def add(self, typeline, x, y, z, art, what, facing=''):
        self.lists.setdefault(typeline, []).append((x, y, z))
        self.statics.append((x, y, z, art))
        self.placed.append((self.section, '0x%04X %s, %d,%d,%d%s' % (art, what, x, y, z, (', ' + facing) if facing else '')))

    def static(self, art, x, y, z, what, facing='', name=None):
        tl = 'Static 0x%04X' % art + (' (Name=%s)' % name if name else '')
        self.add(tl, x, y, z, art, what, facing)

    def addon(self, cls, comps, x, y, z, what, facing):
        self.lists.setdefault(cls, []).append((x, y, z))
        for art, dx, dy, dz in comps:
            self.statics.append((x + dx, y + dy, z + dz, art))
        self.placed.append((self.section, '%s (%s), %d,%d,%d, %s' % (cls, '+'.join('0x%04X' % c[0] for c in comps), x, y, z, facing)))

    def door(self, x, y, z, what):
        # DarkWoodDoor WestCCW: closed art 0x06A9, hung in an east-west (north or south) wall, opens along the wall.
        self.lists.setdefault('DarkWoodDoor (Facing=WestCCW)', []).append((x, y, z))
        self.statics.append((x, y, z, 0x06A9))
        self.placed.append((self.section, '0x06A9 DarkWoodDoor %s, %d,%d,%d, WestCCW (in the east-west wall, folds along it)' % (what, x, y, z)))

    # A walled box x0..x1, y0..y1 (wall tiles) at wall Z z: walls by the rule, floor, roof (unless roof=False).
    def walls(self, k, x0, y0, x1, y1, z, doors=(), swins=(), ewins=(), storey=''):
        """The OSI rule (stair-survey.txt): post NW; the "south" piece along the north row from x0+1 to x1 (so the NE
        corner tile) and the south row between the corners; the "east" piece down the west column from y0+1 to y1 (so
        the SW corner tile, review round 1) and the east column between the corners; the L corner SE."""
        self.section = 'walls' + storey
        doorset = set(doors)
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if (x, y) in doorset or not (x in (x0, x1) or y in (y0, y1)):
                    continue
                if (x, y) == (x0, y0):
                    self.static(k['post'], x, y, z, 'post', 'NW corner')
                elif (x, y) == (x1, y1):
                    self.static(k['corner'], x, y, z, 'L corner', 'SE corner')
                elif x == x0 or (x == x1 and y != y0):
                    art = k['ewin'] if (x, y) in ewins else k['east']
                    self.static(art, x, y, z, 'window' if (x, y) in ewins else 'wall', '"east" piece, north-south run, %s column%s' % ('west' if x == x0 else 'east', ', SW corner' if (x, y) == (x0, y1) else ''))
                else:
                    art = k['swin'] if (x, y) in swins else k['south']
                    self.static(art, x, y, z, 'window' if (x, y) in swins else 'wall', '"south" piece, east-west run, %s row%s' % ('north' if y == y0 else 'south', ', NE corner' if (x, y) == (x1, y0) else ''))

    def house(self, k, x0, y0, x1, y1, z, floor, doors=(), swins=(), ewins=(), roof=True, floor_art_fn=None):
        self.walls(k, x0, y0, x1, y1, z, doors, swins, ewins)
        for (x, y) in doors:
            self.section = 'doors'
            self.door(x, y, z, 'front door')
        self.section = 'floor'
        for x in range(x0 + 1, x1 + 1):
            for y in range(y0 + 1, y1 + 1):
                art = floor_art_fn(x, y) if floor_art_fn else floor[(x + y) % len(floor)]
                self.static(art, x, y, z, 'floor')
        if roof:
            self.roof(k, x0, y0, x1, y1, z + 20)

    def roof(self, k, x0, y0, x1, y1, rz):
        self.section = 'roof'
        cols = list(range(x0 + 1, x1 + 2))
        w = len(cols)
        half = w // 2
        for i in range(half):
            zz = rz + 3 * i
            for y in range(y0 + 1, y1 + 2):
                self.static(k['roof_w'], cols[i], y, zz, 'roof west slope')
                self.static(k['roof_e'], cols[-1 - i], y, zz, 'roof east slope')
            if k['gable']:
                for x in range(cols[i] + 1, cols[-1 - i]):
                    self.static(k['gable'], x, y1, zz, 'gable', 'south wall row')
        if w % 2:
            for y in range(y0 + 1, y1 + 2):
                self.static(k['ridge'], cols[half], y, rz + 3 * half, 'roof ridge')

    def write(self):
        os.makedirs(OUT_CFG, exist_ok=True)
        lines = ['# cc-P734 practice build "%s": %s' % (self.name, self.title),
                 '# Coordinates are relative to the plot\'s north-west corner at ground level; place with',
                 '# [PlaceBuild practice-%s x y z (or where you stand). Made by shard-migration notes/cc-P734-tools/gen_builds.py' % self.name,
                 '# by the rules of notes/guides/building-and-decorating.md; do not edit by hand.', '']
        for tl, pts in self.lists.items():
            lines.append(tl)
            for x, y, z in pts:
                lines.append('%d %d %d' % (x, y, z))
            lines.append('')
        with open(os.path.join(OUT_CFG, 'practice-%s.cfg' % self.name), 'w', encoding='ascii', newline='\n') as f:
            f.write('\n'.join(lines))
        os.makedirs(OUT_REV, exist_ok=True)
        md = ['## %s: %s' % (self.name, self.title), '',
              'Relative to the plot corner; `[PlaceBuild practice-%s` (%d pieces).' % (self.name, sum(len(p) for p in self.lists.values())), '']
        cur = None
        for sec, line in self.placed:
            if sec != cur:
                md += ['', '### ' + sec, '']
                cur = sec
            md.append('- ' + line)
        with open(os.path.join(OUT_REV, 'placed-%s.md' % self.name), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(md) + '\n')

    map_origin = None   # set for a build designed onto a real map place (the dock): its previews use that map

    def render(self, pad=3, below=None, suffix=''):
        """The preview; with below, only the pieces under that Z (a cut-away: roof off, or one storey)."""
        keep = [s for s in self.statics if below is None or s[2] < below]
        xs = [s[0] for s in self.statics]; ys = [s[1] for s in self.statics]
        x1, y1, x2, y2 = min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad
        if self.map_origin:
            ox, oy = self.map_origin
            sc = isorender.Scene.from_map(OVERLAY, 1, ox + x1, oy + y1, ox + x2, oy + y2)
            sc.statics = list(sc.statics) + [(x + ox, y + oy, z, t) for x, y, z, t in keep]
            im = isorender.render(sc, ox + x1, oy + y1, ox + x2, oy + y2)
        else:
            land = {(x, y): (GRASS, 0) for x in range(x1 - 1, x2 + 3) for y in range(y1 - 1, y2 + 3)}
            im = isorender.render(isorender.Scene(land, keep), x1, y1, x2, y2)
        isorender.save(im.resize((im.width * 3 // 4, im.height * 3 // 4)), os.path.join(OUT_REV, 'render-%s%s.jpg' % (self.name, suffix)), colors=0)


BOARDS = [0x04A9, 0x04AA, 0x04AB, 0x04AC]
FLAGSTONE = [0x04FC, 0x04FD, 0x04FE, 0x04FF]
PAVERS = [0x0519, 0x051A, 0x051B, 0x051C, 0x051D, 0x051E]


def carpet(b, x0, y0, x1, y1, z):
    """A red carpet framed by its edges and corners, each drawn from the art: edges north 0x0ACE, south 0x0AD0, west
    0x0ACD, east 0x0ACF (review round 1); corners NW 0x0ACA, SE 0x0AC9 (review round 2 rendered both ways: round 1's
    swap drew loose tufts; P720's isle reading was right), NE 0x0ACC, SW 0x0ACB; centre 0x0AC8. A one-row runner is
    the west end 0x0ACD, centre pieces and the east end 0x0ACF (round 2)."""
    b.section = 'carpet'
    if y0 == y1:
        for x in range(x0, x1 + 1):
            b.static(0x0ACD if x == x0 else (0x0ACF if x == x1 else 0x0AC8), x, y0, z, 'carpet runner')
        return
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if (x, y) == (x0, y0): t = 0x0ACA
            elif (x, y) == (x1, y0): t = 0x0ACC
            elif (x, y) == (x0, y1): t = 0x0ACB
            elif (x, y) == (x1, y1): t = 0x0AC9
            elif y == y0: t = 0x0ACE
            elif y == y1: t = 0x0AD0
            elif x == x0: t = 0x0ACD
            elif x == x1: t = 0x0ACF
            else: t = 0x0AC8
            b.static(t, x, y, z, 'carpet')


def fence_ring(b, x0, y0, x1, y1, gate=None):
    """One closed wooden fence ring by the wall rule (review round 1: 0x0835 is the fence's L corner, so it goes SE;
    the post 0x0838 NW; 0x0836 along the north row to the NE tile and the south row; 0x0837 down the west column to
    the SW tile and the east column), one piece per tile, Z 0, with one LightWoodGate in its west side at `gate`."""
    b.section = 'fence'
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if not (x in (x0, x1) or y in (y0, y1)) or (x, y) == gate:
                continue
            if (x, y) == (x0, y0):
                b.static(0x0838, x, y, 0, 'fence post', 'NW corner')
            elif (x, y) == (x1, y1):
                b.static(0x0835, x, y, 0, 'fence L corner', 'SE corner')
            elif x == x0 or (x == x1 and y != y0):
                b.static(0x0837, x, y, 0, 'fence', 'north-south run' + (', SW corner' if (x, y) == (x0, y1) else ''))
            else:
                b.static(0x0836, x, y, 0, 'fence', 'east-west run' + (', NE corner' if (x, y) == (x1, y0) else ''))
    if gate:
        b.section = 'gate'
        b.lists.setdefault('LightWoodGate (Facing=NorthCCW)', []).append((gate[0], gate[1], 0))
        b.statics.append((gate[0], gate[1], 0, 0x0843))   # 0x839 + 2 * NorthCCW (5)
        b.placed.append(('gate', 'LightWoodGate NorthCCW, %d,%d,0, one gate in the north-south fence (guide 2.4)' % gate))


def shop_sign(b, door, art, name, z=5):
    """The hanger 0x0B98 (the arm that sticks out from a south wall; 0x0B97 lies along it) and its board, on the tile
    outside the south wall two east of the door (OSI multi 0x0064: door 3,3, sign 5,4; review round 1: one east of
    the door covers the door leaf), Z 5."""
    b.section = 'sign'
    x, y = door[0] + 2, door[1] + 1
    b.static(0x0B98, x, y, z, 'sign hanger', 'outside the south wall, two east of the door')
    b.static(art, x, y, z, 'sign board', 'outside the south wall, two east of the door', name=name)


def signpost(b, x, y, name, z=0):
    b.section = 'signpost'
    b.static(0xA854, x, y, z, 'standing signpost', 'beside the path, off the door line and the walk line', name=name)


def chairs_at(b, x, y_north, y_south, z=0):
    """Chairs facing a table between them (review round 1, from the art: 0x0B4E faces east, 0x0B4F south, 0x0B50
    north): 0x0B4F on the north side, 0x0B50 on the south side."""
    b.static(0x0B4F, x, y_north, z, 'chair', 'north of the table, facing south to it')
    b.static(0x0B50, x, y_south, z, 'chair', 'south of the table, facing north to it')


# ---- the six builds ---------------------------------------------------------------------------------------------------

def farmhouse():
    b = Build('farmhouse', 'a small farmhouse: light wood under thatch, a fenced kitchen garden, a well-kept yard')
    k = kit(0x006E)
    k['swin'] = 0x00BA   # the multi has no window in an east-west wall; 0x00BA is light wood's other window (render checks it)
    # 7 x 6 walls at x 2..8, y 2..7; the door in the south wall at x 5. Windows kept clear of furniture (round 1).
    b.house(k, 2, 2, 8, 7, 0, BOARDS, doors=[(5, 7)], swins=[(4, 2), (7, 7)], ewins=[(2, 4), (8, 5)])
    b.section = 'inside'
    # The hearth on the north wall under the roof's high middle (round 1: on the west wall its 24-high chimney came
    # through the low thatch at the roof's edge).
    b.addon('StoneFireplaceSouthAddon', [(0x0967, -1, 0, 0), (0x0961, 0, 0, 0)], 6, 3, 0, 'fireplace', 'against the north wall, facing south into the room, under the ridge')
    # Round 2: the bed stood mid-room; its head now on the north wall, along the east wall (the reviewer's 8,3 is the
    # east wall's own tile, so 7,3).
    b.addon('SmallBedSouthAddon', [(0x0A63, 0, 0, 0), (0x0A5C, 0, 1, 0)], 7, 3, 0, 'bed', 'head against the north wall, along the east wall')
    b.static(0x0B90, 4, 5, 0, 'table')
    chairs_at(b, 4, 4, 6)
    b.static(0x09D7, 4, 5, 6, 'plate on the table')
    b.static(0x0E77, 3, 3, 0, 'barrel', 'north-west corner')
    b.static(0x1039, 3, 6, 0, 'sack of flour', 'south-west corner')
    b.static(0x0A07, 3, 5, 13, 'wall torch', 'west wall (plain piece at 2,5), floor tile in front, floor + 13')
    shop_sign(b, (5, 7), 0x0BD2, 'Practice farmhouse')
    fence_ring(b, 10, 3, 16, 8, gate=(10, 5))
    b.section = 'garden'
    for x in range(12, 16):
        for y in (4, 6):
            b.static(0x0C7B if (x + y) % 2 else 0x0C7C, x, y, 0, 'cabbage', 'in rows')
    b.static(0x1036, 15, 7, 0, 'hay', 'garden corner')
    b.static(0x154D, 9, 7, 0, 'water barrel', 'by the house corner, off the path')
    signpost(b, 3, 10, 'Practice farmhouse: cc-P734')
    return b


def bank():
    b = Build('bank', 'a bank: OSI stone shop walls, shingle roof, counter with a banker, vault and a queue carpet')
    k = kit(0x00A0)
    # The shop multi's front row is arches; the plain stone shop set as P720 read it (guide 2.2), windows by the
    # window survey: 0x005E in east-west walls, 0x005D in north-south walls.
    k.update(post=0x005A, corner=0x0059, south=0x0058, east=0x0057, swin=0x005E, ewin=0x005D)
    b.house(k, 2, 2, 10, 8, 0, [0x049C], doors=[(6, 8)], swins=[(4, 2), (8, 2), (3, 8), (9, 8)], ewins=[(2, 5), (10, 5)])
    b.section = 'inside'
    for x in range(3, 10):
        if x != 9:
            b.static(0x0B40, x, 4, 0, 'counter', 'serving side south toward the door; gap at the east end')
    b.static(0x0E41, 4, 3, 0, 'metal chest (vault)', 'behind the counter')
    b.static(0x0E40, 6, 3, 0, 'metal chest (vault)', 'behind the counter')
    b.static(0x0E41, 8, 3, 0, 'metal chest (vault)', 'behind the counter')
    # The banker: a spawner (staff-only, invisible) that keeps one Banker on its tile behind the counter.
    b.lists.setdefault('Spawner (Spawn=Banker; Count=1; HomeRange=0; WalkingRange=0)', []).append((5, 3, 0))
    b.placed.append(('inside', 'Spawner (one Banker, home range 0), 5,3,0, behind the counter'))
    b.static(0x0B26, 3, 7, 0, 'candelabra', 'south-west corner')
    b.static(0x0B26, 9, 7, 0, 'candelabra', 'south-east corner')
    b.static(0x0A0C, 5, 3, 13, 'wall torch', 'north wall (plain piece at 5,2), floor + 13')
    b.static(0x0A0C, 7, 3, 13, 'wall torch', 'north wall (plain piece at 7,2), floor + 13')
    b.static(0x0A07, 3, 6, 13, 'wall torch', 'west wall (plain piece at 2,6), floor + 13')
    b.static(0x0B2C, 9, 6, 0, 'bench', 'for waiting, along the east wall')
    carpet(b, 4, 5, 8, 7, 0)
    shop_sign(b, (6, 8), 0x0C0B, 'Practice Bank')
    signpost(b, 3, 11, 'Practice bank: cc-P734')
    return b


def lodge():
    b = Build('lodge', 'a League lodge: brick under shingles, a long table, bookcases on the north and west walls, banners')
    k = kit(0x0074)
    # 0x0074's slate roof runs the other way; shingles pitched along y from 0x006C, with the brick gable 0x0055.
    r = kit(0x006C)
    k.update(roof_w=r['roof_w'], roof_e=r['roof_e'], ridge=r['ridge'])
    # Windows where no bookcase or hearth stands in front of them (round 1).
    b.house(k, 2, 2, 12, 9, 0, FLAGSTONE, doors=[(7, 9)], swins=[(3, 2), (11, 2), (4, 9), (10, 9)], ewins=[(2, 5), (2, 8), (12, 6)])
    b.section = 'inside'
    b.addon('StoneFireplaceSouthAddon', [(0x0967, -1, 0, 0), (0x0961, 0, 0, 0)], 7, 3, 0, 'fireplace', 'against the north wall, facing south into the room')
    for x in (4, 5, 9, 10):
        b.static(0x0A98, x, 3, 0, 'bookcase', 'backed against the north wall (plain pieces), facing south')
    # Round 2: 0x0A97 faces south like 0x0A98; the east-facing case for a west wall is 0x0A99 (rendered flat on a run).
    for y in (4, 6, 7):
        b.static(0x0A99, 3, y, 0, 'bookcase', 'backed against the west wall (plain pieces), facing east')
    for x in range(6, 10):
        b.static(0x0B90, x, 6, 0, 'long table')
        chairs_at(b, x, 5, 7)
    b.static(0x0FEF, 7, 6, 6, 'book on the table')
    b.static(0x0B26, 11, 4, 0, 'candelabra', 'north-east corner')
    b.static(0x0A0C, 8, 3, 13, 'wall torch', 'north wall (plain piece at 8,2), beside the hearth, floor + 13')
    b.static(0x0A07, 3, 3, 13, 'wall torch', 'west wall (plain piece at 2,3), floor + 13')
    carpet(b, 5, 8, 9, 8, 0)
    b.section = 'outside'
    b.static(0x1589, 13, 4, 8, 'League banner', 'outside the east wall, flat on it, Z 8 (P720)')
    b.static(0x1589, 13, 7, 8, 'League banner', 'outside the east wall, flat on it, Z 8 (P720)')
    shop_sign(b, (7, 9), 0x0BD2, 'Practice League lodge')
    signpost(b, 4, 12, 'Practice lodge: cc-P734')
    return b


# The dock stands on a real lake (round 1: water statics over grass block nothing). The Fold, origin 1550,612: the
# lake's west bank at x 1554 and east bank at x 1573 are land at Z 1 in rows 618-620, the water between is land -15
# under water statics at -5; the south bank is grass at Z 6 from y 633 (plot_scan.py, shore map in the notes).
DOCK_ORIGIN = (1550, 612)


def dock():
    b = Build('dock', 'a plank bridge across a lake and a pier from the south bank, rope rails and posts as OSI lays them')
    b.map_origin = DOCK_ORIGIN
    D = {'planks': (0x07C9, 0x07CD), 'railX': 0x03A6, 'railY': 0x03A9, 'post': ((0x03AE, -5), (0x03A5, 0), (0x03AB, 5)), 'railDz': 5}

    def deck(cells, dz, rail_rows, rail_cols, posts, what):
        for (x, y) in cells:
            b.static(D['planks'][(x + y) % 2], x, y, dz, what + ' plank')
        for (x, y) in cells:
            if (x, y) in posts:
                for tid, off in D['post']:
                    b.static(tid, x, y, dz + off, what + ' post', 'stacked post (P720 isle-sets dock)')
            elif y in rail_rows:
                b.static(D['railX'], x, y, dz + D['railDz'], what + ' rope rail', 'along x, on the outer row, deck + 5')
            elif x in rail_cols:
                b.static(D['railY'], x, y, dz + D['railDz'], what + ' rope rail', 'along y, on the outer column, deck + 5')

    # The bridge: rows 6..8 (618-620), x 4..22 (1554-1572), deck Z 1 (planks 1 high: a walker stands at 2, one above
    # the flat banks' Z 1 at x 1553 and x 1573); rails on the outer rows, posts at the four ends; the walk row is 7.
    # Round 2: the deck began at x 1555 at Z 0 and the walker stuck on x 1554, a bank tile whose corners run from Z 1
    # down to the lake's -15 (a steep slope): the deck now covers it.
    b.section = 'bridge'
    cells = [(x, y) for x in range(4, 23) for y in (6, 7, 8)]
    deck(cells, 1, (6, 8), (), {(4, 6), (4, 8), (22, 6), (22, 8)}, 'bridge')
    # The pier: columns 15..17 (1565-1567), rows 15..20 (627-632), deck Z 5 (a walker stands at 6, the south bank's
    # Z 6); rails on the outer columns and across the free north end, posts at its four corners; the walk column is 16.
    b.section = 'pier'
    cells = [(x, y) for x in (15, 16, 17) for y in range(15, 21)]
    pier_posts = {(15, 15), (17, 15), (15, 20), (17, 20)}
    deck(cells, 5, (), (15, 17), pier_posts, 'pier')
    b.static(D['railX'], 16, 15, 10, 'pier rope rail', 'across the free end, deck + 5')
    b.static(0x14F8, 15, 17, 11, 'coil of rope', 'hung on the west rail')
    b.section = 'banks'
    b.static(0x0E77, 19, 22, 6, 'barrel', 'on the south bank by the pier, off its line')
    b.static(0x0E3D, 20, 22, 6, 'crate', 'on the south bank by the pier')
    b.static(0x0B20, 3, 5, 1, 'lamp post', 'west bank, beside the bridge end, off its line')
    signpost(b, 3, 9, 'Practice bridge: cc-P734', z=1)
    signpost(b, 13, 22, 'Practice pier: cc-P734', z=6)
    return b


def market():
    b = Build('market', 'a market corner: a paved square, three full stalls, a stone fountain, lamps')
    b.section = 'square'
    for x in range(2, 15):
        for y in range(2, 13):
            b.static(PAVERS[(x * 7 + y * 3) % len(PAVERS)], x, y, 0, 'paver', 'mixed variants')
    b.section = 'stalls'
    # Each stall: a counter run with goods on top (fuller piles, round 1), a crate and a barrel behind it, the keeper's
    # side to the north.
    stalls = ((3, (0x0993, 0x09D2, 0x09D1), 'fruit'), (7, (0x097B, 0x0DD6, 0x0DD7), 'fish'), (11, (0x1039, 0x1039, 0x09D3), 'flour and ham'))
    for sx, goods, label in stalls:
        for i in range(3):
            b.static(0x0B40, sx + i, 4, 0, 'counter (%s stall)' % label, 'serving side south, to the square')
            b.static(goods[i], sx + i, 4, 6, '%s on the counter' % label)
        b.static(0x0E3C, sx, 3, 0, 'crate', 'behind the stall')
        b.static(0x0E77, sx + 2, 3, 0, 'barrel', 'behind the stall')
    b.static(0x1036, 13, 2, 0, 'hay', 'behind the flour stall, on the ground')
    b.static(0x1037, 14, 3, 0, 'hay', 'behind the flour stall, on the ground')
    b.section = 'middle'
    # The centrepiece: pinned's StoneFountainAddon (16 pieces 0x1731 on, 4 x 4 round its centre), What to use where.
    fountain = []
    tid = 0x1731
    offs = ((-2, 1), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (1, -2), (0, -2), (0, -1), (0, 0), (-1, 0), (-2, 0), (-2, -1), (-1, -1), (-1, -2), (-2, -2))
    for i, (dx, dy) in enumerate(offs):
        if i == 15:
            tid += 1   # the last component is ++itemID, skipping one (StoneFountainAddon.cs)
        fountain.append((tid, dx, dy, 0))
        tid += 1
    b.addon('StoneFountainAddon', fountain, 9, 8, 0, 'stone fountain', 'round, no facing; x 7..10, y 6..9')
    for x, y in ((2, 2), (14, 12), (2, 12)):
        b.static(0x0B20, x, y, 0, 'lamp post', 'square corner')
    b.static(0x0E3D, 13, 7, 0, 'crate', 'stacked goods by the east edge')
    b.static(0x0E3C, 13, 7, 3, 'crate', 'stacked on the crate below')
    signpost(b, 0, 13, 'Practice market corner: cc-P734')
    return b


def twostory():
    b = Build('twostory', 'a two-story plaster house with a straight stair inside, climbing north to the upper floor')
    k = kit(0x006C)   # plaster under shingles pitched along y (0x0076 pitches the other way)
    k['swin'] = 0x013A   # window survey: 0x013A stands in east-west walls (26 times), 0x013B in north-south ones
    x0, y0, x1, y1 = 2, 2, 9, 8
    # Ground floor walls Z 0, the door in the south wall; the upper storey walls Z 20, the roof on top at Z 40.
    b.house(k, x0, y0, x1, y1, 0, BOARDS, doors=[(4, 8)], swins=[(6, 2), (7, 8)], ewins=[(2, 5), (9, 4)], roof=False)
    b.walls(k, x0, y0, x1, y1, 20, swins=[(4, 2), (4, 8), (7, 8)], ewins=[(2, 5), (9, 5)], storey=' (upper storey)')
    # The stair: four dark wood "north" steps (0x0739, rises toward the north, height 5) at x 8, y 7..4, Z 0, 5, 10,
    # 15, so the top step's top is 20 = the upper floor; blocks 0x0738 under the upper steps where the side shows.
    b.section = 'stairs'
    for i, y in enumerate((7, 6, 5, 4)):
        b.static(0x0739, 8, y, 5 * i, 'stair step', 'dark wood "north" step: climbs toward the north, top at %d' % (5 * i + 5))
        for zb in range(0, 5 * i, 10):
            if zb + 10 <= 5 * i:
                b.static(0x0738, 8, y, zb, 'stair block', 'under the step')
    # Upper floor Z 20, open over the stair's tiles (x 8, y 4..7) except the landing at y 3.
    b.section = 'upper floor'
    for x in range(x0 + 1, x1 + 1):
        for y in range(y0 + 1, y1 + 1):
            if x == 8 and 4 <= y <= 7:
                continue
            b.static(BOARDS[(x + y) % 4], x, y, 20, 'upper floor')
    # Ground floor: no hearth (round 1: a 24-high fireplace comes up through a floor 20 above).
    b.section = 'ground floor'
    b.static(0x0B90, 5, 5, 0, 'table')
    chairs_at(b, 5, 4, 6)
    b.static(0x09D7, 5, 5, 6, 'plate on the table')
    b.static(0x0A0C, 4, 3, 13, 'wall torch', 'north wall (plain piece at 4,2), floor + 13')
    b.static(0x0A07, 3, 6, 13, 'wall torch', 'west wall (plain piece at 2,6), floor + 13')
    b.static(0x0E77, 3, 7, 0, 'barrel', 'south-west corner')
    b.static(0x0E7F, 3, 3, 0, 'keg', 'north-west corner')
    # Upper rooms: the hearth here, on the north wall under the roof's high middle (its top 44 under the roof at 46+).
    b.section = 'upper rooms'
    b.addon('StoneFireplaceSouthAddon', [(0x0967, -1, 0, 0), (0x0961, 0, 0, 0)], 6, 3, 20, 'fireplace', 'against the north wall, facing south, under the high middle of the roof')
    b.addon('SmallBedSouthAddon', [(0x0A63, 0, 0, 0), (0x0A5C, 0, 1, 0)], 3, 3, 20, 'bed', 'head against the north wall, along the west wall')
    b.static(0x0A98, 7, 3, 20, 'bookcase', 'backed against the north wall (plain piece at 7,2), facing south, beside the stair landing')
    b.static(0x0A07, 3, 6, 33, 'wall torch', 'west wall (plain piece at 2,6), upper floor + 13')
    b.static(0x0B2C, 6, 7, 20, 'bench', 'upper room')
    b.roof(k, x0, y0, x1, y1, 40)
    shop_sign(b, (4, 8), 0x0BD2, 'Practice two-story house')
    signpost(b, 1, 10, 'Practice two-story house: cc-P734')
    return b


BUILDS = {'farmhouse': farmhouse, 'bank': bank, 'lodge': lodge, 'dock': dock, 'market': market, 'twostory': twostory}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BUILDS)
    for n in names:
        b = BUILDS[n]()
        b.write()
        b.render()
        if n == 'twostory':
            b.render(below=20, suffix='-ground-floor')
            b.render(below=40, suffix='-upper-floor')
        elif n not in ('dock', 'market'):
            b.render(below=20, suffix='-inside')
        print('%s: %d pieces, %d lists' % (n, sum(len(p) for p in b.lists.values()), len(b.lists)))
