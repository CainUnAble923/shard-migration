"""cc-P688 (SoS swap S15): the walk between places on the SoS land, and the play-test bot's points on it.

  1. The step rule (notes/cc-P688-tools/walkgrid.py: pinned Movement.cs reduced to the files), on small made-up grids:
     a slope of 2 a tile walks both ways; a 3 rise is refused up and allowed down; on a land slope the step is measured
     from the tile's top corner to the next tile's low corner (GetStartZ zTop, Check landZ), so a hill whose centres rise
     4 a tile still climbs; a bridge is stepped onto from its base Z (itemTop = z) and stood on at half its height; a
     player's diagonal past a blocked side is refused.
  2. Every fixed point the bot and the isle route use (bot_points.py) is standable on the SoS land with the shipped
     trammel.mapops applied, the points one check walks between share one walk area, and T-039 measures from the board
     where HavenSpots.QuestBoard puts it.
  3. The reachability table (verify.py: walkgrid.py's whole-map groups, then every pair of groups within 300 tiles
     walked exactly, both ways, with exact.py): the groups of banks, moongates and docks that reach each other on foot
     are the notes' table (out/table-groups.csv; SL_TABLE points at another copy for a red run).

    set SL_SHARD_REPO=<code copy>  SL_SOS_BASE=<pristine SoS folder: map1LegacyMUL.uop, statics1.mul, staidx1.mul>
    python -P tools/tests/test_sos_walk.py
Facts 2 and 3 build the whole map's grid (about 15 minutes each, the labels cached in %TEMP%); skipped without the
inputs. SL_WALKGRID points fact 1 at another walkgrid.py (red runs).
"""
import csv
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(HERE))
TOOLS = os.path.join(DOCS, 'notes', 'cc-P688-tools')
SHARD = os.environ.get('SL_SHARD_REPO', r'D:\ShatteredLegacy')
BASE = os.environ.get('SL_SOS_BASE', '')
MAPOPS = os.path.join(SHARD, 'player-package', 'vendor', 'shattered-legacy-map', 'trammel.mapops')
READY = os.path.exists(os.path.join(BASE, 'staidx1.mul')) and os.path.exists(MAPOPS)


def walkgrid():
    sys.path.insert(0, TOOLS)
    path = os.environ.get('SL_WALKGRID') or os.path.join(TOOLS, 'walkgrid.py')
    spec = importlib.util.spec_from_file_location('walkgrid_under_test', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Rules(unittest.TestCase):
    def setUp(self):
        self.g = walkgrid()

    def walk(self, stand, low=None, top=None):
        stand = np.array(stand, dtype=np.int16)
        low = stand if low is None else np.array(low, dtype=np.int16)
        top = stand if top is None else np.array(top, dtype=np.int16)
        can = self.g.steps(stand, low, top)
        return can, self.g.areas(can)[0]

    def east(self, can, x, y):
        return bool(can[self.g.DIRS8.index((1, 0))][x, y])

    def west(self, can, x, y):
        return bool(can[self.g.DIRS8.index((-1, 0))][x, y])

    def test_1_steps(self):
        # x runs down the rows: a slope of 2 a tile, then a 3 rise
        can, lab = self.walk([[0, 0], [2, 2], [4, 4], [7, 7]])
        self.assertEqual(lab[0, 0], lab[2, 0], 'a slope of 2 a tile walks both ways')
        self.assertFalse(self.east(can, 2, 0), 'a 3 rise is refused up')
        self.assertTrue(self.west(can, 3, 0), 'and allowed down')
        self.assertNotEqual(lab[2, 0], lab[3, 0])
        # a land hill: centres rise 4 a tile, but each tile's top corner is 2 under the next one's low corner
        stand = [[0, 0], [4, 4], [8, 8]]
        low = [[-2, -2], [2, 2], [6, 6]]
        top = [[2, 2], [6, 6], [10, 10]]
        can, lab = self.walk(stand, low, top)
        self.assertEqual(lab[0, 0], lab[2, 0], 'a land hill climbs corner to corner')
        # a bridge: stood on at 10 (half of 20 over z 0), stepped onto from its base z 0
        can, lab = self.walk([[0, 0], [10, 10], [10, 10]], low=[[0, 0], [0, 0], [10, 10]], top=[[0, 0], [20, 20], [10, 10]])
        self.assertTrue(self.east(can, 0, 0), 'onto a bridge from its base')
        # a diagonal past a blocked side: (0,0) to (1,1) with (0,1) nowhere to stand; open once both sides are
        N = self.g.NONE
        se = self.g.DIRS8.index((1, 1))
        can, lab = self.walk([[0, N], [0, 0]])
        self.assertFalse(bool(can[se][0, 0]), 'no corner cutting past one blocked side')
        can, lab = self.walk([[0, 0], [0, 0]])
        self.assertTrue(bool(can[se][0, 0]), 'the diagonal with both sides open')


@unittest.skipUnless(READY, 'needs SL_SHARD_REPO and SL_SOS_BASE')
class OnTheLand(unittest.TestCase):
    def test_2_bot_points(self):
        sys.path.insert(0, os.path.join(DOCS, 'scripts'))
        work = os.environ.get('P688_PATCHED') or tempfile.mkdtemp(prefix='p688-patched-')
        if not os.path.exists(os.path.join(work, 'staidx1.mul')):
            from mapbuild import mapops
            mapops.apply(open(MAPOPS, encoding='utf-8').read(), BASE, work, 1)
        r = subprocess.run([sys.executable, '-P', os.path.join(TOOLS, 'bot_points.py'), SHARD, work],
                           capture_output=True, text=True)
        bad = [l for l in r.stdout.splitlines() if l.startswith('BAD')]
        self.assertEqual([], bad, r.stdout[-3000:] + r.stderr[-2000:])
        self.assertEqual(0, r.returncode, r.stderr[-2000:])

    def test_3_reachability_table(self):
        sys.path.insert(0, TOOLS)
        import verify
        rows, final, _ = verify.table(SHARD, say=lambda s: None)
        got = sorted(sorted('%s %s' % (rows[j]['kind'], rows[j]['name']) for j in grp) for grp in final)
        want = {}
        with open(os.environ.get('SL_TABLE') or os.path.join(TOOLS, 'out', 'table-groups.csv'), encoding='utf-8') as f:
            for row in csv.DictReader(f):
                want.setdefault(row['group'], []).append('%s %s' % (row['kind'], row['name']))
        self.assertEqual(sorted(sorted(v) for v in want.values()), got)


SCRATCH = os.path.join(DOCS, 'notes', 'cc-P481-tools', 'scratch', 'sos', 'Statics1.mul')


@unittest.skipUnless(os.path.exists(SCRATCH), 'needs P481\'s SoS scratch copy')
class Exact(unittest.TestCase):
    def exact(self):
        sys.path.insert(0, TOOLS)
        path = os.environ.get('SL_EXACT') or os.path.join(TOOLS, 'exact.py')
        spec = importlib.util.spec_from_file_location('exact_under_test', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_4_the_exact_walk_where_one_level_a_tile_is_not_enough(self):
        e = self.exact()
        # Papua's bank (z14 floor on z13 logs over the dirt) to Papua's docks: out the door onto the lower logs
        ok, steps, near, _ = e.walk((5600, 3080, 5900, 3300), (5669, 3131, 14), (5825, 3256))
        self.assertTrue(ok, 'Papua bank to its docks; nearest %s' % (near,))
        # Fort Yondall's bank to the road south of the fort: up the gatehouse stairs to z20 and down outside
        ok, steps, near, _ = e.walk((3250, 200, 3550, 500), (3393, 337, 0), (3330, 420))
        self.assertTrue(ok, 'Fort Yondall bank to outside; nearest %s' % (near,))
        # and the fort's gate itself is static doors (0x06C5, 0x06C7): no walk straight through it
        ok, steps, near, _ = e.walk((3383, 378, 3390, 386), (3386, 380, 0), (3386, 384))
        self.assertFalse(ok, 'through the static gate')


if __name__ == '__main__':
    unittest.main(verbosity=2)
