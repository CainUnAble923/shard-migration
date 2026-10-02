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

    # ---- D24 fix 3: an enum member is owned by the file declaring its enum ---------------------
    def test_enum_member_resolves_to_the_file_declaring_its_enum(self):
        # S9 printed `unknown: Good` for the Epiphany set. `Alignment.Good`: that enum is declared
        # in DespiseCreature.cs. On the S9-era tree, because ours has since ported Alignment itself.
        if not self.s9_tree:
            self.skipTest('cannot export the S9-era customizations tree')
        rel = 'Items/Artifacts/Equipment/Armor/Sets/Epiphany/EpiphanyHelper.cs'
        fixed, legacy = ci.Index(self.s9_tree), ci.Index(self.s9_tree, legacy=True)
        got = fixed.row('artifacts')['files'][rel]
        self.assertEqual(got['bucket'], 'elsewhere')
        self.assertEqual(got['names']['elsewhere'], ['Good'])
        self.assertEqual(fixed.resolve_name('Good', set(), fixed.sv[rel]), ('elsewhere', 'Mobiles/Normal/DespiseCreature.cs'))
        self.assertIn('Good', legacy.missing(legacy.sv[rel]))
        self.assertEqual(legacy.resolve_name('Good', set(), legacy.sv[rel])[0], 'unknown')

    def test_member_missing_from_an_enum_pinned_ships_is_upstream(self):
        # Pinned's TalismanSlayerName stops at Bovine: a patch to that enum, not an unknown name.
        rel = 'Items/Equipment/Talismans/TalismanofGoblinSlaying.cs'
        self.assertIn('Goblin', self.fixed.missing(self.fixed.sv[rel]))
        self.assertEqual(self.fixed.resolve_name('Goblin', set(), self.fixed.sv[rel]), ('upstream', None))
        self.assertEqual(self.legacy.resolve_name('Goblin', set(), self.legacy.sv[rel])[0], 'unknown')

    def test_qualifier_breaks_the_enum_member_type_tie(self):
        # `HuntType.Lion` is the enum member in HuntingTrophyInfo.cs, not the Lion mobile.
        f = self.fixed.sv['Services/HuntmasterChallenge/HuntingSystem.cs']
        self.assertIn('Lion', self.fixed.missing(f))
        self.assertEqual(self.fixed.resolve_name('Lion', set(), f),
                         ('elsewhere', 'Services/HuntmasterChallenge/HuntingTrophyInfo.cs'))
        self.assertEqual(self.legacy.resolve_name('Lion', set(), self.legacy.sv[f.rel]),
                         ('elsewhere', 'Mobiles/Normal/Lion.cs'))
        # A file's own enum member is its own only when every use is qualified by that enum.
        # Trophies.cs writes only `TrophyStyle.Crab`; AmmoInfo.cs also writes `typeof(Cannonball)`.
        trophies = self.fixed.sv['Services/Expansions/High Seas/Items/Fish/Trophies.cs']
        self.assertNotIn('Crab', self.fixed.missing(trophies))
        self.assertIn('Crab', self.legacy.missing(self.legacy.sv[trophies.rel]))
        ammo = self.fixed.sv['Services/Expansions/High Seas/Items/Cannons and Ammo/AmmoInfo.cs']
        self.assertIn('Cannonball', ammo.enums['AmmunitionType'])
        self.assertIn('Cannonball', self.fixed.missing(ammo))

    # ---- D24 fix 4: [SerializableField] names are the generated property's -----------------------
    def test_generated_name_matches_the_generator(self):
        # Each pair was produced by ModernUO.Serialization.Generator 2.14.3's own GetPropertyName.
        for field, prop in [('_recipeID', 'RecipeID'), ('_bardingHP', 'BardingHP'), ('_loginIPs', 'LoginIPs'),
                            ('_line1', 'Line1'), ('_hue', 'Hue'), ('m_Hue', 'Hue'), ('_max_hits', 'MaxHits'),
                            ('_a2b', 'A2b')]:
            self.assertEqual(ci.generated_name(field), prop, field)
        # The one pinned field written with no space before its name.
        self.assertIn('DamageEntries', self.fixed.muo['UOContent/Engines/CannedEvil/ChampionSpawn.cs'].generated)

    def test_generated_property_resolves_only_when_fixed(self):
        rel = 'Items/Books/SpecialScrollBooks/RecipeBook/RecipeBookGump.cs'
        self.assertNotIn('RecipeID', self.fixed.missing(self.fixed.sv[rel]))
        self.assertIn('RecipeID', self.legacy.missing(self.legacy.sv[rel]))
        self.assertEqual(self.fixed.tree.generated_only['RecipeID'], 'UOContent/Items/Skill Items/Misc/RecipeScroll.cs')

    # ---- D24: the same-graphic check says when it did not run ----------------------------------
    def test_graphic_check_distinguishes_not_run_from_none_found(self):
        rows = {r['type']: r for r in self.fixed.hidden(ci.ROWS['artifacts'])}
        self.assertEqual(rows['MaleGargishClothKilt']['graphic_check'], 'twin')
        self.assertEqual(rows['GuildedKilt']['graphic_check'], 'none found')
        self.assertEqual(rows['ZooMemberCloak']['graphic_check'], 'not run')         # base(hue), inherited
        self.assertEqual(rows['GargishKiltOfMining']['graphic_check'], 'not run')    # base(bonus, 0x030C)

    # ---- P2: a #region label is not a name ------------------------------------------------------
    def test_preprocessor_lines_are_not_names_when_fixed(self):
        rel = 'Items/Addons/GargishCotEastAddon.cs'                     # `#region Mondain's Legacy`
        self.assertIn('Mondain', self.legacy.missing(self.legacy.sv[rel]))
        self.assertNotIn('Mondain', self.fixed.missing(self.fixed.sv[rel]))
        # The resolving side too: pinned spells `Stygian` only in a #region. (`Helpers` is the same in
        # BasePeerless.cs, but Medusa's `_helpers` generates it, so it still resolves: by name, as ever.)
        self.assertIn('Stygian', self.legacy.tree.idents)
        self.assertNotIn('Stygian', self.fixed.tree.idents)

    # ---- P2: decimal graphics are read, clilocs are not ------------------------------------------
    def test_graphic_check_reads_decimal_literals_in_art_range(self):
        rows = {r['type']: r for r in self.fixed.hidden(ci.ROWS['artifacts'])}
        self.assertEqual(rows['HangingPlatemailArms']['graphic'], hex(40681))       # base(40681)
        self.assertEqual(rows['HangingPlatemailArms']['graphic_check'], 'none found')
        self.assertEqual(rows['CompleteNecromancerSpellbook']['graphic_check'], 'not run')  # base((ulong)0x1FFFF)
        f = ci.FileInfo('x.cs', 'class A : Item { public A() : base(1094954) {} } '
                                'class B : Item { public B(int n) : base(1) {} } '
                                'class C : Item { public C() : base(4014) {} }')
        self.assertEqual(f.graphics, {'C': 4014})                                  # cliloc and amount skipped

    # ---- D33 reach: what puts a type in the world, not what names it ----------------------------
    # Facts about the tree as it stands. Like the spawn-orphan facts in the shard tests, they are meant to
    # move when a gate is built; change the expectation then, with a line saying which gate did it.
    @classmethod
    def reach(cls):
        if not hasattr(cls, '_reach'):
            cls._reach = ci.Reach()
        return cls._reach

    def test_reach_spawn_entries_resolve_case_insensitively(self):
        # Underworld.json:258 writes `tanglingroots`; BaseSpawner resolves it like FindTypeByName (Q-048).
        e = self.reach().reached['TanglingRoots']
        self.assertEqual((e[1], e[4], e[5]), ('spawn', 'data/Spawns/post-uoml/termur/Underworld.json', 258))

    def test_reach_a_string_table_read_by_static_access_creates_its_entries(self):
        # DespiseSpawns holds entry names as strings and is only ever read as `DespiseSpawns.Definitions`.
        e = self.reach().reached['Silenii']
        self.assertEqual((e[1], e[3]), ('string', 'DespiseSpawns'))

    def test_reach_static_access_runs_no_instance_code(self):
        # TanglingRoots reads `FountainOfFortune.UnderProtection`. That makes the fountain's code live but makes no
        # fountain, so the satchel its reward code constructs is not made either. From TanglingRoots alone, since
        # gate 14 is built: cc-P27's ClusterFFountainOfFortuneSeeder places a fountain (D14), and the whole tree now
        # reaches both by `new`.
        r = self.reach()
        created, live = r._closure(r.out, {'TanglingRoots'})
        self.assertEqual(live['FountainOfFortune'][1], 'static')
        self.assertNotIn('FountainOfFortune', created)
        self.assertNotIn('GemologistsSatchel', created)
        self.assertEqual(r.reached['FountainOfFortune'][1:4:2], ('new', 'ClusterFFountainOfFortuneSeeder'))

    def test_reach_a_list_that_reads_types_does_not_create_them(self):
        # GemologistsSatchel.IngredTypes says what the satchel accepts, not where reagents come from.
        r = self.reach()
        self.assertNotIn('DaemonClaw', r.reached)
        self.assertEqual({(x[1], x[2]) for x in r.by_target['DaemonClaw']}, {('check', 'IngredTypes')})

    def test_reach_a_base_is_reached_through_children_unless_it_is_an_item_itself(self):
        r = self.reach()
        self.assertEqual(r.reached['ShameGuardian'][1], 'base')                  # no [Constructible]
        created = r.what_if({'AloronsBustier'})
        self.assertIn('AloronsBustier', created)
        self.assertNotIn('TigerPeltBustier', created)                            # an item in its own right

    def test_reach_a_data_file_that_only_lists_names_places_nothing(self):
        # bodyTable.cfg names Allosaurus; no spawn file does (notes/cc3-eodon.md).
        r = self.reach()
        self.assertNotIn('Allosaurus', r.reached)
        self.assertIn('data-mention', {x[1] for x in r.by_target['Allosaurus']})

    def test_reach_pinned_code_left_commented_out_is_reported(self):
        # Ilhenir.cs:163, under `// TODO: uncomment once added`, which no patch of ours uncomments (cc-P7 2.3).
        # Until cc-P27 this fact used GreymistChest at LadyLissith.cs:53, which cc-P7's patch uncommented.
        hits = [x for x in self.reach().by_target['GrizzleGauntlets'] if x[1] == 'pinned-comment:new']
        self.assertEqual([(x[4], x[5]) for x in hits],
                         [('pinned/UOContent/Mobiles/Monsters/ML/Special/Ilhenir.cs', 163)])

    def test_reach_an_uncomment_patch_makes_pinned_code_live(self):
        # cc-P7's patches only take the comment markers off pinned's own drops, so `new MyrmidonGloves()` is a
        # context line of the patch, not an added one. Pinned is read as the build compiles it (cc-P27), so the
        # drop reaches; read as pinned plus added lines it stayed a comment and gate 9 read 0 delivered (cc-P7 2.7).
        r = self.reach()
        for name, where in (('MyrmidonGloves', ('pinned/UOContent/Mobiles/Monsters/ML/Labyrinth/Miasma.cs', 54)),
                            ('GreymistChest', ('pinned/UOContent/Mobiles/Monsters/ML/Twisted Weald/LadyLissith.cs', 53))):
            e = r.reached.get(name)
            self.assertIsNotNone(e, name)
            self.assertEqual((e[1], e[3], e[4], e[5]), ('new', 'root:pinned') + where)

    def test_reach_a_later_typeof_in_addcraft_is_a_resource_not_a_product(self):
        # AddCraft(typeof(Product), group, name, min, max, typeof(FirstResource), ...): only the first typeof is
        # made (craft-registrations 4.1.1). ServUO DefTinkering.cs:614 crafts ArcanicRuneStone from CrystalShards,
        # which --sources used to report as a tinkering source of CrystalShards.
        code = 'AddCraft(typeof(Product), 1044050, 1113172, 70.0, 120.0, typeof(Resource), 1044036, 1, 1044037);'
        self.assertEqual(ci.ref_kind(code, code.index('Product'), code.index('Product') + 7), ('typeof', 'AddCraft'))
        self.assertEqual(ci.ref_kind(code, code.index('Resource'), code.index('Resource') + 8), ('check', 'AddCraft'))
        src = ci.servuo_sources(self.reach(), ['CrystalShards'])['CrystalShards']
        self.assertNotIn('Scripts/Services/Craft/DefTinkering.cs', {x[4] for x in src})
        self.assertTrue(src)                                                     # its real sources remain

    def test_reach_servuo_turn_in_table_is_not_a_source(self):
        # CleanUpBritanniaData.Entries is what a player hands in; CleanUpBritanniaRewards hands out.
        src = ci.servuo_sources(self.reach(), ['BestialArms', 'AntiqueWeddingDress'])
        self.assertEqual({x[4] for x in src['BestialArms']}, {'Scripts/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs'})
        # Turned in for points (CleanUpBritanniaData.cs), never handed out by Clean Up.
        self.assertNotIn('Scripts/Services/PointsSystems/CleanUpBritanniaData.cs', {x[4] for x in src['AntiqueWeddingDress']})
        self.assertTrue(src['AntiqueWeddingDress'])

    def test_twin_sweep_finds_a_pinned_type_under_a_misspelling(self):
        # Pinned ships the champion artifact as `GuantletsOfAnger`, same cliloc 1094902.
        hits = {(n, test, m) for n, f, test, m, where in ci.twins(self.reach(), ci.C)}
        self.assertIn(('GauntletsOfAnger', 'cliloc', 'GuantletsOfAnger'), hits)


if __name__ == '__main__':
    unittest.main()
