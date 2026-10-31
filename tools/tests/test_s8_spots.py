"""cc-P677 (SoS swap S8): every coordinate literal in S8's files stands on the land the server reads.

    SL_SHARD_REPO=<code copy> SL_SOS_MAP=<SoS map folder> python -P tools/tests/test_s8_spots.py

SL_SOS_MAP holds the server's map overlay (map1LegacyMUL.uop, statics1.mul, staidx1.mul: the SoS base with the code
copy's trammel.mapops; docker/uo/Build-MapOverlay.ps1 writes it). Skipped without it. The files are the 30 of ours
P669's geo-files.csv grades "moves" or "needs rework" (notes/cc-P677-tools/files-all30.txt); the literals and the
spot rule are notes/cc-P677-tools/spots.py's: a standing surface on the tile (land at Map.GetAverageZ, or a Surface
static; Bridge items at half height), nothing impassable or solid in the 16 Z above, and a literal's Z within 5 of it.

  1. Every literal passes, except these, each by a rule and never one by one:
     - on another facet (Ter Mur, Ilshenar, Malas, Tokuno): not on the SoS land;
     - a corner of an area (Rectangle2D/3D, or a Point3D pair with MinZ/MaxZ): it bounds an area, nothing stands there;
     - the spot an old world's NPC is moved FROM (wasAt, .WasAt(, the first point of a mine camp NPC move): a fresh world
       (Chase 10-27) has nobody there;
     - Blackthorn's files: their literals are ServUO's stock spots, which BlackthornFold.Move puts on the Fold (cc-P691;
       the dungeon is its map patch's copy, checked by the shard's BlackthornDungeonVerification and P691's TazUO walks);
     - the guild hall table, whose halls fact 3 checks with their own walk checks;
     - a test patch's fixture spot (ImportCleanupTests-guid-key.patch): the test host has no map.
  2. cc-P691: Blackthorn is on the Fold, not on this land: its region registers on the Fold only, and [GenBlackthorn
     refuses while the Fold's copy is missing (BlackthornFold.MapReady). (cc-P677's fact was that it was off.)
  3. The guild halls on SoS: P281's check.py, run with its client folder on the SoS land (notes/cc-P677-tools/p281sos,
     made by make_p281sos.py), passes every hall but the two P708 moves (Merchants, Custodians).
  4. The stealable artifacts whose land is gone are parked: the patch's Ararat entries and the second set of Castle
     Blackthorne's are on Map.Internal, and CheckRespawn never spawns a parked entry. cc-P691: the first set of three
     stands in the dungeon on the Fold (FoldMaps.Fold, parked if the Fold is not registered yet).
"""
import os
import re
import subprocess
import sys
import unittest

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TOOLS = os.path.join(DOCS, 'notes', 'cc-P677-tools')
sys.path.insert(0, TOOLS)
SHARD = os.environ.get('SL_SHARD_REPO', r'D:\ShatteredLegacy')
SOS = os.environ.get('SL_SOS_MAP', '')
READY = bool(SOS) and os.path.exists(os.path.join(SOS, 'staidx1.mul'))
FILES = [l.strip() for l in open(os.path.join(TOOLS, 'files-all30.txt')) if l.strip()]
BLACKTHORN = 'server/customizations/Services/Revamped Dungeons/BlackthornDungeon/'
HALLS = 'server/customizations/ClusterFGuildHallPlacementData.cs'
TEST_PATCHES = ('server/patches/ImportCleanupTests-guid-key.patch',)
P708 = {'merchants', 'custodians'}


def moved_from(text, kind_of_file):
    """The literal is where an old world's NPC is moved from."""
    if 'wasAt' in text or '.WasAt(' in text:
        return True
    return kind_of_file.endswith('ClusterFMineCampLayout.cs') and text.startswith('new("')


def exempt(row):
    rel, text, verdict = row[0], row[6], row[7]
    if verdict in ('ok', 'gone'):
        return 'ok'
    if verdict.startswith('not on SoS'):
        return 'another facet'
    if verdict == 'area corner':
        return 'area corner'
    if rel.startswith(BLACKTHORN):
        return 'Blackthorn (stock spots, moved to the Fold; P691)'
    if rel == HALLS:
        return 'guild hall (fact 3)'
    if rel in TEST_PATCHES:
        return 'test fixture'
    if moved_from(text, rel):
        # only the first point of a camp move is "from"; the second must pass on its own
        if rel.endswith('ClusterFMineCampLayout.cs'):
            first = re.search(r"new Point3D\(\s*(\d+)\s*,\s*(\d+)", text)
            if not first or (int(first.group(1)), int(first.group(2))) != (row[3], row[4]):
                return None
        return 'moved from (old world)'
    return None


def read(rel):
    return open(os.path.join(SHARD, rel), encoding='utf-8').read()


class Code(unittest.TestCase):
    def test_2_blackthorn_is_on_the_fold_not_this_land(self):
        region = read(BLACKTHORN + 'Region.cs')
        gen = read(BLACKTHORN + 'Generate.cs')
        fold = read(BLACKTHORN + 'BlackthornFold.cs')
        self.assertRegex(region, r'public static void Initialize\(\) => Register\(BlackthornFold\.Map\);')
        self.assertNotRegex(region, r'Register\(Map\.(Trammel|Felucca)\)')
        self.assertRegex(fold, r'public static Map Map => FoldMaps\.Fold;')
        self.assertRegex(gen, r'Generate_OnCommand\(CommandEventArgs e\)\s*\{\s*if \(!BlackthornFold\.MapReady\(\)\)')

    def test_4_the_lost_stealables_are_parked(self):
        text = read('server/patches/StealableArtifacts-servuo-entries.patch')
        added = [l for l in text.splitlines() if l.startswith('+') and ('new(Map.' in l or 'new(FoldMaps.' in l)]
        for name in ('SternAnchorOfBmvArarat', 'ShipsBellOfBmvArarat', 'FigureheadOfBmvArarat'):
            rows = [l for l in added if 'typeof(%s)' % name in l]
            self.assertTrue(rows, name)
            self.assertTrue(all('new(Map.Internal,' in l for l in rows), rows)
        for name in ('KingsGildedStatue', 'KingsPainting1', 'KingsPainting2'):
            rows = [l for l in added if 'typeof(%s)' % name in l]
            self.assertEqual(2, len(rows), name)
            self.assertEqual(1, sum('new(FoldMaps.Fold ?? Map.Internal,' in l for l in rows), rows)
            self.assertEqual(1, sum('new(Map.Internal,' in l for l in rows), rows)
        self.assertEqual(6, sum(1 for l in added if 'new(Map.Internal,' in l))
        self.assertIn('+            if (Entry.Map == Map.Internal)', text)


@unittest.skipUnless(READY, 'needs SL_SOS_MAP (the server map overlay on the SoS base)')
class OnSos(unittest.TestCase):
    def test_1_every_literal_stands_on_the_sos_land(self):
        import spots
        rows = spots.run(SOS, SHARD, FILES)
        bad = [(r[0].split('/')[-1], r[1], r[3], r[4], r[5], r[7]) for r in rows if exempt(r) is None]
        kinds = {}
        for r in rows:
            k = exempt(r) or 'FAIL'
            kinds[k] = kinds.get(k, 0) + 1
        print('\n  literals %d: %s' % (len(rows), ', '.join('%s %d' % kv for kv in sorted(kinds.items()))))
        self.assertEqual([], bad)

    def test_3_the_guild_halls_pass_their_own_checks_on_sos(self):
        folder = os.path.join(TOOLS, 'p281sos')
        self.assertTrue(os.path.exists(os.path.join(folder, 'check.py')), 'run notes/cc-P677-tools/make_p281sos.py')
        env = dict(os.environ)
        subprocess.run([sys.executable, '-P', 'check.py'], cwd=folder, env=env, capture_output=True, text=True)
        table = open(os.path.join(folder, 'check.out.txt'), encoding='utf-8').read()
        rows = re.findall(r'^\| (\w+) \| (ok|FAIL[^|]*?) \|', table, re.M)
        self.assertGreater(len(rows), 10, table[:300])
        failing = {k for k, v in rows if v.startswith('FAIL')}
        self.assertTrue(failing <= P708, sorted(failing - P708))


if __name__ == '__main__':
    unittest.main(verbosity=2)
