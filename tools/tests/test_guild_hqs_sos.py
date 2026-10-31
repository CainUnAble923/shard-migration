"""cc-P708: the headquarters moved onto the Siege of Sosaria land (Chase's picks of 2026-10-27 from P704; the places are
Zigholtul's) stand on dry, reachable ground on the SoS file the server reads.

    SL_SHARD_REPO=<code copy> python -P tools/tests/test_guild_hqs_sos.py

The land is notes/cc-P708-tools/p281sos (P281's hall tools copied by make_p281sos.py: their client folder on today's SoS
overlay from make_sosclient.py, our decoration and the SoS spawners). Skips when that folder is missing. The walk is P281's
(walk.py: every standable height per tile, so it walks up into a two-storey house; doors passable; a step of 3; and,
in the P708 copy, sloped land climbed as pinned Movement.Check climbs it).

  1. The six moved halls are where Chase picked (Valunstead twice, Fort Whitestone, Fort Viridian, Hammerhill twice),
     read from the design file.
  2. Each moved hall's guildmaster tile and travel stop are standable at their Z and not water; the travel stop is
     under open sky; the sign's tile is not water, and has a wall or other blocking piece on it or beside it to hang on.
  3. Each moved hall's guildmaster is reached on foot from its travel stop, and the travel stop is reached on foot from
     the town's bank (Valunstead's and Hammerhill's, the author's Bank points) or, for the two forts, from the author's
     Yew Forest Guardpost (1047,1080), so a player walks in from the land around.
  4. (cc-P750) Each moved hall's guildmaster shows in the game's camera: at most a quarter of a standing figure's screen
     box (20 by 60 pixels above his tile) is covered by the art drawn after his tile (larger x + y), from the art's own
     pixels. As the client does, a static at or above the first one over his head on his tile (a roof, a floor above) is
     left out. P708's Rangers post in Fort Viridian's south court (1003,1004) was wholly covered by the rampart in front
     of it; neither the guildmaster nor the Tester showed in P708's shots.
  5. (cc-P750) Each moved hall's sign shows: at most a quarter of its own art's pixels (the board the server places,
     0x0B95 + 2 x SignType + facing) is covered by the art drawn after it (a larger x + y, or a higher piece on its own
     tile). P708's League sign beside the keep's steps (566,321) was wholly covered by them, and the Tinkers' (1494,1026)
     half covered by the house south-east of it; neither showed in P708's shots.
"""
import json
import os
import sys
import unittest

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TOOLS = os.path.join(DOCS, 'notes', 'cc-P708-tools', 'p281sos')
SHARD = os.environ.get('SL_SHARD_REPO', r'D:\ShatteredLegacy')
PLAN = os.environ.get('HALLS_JSON', os.path.join(SHARD, 'design', 'guild-halls', 'halls.json'))
READY = os.path.exists(os.path.join(TOOLS, 'walk.py'))

PICKS = {'league': 'Valunstead', 'merchants': 'Valunstead', 'healers': 'Fort Whitestone',
         'rangers': 'Fort Viridian', 'custodians': 'Hammerhill', 'tinkers': 'Hammerhill'}
# where a player comes from: the author's points (notes/sos-map-author-spots.md)
FROM = {'Valunstead': (484, 434, 15), 'Hammerhill': (1530, 994, 5),
        'Fort Whitestone': (1047, 1080, 0), 'Fort Viridian': (1047, 1080, 0)}
# the walk's box per place: Valunstead's island (P688's group 7, 234-655 by 180-499; its keep is joined to the lower
# town round the west), the Yew forest round the two forts, Hammerhill inside its walls
BOX = {'Valunstead': (234, 180, 655, 499), 'Hammerhill': (1470, 950, 1630, 1080),
       'Fort Whitestone': (760, 900, 1200, 1200), 'Fort Viridian': (760, 900, 1200, 1200)}


def halls():
    return {h['key']: h for h in json.load(open(PLAN, encoding='utf-8'))['halls']}


SHOWS = 0.25   # fact 4: the most of a guildmaster's figure the art in front of him may cover


def pt(d):
    return d['x'], d['y'], d['z']


@unittest.skipUnless(READY, 'run notes/cc-P708-tools/make_sosclient.py and make_p281sos.py first')
class GuildHqsOnSos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, TOOLS)
        global H, Walk
        import hallbase as H  # noqa: F401
        from walk import Walk
        cls.H = halls()

    def walk(self, *pts, pad=8):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return Walk(1, (min(xs), min(ys), max(xs), max(ys)), pad=pad)

    @staticmethod
    def at(W, p, slack=0):
        """The standable height at p within slack of its Z, or None."""
        hs = [h for h in W.heights(p[0], p[1]) if abs(h - p[2]) <= slack]
        return min(hs, key=lambda h: abs(h - p[2])) if hs else None

    def test_1_the_six_halls_are_where_chase_picked(self):
        for key, town in PICKS.items():
            h = self.H[key]
            self.assertEqual(town, h['town'], key)
            self.assertEqual(1, h['facet'], key)
            self.assertIn('Zigholtul', h['building_name'], key)

    def test_2_guildmaster_sign_and_stop_on_dry_ground(self):
        bad = []
        for key in PICKS:
            h = self.H[key]
            npc, stop, sign = pt(h['npc']), pt(h['travel']), pt(h['sign'])
            W = self.walk(npc, stop, sign)
            for name, p in (('npc', npc), ('travel', stop)):
                lid = W.F.land(p[0], p[1])[0]
                if self.at(W, p) is None:
                    bad.append('%s %s %s: not standable at its z (heights %s)' % (key, name, p, W.heights(p[0], p[1])))
                elif H.LAND[lid][0] & H.WET and not any(H.iflags(s[0]) & H.SURF for s in W.F.statics(p[0], p[1])):
                    bad.append('%s %s %s: water' % (key, name, p))
            if self.at(W, stop) is not None and W.F.roof_over(stop[0], stop[1], self.at(W, stop)):
                bad.append('%s travel %s: under a roof' % (key, stop))
            lid = W.F.land(sign[0], sign[1])[0]
            if H.LAND[lid][0] & H.WET:
                bad.append('%s sign %s: water' % (key, sign))
            hang = any(H.iflags(s[0]) & (H.WALL | H.IMP)
                       for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                       for s in W.F.statics(sign[0] + dx, sign[1] + dy) if abs(s[1] - sign[2]) <= 20)
            if not hang:
                bad.append('%s sign %s: nothing to hang on' % (key, sign))
        self.assertEqual([], bad)

    def test_3_reached_on_foot(self):
        bad = []
        for key, town in PICKS.items():
            h = self.H[key]
            npc, stop = pt(h['npc']), pt(h['travel'])
            start = FROM[town]
            W = Walk(1, BOX[town], pad=0)
            s = (stop[0], stop[1], self.at(W, stop))
            reach = W.flood(s)
            beside = [(npc[0] + dx, npc[1] + dy, hh) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy
                      for hh in W.heights(npc[0] + dx, npc[1] + dy) if abs(hh - npc[2]) <= 3]
            if not any(t in reach for t in beside):
                bad.append('%s: guildmaster %s not reached from the stop %s' % (key, npc, stop))
            g = self.at(W, start, slack=5)
            if g is None or (start[0], start[1], g) not in reach:
                bad.append('%s: the stop %s and %s (%s) are not joined on foot' % (key, stop, start, town))
            print('  %-10s stop %s: %d tiles reached; guildmaster and %s reached' % (key, stop, len(reach), town))
        self.assertEqual([], bad)


    def test_4_guildmaster_shows_in_the_camera(self):
        import numpy as np
        # hallbase (imported in setUpClass) has pointed uofiles.CLIENT at the SoS client folder; isorender reads its
        # tiledata from there, and the art too
        os.environ.setdefault('MAPBUILD_ART', H.CLIENT)
        from mapbuild import isorender as iso
        art = iso.Art(art_folder=H.CLIENT, client=H.CLIENT)
        bad = []
        for key in PICKS:
            x, y, z = pt(self.H[key]['npc'])
            covered = figure_covered(iso, art, np, x, y, z)
            print('  %-10s guildmaster %s: %.0f%% covered' % (key, (x, y, z), covered * 100))
            if covered > SHOWS:
                bad.append('%s: the guildmaster at %s is %.0f%% covered by the art in front of him' % (key, (x, y, z), covered * 100))
        self.assertEqual([], bad)


    def test_5_sign_shows_in_the_camera(self):
        import re
        import numpy as np
        os.environ.setdefault('MAPBUILD_ART', H.CLIENT)
        from mapbuild import isorender as iso
        art = iso.Art(art_folder=H.CLIENT, client=H.CLIENT)
        src = open(os.path.join(H.PINNED, 'Projects', 'UOContent', 'Items', 'Construction', 'Signs', 'Sign.cs'),
                   encoding='utf-8').read()
        body = src[src.index('enum SignType'):]
        body = re.sub(r'//.*', '', body[body.index('{') + 1:body.index('}')])
        names = [n.strip() for n in body.split(',') if n.strip()]
        bad = []
        for key in PICKS:
            s = self.H[key]['sign']
            tid = 0xB95 + 2 * names.index(s['type']) + (1 if s['facing'] == 'West' else 0)
            board = np.array(art.static(tid))[:, :, 3] > 0
            covered = covered_share(iso, art, np, s['x'], s['y'], s['z'], board, same_tile_above=True)
            print('  %-10s sign %s 0x%04X: %.0f%% covered' % (key, (s['x'], s['y'], s['z']), tid, covered * 100))
            if covered > SHOWS:
                bad.append('%s: the sign at %s is %.0f%% covered by the art in front of it' % (key, (s['x'], s['y'], s['z']), covered * 100))
        self.assertEqual([], bad)


def covered_share(iso, art, np, x, y, z, mask, same_tile_above=False, roof=None):
    """The share of mask's pixels (an art-sized picture standing on (x, y, z), anchored as the client anchors art) that
    the art drawn after it covers: a larger x + y, or (same_tile_above) a higher piece on its own tile. Pieces at or
    above roof are left out, as the client leaves a roof out over the player."""
    sc = iso.Scene.from_map(H.CLIENT, 1, x - 1, y - 1, x + 16, y + 16)
    mh0, mw0 = mask.shape
    left0, top0 = (x - y) * 22 + 22 - mw0 // 2, (x + y) * 22 + 44 - mh0 - z * 4
    cov = np.zeros_like(mask)
    for sx, sy, sz, tid in sc.statics:
        later = sx + sy > x + y or (same_tile_above and (sx, sy) == (x, y) and sz > z)
        if not later or (roof is not None and sz >= roof):
            continue
        im = art.static(tid)
        if im is None:
            continue
        m = np.array(im)[:, :, 3] > 0
        mh, mw = m.shape
        left, top = (sx - sy) * 22 + 22 - mw // 2, (sx + sy) * 22 + 44 - mh - sz * 4
        a0, b0 = max(left0, left), max(top0, top)
        a1, b1 = min(left0 + mw0, left + mw), min(top0 + mh0, top + mh)
        if a0 < a1 and b0 < b1:
            cov[b0 - top0:b1 - top0, a0 - left0:a1 - left0] |= m[b0 - top:b1 - top, a0 - left:a1 - left]
    return float((cov & mask).sum()) / float(mask.sum())


def figure_covered(iso, art, np, x, y, z):
    """The share of a standing figure's 20 x 60 pixel box at (x, y, z) that the art drawn after it covers."""
    sc = iso.Scene.from_map(H.CLIENT, 1, x - 1, y - 1, x + 16, y + 16)
    over = [s[2] for s in sc.statics if (s[0], s[1]) == (x, y) and s[2] > z + 10]
    roof = min(over) if over else None
    cx, feet = (x - y) * 22 + 22, (x + y) * 22 + 22 - z * 4
    left0, top0, w, h = cx - 10, feet - 60, 20, 60
    cov = np.zeros((h, w), bool)
    for sx, sy, sz, tid in sc.statics:
        if sx + sy <= x + y or (roof is not None and sz >= roof):
            continue
        im = art.static(tid)
        if im is None:
            continue
        m = np.array(im)[:, :, 3] > 0
        mh, mw = m.shape
        left, top = (sx - sy) * 22 + 22 - mw // 2, (sx + sy) * 22 + 44 - mh - sz * 4
        a0, b0 = max(left0, left), max(top0, top)
        a1, b1 = min(left0 + w, left + mw), min(top0 + h, top + mh)
        if a0 < a1 and b0 < b1:
            cov[b0 - top0:b1 - top0, a0 - left0:a1 - left0] |= m[b0 - top:b1 - top, a0 - left:a1 - left]
    return float(cov.mean())


if __name__ == '__main__':
    unittest.main(verbosity=2)
