"""Regression checks for content_index.py. Read-only against all three trees.

    python -m unittest tools/test_content_index.py

The S9 reproduction exports server/customizations as it stood when S9 ran (ShatteredLegacy
b21bcd9, 198 .cs) into a temp dir with `git archive`; it is skipped if that is not possible.
"""
import io, os, subprocess, sys, tarfile, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_index as ci

SHARD = r'D:\ShatteredLegacy'
S9_REV = 'b21bcd9'
S9_NOTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 's9-backlog-remeasure.md')


def export_s9_tree():
    tmp = tempfile.mkdtemp(prefix='ours-s9-')
    try:
        data = subprocess.run(['git', '-C', SHARD, 'archive', '--format=tar', S9_REV, 'server/customizations'],
                              capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    tarfile.open(fileobj=io.BytesIO(data)).extractall(tmp, filter='data')
    return os.path.join(tmp, 'server', 'customizations')


class ContentIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty = tempfile.mkdtemp(prefix='ours-empty-')
        cls.s9_tree = export_s9_tree()
        cls.fixed = ci.Index()
        cls.legacy = ci.Index(legacy=True)

    # ---- the S9 method still reproduces --------------------------------------------------------
    def test_legacy_filter_pinned_only(self):
        # S3/S9 published 3,134 of 6,144. This index gets 3,133; the one file is comment handling,
        # recorded in notes/armour-set-completion.md C.5 and notes/index-blindspots.md.
        idx = ci.Index(self.empty, legacy=True)
        self.assertEqual(len(idx.sv), 6144)
        self.assertEqual(len(idx.discarded), 3133)

    def test_legacy_reproduces_s9_artifacts_row_file_for_file(self):
        if not self.s9_tree:
            self.skipTest('cannot export the S9-era customizations tree')
        idx = ci.Index(self.s9_tree, legacy=True)
        r = idx.row('artifacts')
        s9 = ci.parse_s9(S9_NOTE, 'Artifacts + equipment')
        self.assertEqual(len(r['raw']), 1022)
        self.assertEqual(len(r['discarded']), 567)
        for rel in r['raw']:
            got = r['files'][rel]['bucket'] if rel in r['files'] else 'discarded'
            self.assertEqual(got, s9.get(rel), rel)

    # ---- fix 1: alias strings are declarations -------------------------------------------------
    def test_alias_name_resolves_only_when_fixed(self):
        self.assertIn('GargishClothKilt', self.fixed.tree.types)
        self.assertIn('GargishClothKilt', self.fixed.tree.alias_only)
        self.assertNotIn('GargishClothKilt', self.legacy.tree.types)

    def test_kilt_is_no_longer_blocked_on_an_alias(self):
        f = self.fixed.sv['Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialKilt.cs']
        self.assertNotIn('GargishClothKilt', self.fixed.missing(f))
        self.assertIn('GargishClothKilt', self.legacy.missing(f))

    def test_alias_primary_file_is_discarded_as_aliased(self):
        rel = 'Items/Equipment/Armor/GargishLeatherKilt.cs'
        self.assertEqual(self.fixed.discard_reason.get(rel), 'aliased')
        self.assertNotIn(rel, self.legacy.discarded)

    # ---- fix 2: every secondary type of a discarded file ---------------------------------------
    def test_unreferenced_secondary_types_are_reported(self):
        rows = {(r['file'], r['type']): r for r in self.fixed.hidden(ci.ROWS['artifacts'])}
        for key in [('Items/Equipment/Clothing/OuterLegs.cs', 'GuildedKilt'),
                    ('Items/Artifacts/Equipment/Armor/GlovesOfMining.cs', 'GargishKiltOfMining')]:
            self.assertIn(key, rows)
            self.assertEqual(rows[key]['class'], 'item')

    def test_equivalent_twin_is_flagged_by_graphic(self):
        rows = {r['type']: r for r in self.fixed.hidden(ci.ROWS['artifacts'])}
        self.assertIn('GargishClothKiltType1', rows['MaleGargishClothKilt']['pinned_same_graphic'])

    # ---- the mislabel: a type in a discarded file is an extract, not an upstream member -------
    def test_type_in_discarded_file_is_extract_not_upstream(self):
        self.assertEqual(self.fixed.resolve_name('GargishClothWingArmor', set())[0], 'extract')
        self.assertEqual(self.legacy.resolve_name('GargishClothWingArmor', set())[0], 'upstream')
        self.assertEqual(self.fixed.resolve_name('TempDamageAbsorb', set())[0], 'upstream')


if __name__ == '__main__':
    unittest.main()
