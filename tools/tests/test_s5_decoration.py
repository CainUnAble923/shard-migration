"""cc-P680 (SoS swap S5): the stock decoration [Decorate places on Trammel and Felucca, checked on the SoS land.

    SL_SHARD_REPO=<code copy> SL_SOS_MAP=<overlay> python -P tools/tests/test_s5_decoration.py

SL_SOS_MAP holds the server's map overlay (map1LegacyMUL.uop, statics1.mul, staidx1.mul; docker/uo/Build-MapOverlay.ps1),
which Trammel and Felucca both read (SosMaps.cs). MAPBUILD_CLIENT names the client whose tiledata.mul is read. EA's own
maps (D:\\UO\\UltimaOnlineVanilla) are the stock. The decoration is the code copy's server/data/Decoration/{Britannia,
Trammel,Felucca} when it has them (Decorate-sos-decoration.patch reads them in place of pinned's), else pinned's.
Britannia's cfgs go on both facets.

  1. No item stands in water or void with nothing under it: its tile's land is water, void or cave-mouth land, and
     neither SoS nor a cfg static on that facet has anything on the tile at or below it.
  2. No door hangs outside a doorway (notes/cc-P680-tools/doors.py: a wall on both sides along one axis, the walls
     being SoS's statics and the cfg's own statics on that facet, and nothing impassable on its own tile).
  Facts 1 and 2 leave out stock's own placements: an entry exactly as pinned has it, whose tile and the 8 round it
  are the same on SoS as on its stock map (maps.Map.same_tile), and which fails the same way there.
  3. The shipped cfgs are pinned's, less exactly the entries notes/cc-P680-tools/out-decisions.csv drops, with its
     moves applied, and every row of the CSV gives a reason.
"""
import csv
import glob
import os
import re
import sys
import unittest

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TOOLS = os.path.join(DOCS, 'notes', 'cc-P680-tools')
sys.path.insert(0, TOOLS)
SHARD = os.environ.get('SL_SHARD_REPO', r'D:\ShatteredLegacy')
SOS = os.environ.get('SL_SOS_MAP', '')
READY = bool(SOS) and os.path.exists(os.path.join(SOS, 'staidx1.mul'))
PINNED = r'D:\UO\ModernUO-pinned\Distribution\Data\Decoration'
FOLDERS = ('Britannia', 'Trammel', 'Felucca')
ENTRY = re.compile(r'^\s*(-?\d+)\s+(-?\d+)\s+(-?\d+)(.*)$')


# cc-P683 (S6): the author's dungeon decoration ships beside pinned's decided cfgs; it is not pinned's, and its own
# facts are tools/tests/test_sos_dungeon_decoration.py
OURS = {'sos-dungeons.cfg'}


def read(root):
    """[(folder, file, header, x, y, z, extra)] of every entry of pinned's cfgs, in order."""
    out = []
    for folder in FOLDERS:
        for path in sorted(glob.glob(os.path.join(root, folder, '*.cfg'))):
            if os.path.basename(path) in OURS:
                continue
            header = None
            with open(path, encoding='utf-8') as f:
                for raw in f:
                    s = raw.strip()
                    if not s:
                        header = None
                        continue
                    if s.startswith('#'):
                        continue
                    m = ENTRY.match(s)
                    if m and header is not None:
                        out.append((folder, os.path.basename(path), header, int(m.group(1)), int(m.group(2)),
                                    int(m.group(3)), m.group(4).strip()))
                    else:
                        header = s
    return out


def shipped_root():
    ours = os.path.join(SHARD, 'server', 'data', 'Decoration')
    return ours if os.path.isdir(os.path.join(ours, 'Britannia')) else PINNED


def facets(folder):
    return ('Trammel', 'Felucca') if folder == 'Britannia' else (folder,)


@unittest.skipUnless(READY, 'SL_SOS_MAP (the server map overlay) not set')
class OnSos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import doors
        import maps
        cls.maps, cls.doors = maps, doors
        cls.S = maps.sos(SOS)
        cls.K = {'Trammel': maps.stock('Trammel'), 'Felucca': maps.stock('Felucca')}
        cls.entries = read(shipped_root())
        cls.pinned = read(PINNED)
        cls.pinned_set = set(cls.pinned)
        cls.lay = {f: doors.facet_layout([(e[0], e[2], e[3], e[4], e[5]) for e in cls.entries], f, None)
                   for f in ('Trammel', 'Felucca')}
        cls.stock_lay = {f: doors.facet_layout([(e[0], e[2], e[3], e[4], e[5]) for e in cls.pinned], f, None)
                         for f in ('Trammel', 'Felucca')}

    def untouched(self, e, facet):
        """Exactly as pinned has it, on land SoS left alone (against the stock map that entry was made for)."""
        stock = self.K['Felucca' if e[0] == 'Felucca' else 'Trammel']
        return e in self.pinned_set and all(self.S.same_tile(stock, e[3] + dx, e[4] + dy)
                                            for dx in (-1, 0, 1) for dy in (-1, 0, 1))

    def stranded(self, M, extra, x, y, z):
        if M.land_kind(x, y) not in ('water', 'void', 'ignored'):
            return None
        under = [sz for sz, _ in M.statics(x, y) + extra.get((x, y), []) if sz <= z]
        return None if under else M.land_kind(x, y)

    def test_1_no_item_in_water_or_void(self):
        bad, quirks = [], 0
        for e in self.entries:
            for f in facets(e[0]):
                why = self.stranded(self.S, self.lay[f][1], e[3], e[4], e[5])
                if not why:
                    continue
                stock = self.K['Felucca' if e[0] == 'Felucca' else 'Trammel']
                if self.untouched(e, f) and self.stranded(stock, self.stock_lay[f][1], e[3], e[4], e[5]):
                    quirks += 1
                    continue
                bad.append('%s %s/%s %s at %d,%d,%d: %s' % (f, e[0], e[1], e[2][:30], e[3], e[4], e[5], why))
        print('\n  entries', len(self.entries), 'stock quirks', quirks, 'in water or void', len(bad))
        for b in bad[:40]:
            print('   ', b)
        self.assertEqual([], bad)

    def test_2_no_door_outside_a_doorway(self):
        bad, quirks, n = [], 0, 0
        for e in self.entries:
            if not self.doors.is_door(e[2]):
                continue
            for f in facets(e[0]):
                n += 1
                d, extra = self.lay[f]
                ok, why = self.doors.in_doorway(self.S, e[3], e[4], e[5], d, extra)
                if ok:
                    continue
                stock = self.K['Felucca' if e[0] == 'Felucca' else 'Trammel']
                sd, sextra = self.stock_lay[f]
                if self.untouched(e, f) and not self.doors.in_doorway(stock, e[3], e[4], e[5], sd, sextra)[0]:
                    quirks += 1
                    continue
                bad.append('%s %s/%s %s at %d,%d,%d: %s' % (f, e[0], e[1], e[2][:30], e[3], e[4], e[5], why))
        print('\n  door placements', n, 'stock quirks', quirks, 'outside a doorway', len(bad))
        for b in bad[:40]:
            print('   ', b)
        self.assertEqual([], bad)


class Csv(unittest.TestCase):
    def test_3_every_dropped_and_moved_entry_is_in_the_csv_with_its_reason(self):
        root = shipped_root()
        self.assertNotEqual(PINNED, root, 'the code copy ships no decided decoration (server/data/Decoration)')
        pinned = read(PINNED)
        rows = list(csv.DictReader(open(os.path.join(TOOLS, 'out-decisions.csv'), encoding='utf-8')))
        self.assertTrue(all(r['reason'].strip() for r in rows), 'a row without a reason')
        dropped = {(r['folder'], r['file'], r['item'], int(r['x']), int(r['y']), int(r['z']))
                   for r in rows if r['action'] == 'dropped'}
        moved = {(r['folder'], r['file'], r['item'], int(r['x']), int(r['y']), int(r['z'])):
                 (int(r['new_x']), int(r['new_y']), int(r['new_z'])) for r in rows if (r['new_x'], r['new_y'], r['new_z'])
                 != (r['x'], r['y'], r['z']) and r['action'] != 'dropped'}
        want = []
        for e in pinned:
            k = e[:6]
            if k in dropped:
                continue
            if k in moved:
                e = e[:3] + moved[k] + e[6:]
            want.append(e)
        got = read(root)
        self.assertEqual(len(want), len(got))
        self.assertEqual(sorted(want), sorted(got))


if __name__ == '__main__':
    unittest.main(verbosity=2)
