r"""cc-P687 (SoS swap S14): the fences and the seam dressing, checked on the Siege of Sosaria land.

The code copy's facts (each fence registered on both facets, refusing a step, a landing and every spell that ends inside,
boats sailing by, no housing) are its SosFenceRegionsVerification. These need the map:

  1. Each fence in the code copy's SosFenceRegions.cs is notes/cc-P687-tools/fences.py's: the same rectangles and the
     same turn-back spot, and that spot is standable on SoS (P681's walk grid), outside every fence, on a walkable area
     of at least 20,000 tiles (the mainland or a big island).
  2. Nothing a player needs is inside a fence: no end of a shipped teleporter (teleporters-sos.json), no shipped
     spawner (server/data/Spawns), no decoration line (server/data/Decoration), no public moongate, no guarded town.
  3. The author's dungeons: the only walk-in ways (a standable tile inside one of his dungeon regions a step from a
     standable tile outside all of them, dungeon_ways_in.py) that lead anywhere are the Swamp of Desolation's, and every
     one of those is inside its fence. The rest are reached only by the teleporters S6 left out.
  4. The dressing (dress.py) in the code copy's trammel.mapops: every one of its boulders stands on a target seam tile
     (seamgrid.py), at the low neighbour's Z plus a multiple of 20, its top at least 2 under the tile's walking Z, so no
     tile's walkability changes; more than 6,000 faces are dressed; the patch is under 5 MB; and applied to the
     pristine SoS copy (SL_SOS_BASE) it reports 0 drifted blocks and 0 missing removals (mapops apply).

    set SL_SHARD_REPO=<code copy>  SL_SOS_BASE=<pristine SoS folder: map1LegacyMUL.uop, statics1.mul, staidx1.mul>
    python -P tools/tests/test_sos_fences.py
SL_MAPOPS and SL_FENCES_CODE (red runs) point fact 4 at another patch and facts 1-3 at another SosFenceRegions.cs. Skipped when an input is missing.
"""
import csv
import glob
import json
import os
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(HERE))
TOOLS = os.path.join(DOCS, 'notes', 'cc-P687-tools')
sys.path.insert(0, TOOLS)
sys.path.insert(0, os.path.join(DOCS, 'scripts'))

SHARD = os.environ.get('SL_SHARD_REPO', r'D:\ShatteredLegacy')
BASE = os.environ.get('SL_SOS_BASE', '')
MAPOPS = os.environ.get('SL_MAPOPS') or os.path.join(SHARD, 'player-package', 'vendor', 'shattered-legacy-map', 'trammel.mapops')
CODE = os.environ.get('SL_FENCES_CODE') or os.path.join(SHARD, 'server', 'customizations', 'Regions', 'SosFenceRegions.cs')
READY = os.path.exists(CODE) and os.path.exists(os.path.join(BASE, 'staidx1.mul'))
BOULDERS = {0x1357, 0x1358, 0x1359, 0x135A, 0x135B, 0x135C}

_cache = {}


def grid():
    if 'g' not in _cache:
        import sosgrid
        _cache['g'] = sosgrid.load()
    return _cache['g']


def code_fences():
    """(name, [rects], turnBack) from the code copy's Fences table."""
    s = open(CODE, encoding='utf-8').read()
    body = s[s.index('public static readonly Fence[] Fences'):s.index('];', s.index('public static readonly Fence[] Fences'))]
    out = []
    for m in re.finditer(r'new\(\s*"([^"]+)",\s*\[(.*?)\],\s*new Point3D\((-?\d+), (-?\d+), (-?\d+)\)', body, re.S):
        rects = [tuple(int(v) for v in q) for q in re.findall(r'\((\d+), (\d+), (\d+), (\d+)\)', m[2])]
        out.append((m[1], rects, (int(m[3]), int(m[4]), int(m[5]))))
    return out


def in_fence(fences, x, y):
    return [n for n, rs, _ in fences if any(a <= x <= c and b <= y <= d for a, b, c, d in rs)]


@unittest.skipUnless(READY, 'needs SL_SHARD_REPO with SosFenceRegions.cs and SL_SOS_BASE (the pristine SoS copy)')
class Fences(unittest.TestCase):
    def test_1_each_fence_and_its_turn_back_spot(self):
        import fences as F
        import sosgrid
        code = code_fences()
        tool = json.load(open(os.path.join(TOOLS, 'out', 'fences.json')))
        self.assertEqual(6, len(code))
        self.assertEqual([[tuple(q) for q in f['rects']] for f in tool], [rs for _, rs, _ in code])
        self.assertEqual([tuple(f['turnBack']) for f in tool], [tb for _, _, tb in code])
        stand = grid()['stand']
        for name, _, (x, y, z) in code:
            self.assertNotEqual(sosgrid.NONE, stand[x, y], name)
            self.assertEqual(z, int(stand[x, y]), name)
            self.assertEqual([], in_fence(code, x, y), name)
            self.assertGreaterEqual(F.component_size(stand, x, y), F.BIG, name)

    def test_2_nothing_a_player_needs_is_inside(self):
        code = code_fences()
        data = os.path.join(SHARD, 'server', 'data')
        bad = []
        for t in json.load(open(os.path.join(data, 'teleporters-sos.json'), encoding='utf-8')):
            for k in ('src', 'dst'):
                if t[k]['map'] in ('Trammel', 'Felucca') and in_fence(code, *t[k]['loc'][:2]):
                    bad.append(('teleporter', k, t[k]['loc']))
        spawners = 0
        for p in glob.glob(os.path.join(data, 'Spawns', '**', '*.json'), recursive=True):
            for m in re.finditer(r'"location"\s*:\s*\[\s*(\d+)\s*,\s*(\d+)', open(p, encoding='utf-8').read()):
                spawners += 1
                if in_fence(code, int(m[1]), int(m[2])):
                    bad.append(('spawner', os.path.basename(p), m[1], m[2]))
        deco = 0
        for p in glob.glob(os.path.join(data, 'Decoration', '**', '*.cfg'), recursive=True):
            if os.path.basename(os.path.dirname(p)) == 'Builds':
                continue   # cc-P734: saved builds, coordinates relative to their own corner, placed by [PlaceBuild
            for m in re.finditer(r'^(\d+)\s+(\d+)\s+-?\d+', open(p, encoding='utf-8', errors='replace').read(), re.M):
                deco += 1
                if in_fence(code, int(m[1]), int(m[2])):
                    bad.append(('decoration', os.path.relpath(p, data), m[1], m[2]))
        import seams
        for x, y in seams.MOONGATES:
            if in_fence(code, x, y):
                bad.append(('moongate', x, y))
        for name, (x1, y1, x2, y2) in seams.towns(SHARD):
            for n, rs, _ in code:
                if any(a <= x2 - 1 and x1 <= c and b <= y2 - 1 and y1 <= d for a, b, c, d in rs):
                    bad.append(('town', name, n))
        self.assertGreater(spawners, 500)
        self.assertGreater(deco, 20000)
        self.assertEqual([], bad)

    def test_3_the_only_walk_in_dungeon_is_fenced(self):
        import collections
        import numpy as np
        import dungeon_ways_in as D
        import sosgrid
        stand = grid()['stand'].astype(np.int32)
        code = code_fences()
        dungeons = D.his_dungeons(SHARD)
        own = np.zeros(stand.shape, bool)
        for _, rects in dungeons:
            for x1, y1, x2, y2 in rects:
                own[x1:x2, y1:y2] = True

        def reach(x, y, cap=200):
            seen = {(x, y)}
            q = collections.deque([(x, y)])
            while q and len(seen) < cap:
                a, b = q.popleft()
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        c, d = a + dx, b + dy
                        if (c, d) in seen or own[c, d] or stand[c, d] == sosgrid.NONE or abs(stand[c, d] - stand[a, b]) > D.STEP:
                            continue
                        seen.add((c, d))
                        q.append((c, d))
            return len(seen)

        ways = collections.defaultdict(list)
        owner = {}
        for i, (n, rects) in enumerate(dungeons):
            for x1, y1, x2, y2 in rects:
                for x in range(x1, x2):
                    for y in (y1, y2 - 1):
                        owner.setdefault((x, y), n)
                for y in range(y1, y2):
                    for x in (x1, x2 - 1):
                        owner.setdefault((x, y), n)
        for (x, y), n in owner.items():
            if stand[x, y] == sosgrid.NONE:
                continue
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    ox, oy = x + dx, y + dy
                    if own[ox, oy] or stand[ox, oy] == sosgrid.NONE or abs(stand[ox, oy] - stand[x, y]) > D.STEP:
                        continue
                    if reach(ox, oy) >= 200:   # the outside tile leads somewhere (not a sliver past a rect's edge)
                        ways[n].append((x, y))
        self.assertEqual(['Swamp of Desolation'], sorted(ways))
        self.assertEqual([], [p for p in ways['Swamp of Desolation'] if 'Sealed: the Swamp of Desolation' not in in_fence(code, *p)])

    def test_4_the_dressing(self):
        import numpy as np
        import seamgrid
        import sosgrid
        from mapbuild import mapops
        text = open(MAPOPS, encoding='ascii').read()
        self.assertLess(len(text.encode()), 5 * 1024 * 1024)
        g = seamgrid.build(SHARD)
        zs = g['zs'].astype(np.int32)
        stand = grid()['stand']
        lines = [l.split() for l in text.splitlines() if l.startswith('S+ ')]
        ours = [tuple(int(v) for v in l[1:5]) for l in lines if int(l[1]) < 5120 and int(l[4]) in BOULDERS]
        faces = {(x, y) for x, y, _, _ in ours}
        self.assertGreater(len(faces), 6000)
        bad = []
        for x, y, z, tid in ours:
            low = min(int(zs[x + dx, y + dy]) for dx, dy in ((0, 1), (1, 0), (1, 1)))
            top = int(stand[x, y]) if stand[x, y] != sosgrid.NONE else int(zs[x, y])
            if not g['target'][x, y] or (z - low) % 20 or z + 5 > top - 2:
                bad.append((x, y, z, hex(tid)))
        self.assertEqual([], bad[:20])
        with tempfile.TemporaryDirectory() as out:
            drifted, missing = mapops.apply(text, BASE, out, 1)
        self.assertEqual(([], []), (drifted, missing))


if __name__ == '__main__':
    unittest.main(verbosity=2)
