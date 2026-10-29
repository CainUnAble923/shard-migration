"""cc-P676 (SoS swap S3): Trammel's regions on the Siege of Sosaria land, checked on the map.

    SL_SHARD_REPO=<code copy> SL_SOS_MAP=<SoS map folder> python -P tools/tests/test_regions_sos.py

SL_SOS_MAP holds map1LegacyMUL.uop, statics1.mul and staidx1.mul: the SoS base with the code copy's trammel.mapops,
as the server reads it (docker/uo/Build-MapOverlay.ps1 writes one). The regions are the code copy's
server/data/regions-trammel.json (notes/cc-P676-tools/gen_regions.py). The server's own facts (names, types, the
loader) are in its SosTrammelRegionsVerification. Skipped when either input is missing.

  1. Every rect of every region lies on dry SoS land or its own water: it holds dry land or a built static (a dock, a
     pier), or touches a rect of the same region that holds dry land (a town's harbour, an isle's shore). A rect that is
     not a dungeon's is not mostly void; a dungeon's is not mostly water and has some floor.
  2. No guard zone this prompt drew covers open wild: each open-wild 8 x 8 block (all dry, nothing built) of a guarded
     region redrawn from the author or new here is enclosed by the town, or within 3 blocks (24 tiles) of a built block
     of that zone (gen_regions.peel_to_town joins built blocks up to 2 apart, then adds a margin of 1).
     Pinned's own guarded regions, kept where their land changed under 25 percent (or clipped to such rects: the
     moongates' zones), are pinned's and are only counted.
  3. The 7 new towns, Glimmerwood and the Nujel'm desert each cover dry land (over half of each is dry).

cc-P686 (SoS swap S13): Felucca reads Trammel's files (P675), so its regions stand on the same land. The same three
facts run on the code copy's server/data/regions-felucca.json (notes/cc-P686-tools/gen_felucca.py), with its own
decision log (SL_REGIONS_FELUCCA for a red run), and two more need no map:
  4. The towns match: every region named in both files has the same rects on both facets, and Ocllo (Felucca's name
     for the pre-UOML Haven town) has pinned Trammel Haven's rects, the ones Trammel's New Haven is registered over
     (P678). Buccaneer's Den keeps its guards off; every guarded Felucca region is pinned Felucca's or one of the
     author's towns.
  5. No champion spawn's area (P685's 17 altars, each 48 x 48 round its altar, notes/cc-P685-tools/out/champs.csv)
     touches a Felucca guard zone.
"""
import csv
import json
import os
import sys
import unittest

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TOOLS = os.path.join(DOCS, 'notes', 'cc-P676-tools')
sys.path.insert(0, TOOLS)
SHARD = os.environ.get('SL_SHARD_REPO', r'D:\ShatteredLegacy')
SOS = os.environ.get('SL_SOS_MAP', '')
REGIONS = os.environ.get('SL_REGIONS') or os.path.join(SHARD, 'server', 'data', 'regions-trammel.json')  # a red run: pinned's
DECISIONS = os.path.join(TOOLS, 'out-decisions.csv')
READY = bool(SOS) and os.path.exists(os.path.join(SOS, 'staidx1.mul')) and os.path.exists(REGIONS)
REGIONS_FELUCCA = os.environ.get('SL_REGIONS_FELUCCA') or os.path.join(SHARD, 'server', 'data', 'regions-felucca.json')
DECISIONS_FELUCCA = os.path.join(DOCS, 'notes', 'cc-P686-tools', 'out-decisions.csv')
READY_FELUCCA = bool(SOS) and os.path.exists(os.path.join(SOS, 'staidx1.mul')) and os.path.exists(REGIONS_FELUCCA)
PINNED = r'D:/UO/ModernUO-pinned/Distribution/Data/regions.json'
CHAMPS = os.path.join(DOCS, 'notes', 'cc-P685-tools', 'out', 'champs.csv')
REACH = 3  # blocks: gen_regions.peel_to_town's join (2) plus its margin (1)
NEW_TOWNS = ['Valunstead', 'Hammerhill', 'Kameron Kove', 'Elmhaven', 'Kettleburg', 'Fort Yondall', 'Elandrim Nur Shaz']

_land = None


def land():
    global _land
    if _land is None:
        import gen_regions
        _land = gen_regions.Land(SOS)
    return _land


def rects(r):
    return [(a['x1'], a['y1'], a['x2'], a['y2']) for a in r['Area']]


def touch(a, b):
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def has_built(L, q):
    import gen_regions
    x1, y1, x2, y2 = q
    for bx in range(max(0, x1) // 8, (min(gen_regions.W, x2) - 1) // 8 + 1):
        for by in range(max(0, y1) // 8, (min(gen_regions.H, y2) - 1) // 8 + 1):
            if gen_regions.is_built(L, (bx, by)):
                return True
    return False


@unittest.skipUnless(READY, 'needs SL_SOS_MAP (the SoS map with our patch) and the code copy\'s regions-trammel.json')
class Regions(unittest.TestCase):
    FILE, LOG = REGIONS, DECISIONS

    @classmethod
    def setUpClass(cls):
        cls.regions = json.load(open(cls.FILE, encoding='utf-8'))
        cls.decided = {r['region']: r['decision'] for r in csv.DictReader(open(cls.LOG))}

    def test_1_every_rect_on_dry_land_or_its_own_water(self):
        L = land()
        bad = []
        for r in self.regions:
            name, dungeon = r.get('Name') or '(unnamed)', r.get('$type') == 'DungeonRegion'
            rs = rects(r)
            dry = [L.share([q], 0) > 0 for q in rs]
            for i, q in enumerate(rs):
                water, void = L.share([q], 1), L.share([q], 2)
                if dungeon:
                    if water > 0.5 or not dry[i]:
                        bad.append((name, q, 'a dungeon rect with water %.2f, dry %s' % (water, dry[i])))
                    continue
                if void > 0.5:
                    bad.append((name, q, 'void %.2f' % void))
                elif not dry[i] and not has_built(L, q) and not any(dry[j] and touch(q, rs[j]) for j in range(len(rs)) if j != i):
                    bad.append((name, q, 'open sea, away from the region\'s land'))
        self.assertEqual([], bad)

    def test_2_no_guard_zone_drawn_here_covers_open_wild(self):
        import gen_regions
        L = land()
        bad, pinned = [], []
        for r in self.regions:
            if r.get('$type') not in gen_regions.GUARDED or r.get('Parent'):
                continue
            name = r.get('Name')
            blocks = {(bx, by) for (x1, y1, x2, y2) in rects(r)
                      for bx in range(x1 // 8, (x2 - 1) // 8 + 1) for by in range(y1 // 8, (y2 - 1) // 8 + 1)}
            # pinned's own rects (cc-P686: Ocllo takes pinned Trammel Haven's, as S7 keeps Haven's on Trammel)
            if self.decided.get(name) in ('kept', 'kept for S7', 'clipped', 'redrawn to the town'):
                wild = sum(1 for b in blocks if gen_regions.is_wild(L, b))
                pinned.append('%s %d of %d' % (name, wild, len(blocks)))
                continue
            built = {b for b in blocks if gen_regions.is_built(L, b)}
            # enclosed: not reachable from outside the zone through unbuilt blocks
            open_ = blocks - built
            edge = [b for b in open_ if any((b[0] + dx, b[1] + dy) not in blocks for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
            outside, q = set(edge), list(edge)
            while q:
                bx, by = q.pop()
                for n in ((bx + 1, by), (bx - 1, by), (bx, by + 1), (bx, by - 1)):
                    if n in open_ and n not in outside:
                        outside.add(n)
                        q.append(n)
            town = blocks - outside
            reach = REACH  # peel_to_town joins built blocks up to 2 apart, then adds a margin of 1
            far = [b for b in blocks - town if gen_regions.is_wild(L, b)
                   and not any((b[0] + dx, b[1] + dy) in built for dx in range(-reach, reach + 1) for dy in range(-reach, reach + 1))]
            if far:
                bad.append((name, len(far), sorted(far)[:5]))
        print('\n  pinned guard zones kept as pinned (open-wild blocks): ' + '; '.join(pinned))
        self.assertEqual([], bad)

    def test_3_the_new_towns_and_wild_areas_are_on_dry_land(self):
        L = land()
        by_name = {r.get('Name'): r for r in self.regions}
        for name in NEW_TOWNS + ['Glimmerwood', 'Nujelm Desert']:
            self.assertIn(name, by_name)
            share = L.share(rects(by_name[name]), 0)
            self.assertGreater(share, 0.5, '%s: dry %.2f' % (name, share))


@unittest.skipUnless(READY_FELUCCA, 'needs SL_SOS_MAP and the code copy\'s regions-felucca.json')
class FeluccaRegions(Regions):
    """cc-P686: facts 1-3 on Felucca's file."""
    FILE, LOG = REGIONS_FELUCCA, DECISIONS_FELUCCA


def guarded(regions):
    """[(name, rects)] of every region with guards on: a TownRegion or GuardedRegion, or a child under one (a child
    forwards guard hooks to its parent), unless GuardsDisabled."""
    by = {r.get('Name'): r for r in regions if r.get('Name')}
    out = []
    for r in regions:
        g = r
        while g.get('$type') not in ('TownRegion', 'GuardedRegion') and isinstance(g.get('Parent'), dict) \
                and g['Parent']['Name'] in by:
            g = by[g['Parent']['Name']]
        if g.get('$type') in ('TownRegion', 'GuardedRegion') and not g.get('GuardsDisabled'):
            out.append((r.get('Name') or '(unnamed under %s)' % r['Parent']['Name'], rects(r)))
    return out


@unittest.skipUnless(os.path.exists(REGIONS_FELUCCA) and os.path.exists(REGIONS), 'needs both region files')
class FeluccaMatches(unittest.TestCase):
    """cc-P686: facts 4 and 5 (no map needed)."""

    @classmethod
    def setUpClass(cls):
        cls.fel = json.load(open(REGIONS_FELUCCA, encoding='utf-8'))
        cls.tram = json.load(open(REGIONS, encoding='utf-8'))
        cls.pinned = json.load(open(PINNED, encoding='utf-8'))

    def test_4_the_towns_match_and_felucca_keeps_its_rules(self):
        tram = {r['Name']: r for r in self.tram if r.get('Name')}
        fel = {r['Name']: r for r in self.fel if r.get('Name')}
        self.assertTrue(all(r['Map'] == 'Felucca' for r in self.fel))
        differ = sorted(n for n in fel if n in tram and rects(fel[n]) != rects(tram[n]))
        self.assertEqual([], differ, 'regions named on both facets with different rects')
        for town in NEW_TOWNS + ['Britain', 'Vesper', 'Yew', 'Moonglow', 'Magincia', "Buccaneer's Den", 'Minoc']:
            self.assertIn(town, fel)
        haven = next(r for r in self.pinned if r['Map'] == 'Trammel' and r.get('Name') == 'Haven')
        self.assertEqual(rects(haven), rects(fel['Ocllo']), 'Ocllo is the pre-UOML Haven town')
        self.assertTrue(fel["Buccaneer's Den"].get('GuardsDisabled'), "Buccaneer's Den stays unguarded")
        pinned_guarded = {r.get('Name') for r in self.pinned
                          if r['Map'] == 'Felucca' and r.get('$type') in ('TownRegion', 'GuardedRegion')}
        extra = sorted(r.get('Name') or '(unnamed)' for r in self.fel if r.get('$type') in ('TownRegion', 'GuardedRegion')
                       and r.get('Name') not in pinned_guarded and r.get('Name') not in NEW_TOWNS + ['Lord British Castle'])
        self.assertEqual([], extra, 'guarded on Felucca but neither pinned Felucca\'s nor the author\'s town')

    def test_5_no_champion_area_in_a_guard_zone(self):
        zones = guarded(self.fel)
        bad = []
        for row in csv.DictReader(open(CHAMPS)):
            x, y = int(row['x']), int(row['y'])
            area = (x - 24, y - 24, x + 24, y + 24)  # ChampionSpawn's initial SpawnArea, 48 x 48 round the altar
            for name, rs in zones:
                for q in rs:
                    if q[0] < area[2] and area[0] < q[2] and q[1] < area[3] and area[1] < q[3]:
                        bad.append((row['id'], name, q))
        self.assertEqual([], bad)


if __name__ == '__main__':
    unittest.main(verbosity=2)
