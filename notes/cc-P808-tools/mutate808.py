# cc-P808: one deliberate break per behaviour, as changed sources under mutants/<name>/. run-mutants-inner.sh builds each and
# runs the Scavenger facts. Each must turn a fact red; see mutants.txt.
import os, shutil
S = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/'
OUT = 'D:/UO/golems/Iron/shard-migration/notes/cc-P808-tools/mutants/'
P = ('Mobiles/ClockworkScavenger/ClockworkScavenger.cs', 'Mobiles/ClockworkScavenger/ClockworkScavenger.cs')
Q = ('Mobiles/ClockworkScavenger/ClockworkScavengerQuest.cs', 'Mobiles/ClockworkScavenger/ClockworkScavengerQuest.cs')
C = ('Mobiles/ClockworkScavenger/ClockworkScavengerConfig.cs', 'Mobiles/ClockworkScavenger/ClockworkScavengerConfig.cs')
D = ('Mobiles/Mule/MuleModuleData.cs', 'Mobiles/Mule/MuleModuleData.cs')
M = {
 'quest-no-membership': (Q, 'if (!ClusterFGuildSystem.IsJoined(pm, GuildKey))', 'if (false)'),
 'quest-no-rank': (Q, 'else if (RankOf(pm) < minRank)', 'else if (false)'),
 'quest-second-frame': (Q, 'else if (FrameOf(pm) != null)', 'else if (false)'),
 'quest-second-scavenger': (Q, 'else if (ScavengerOf(pm) != null)', 'else if (false)'),
 'assemble-keeps-parts': (Q, 'if (pack.ConsumeTotal(types, amounts) != -1)', 'if (false)'),
 'assemble-unbound': (Q, 'if (frame.Deleted || frame.Owner != pm)', 'if (frame.Deleted)'),
 'assemble-keeps-frame': (Q, 'frame.Delete();\n            pm.PlaySound(0x241);', 'pm.PlaySound(0x241);'),
 'entry-for-everyone': (Q, 'ClusterFGuildSystem.IsJoined(from, GuildKey)', 'true'),
 'frame-liftable': (P, '(_owner == null || from == _owner || from.AccessLevel > AccessLevel.Player) && base.OnDragLift(from);', 'base.OnDragLift(from);'),
 'not-blessed': (P, 'Blessed = true;', ''),
 'no-default-filter': (P, '_filterList = new List<string>(c.DefaultFilter ?? []);', '_filterList = new List<string>();'),
 'loot-crime': (P, '!corpse.IsCriminalAction(owner) && corpse.CanLoot(owner, null) &&', ''),
 'loot-player-corpse': (P, 'corpse.Owner is not PlayerMobile && (corpse.Owner is BaseCreature || corpse.OwnerWasBaseCreature) &&', ''),
 'loot-ignores-filter': (P, ' ||\n                        !corpse.IsChildVisibleTo(owner, item) || !MuleModules.Matches(item, Filter))', ' ||\n                        !corpse.IsChildVisibleTo(owner, item))'),
 'loot-empty-filter': (P, 'owner.Backpack == null || Filter.Count == 0)', 'owner.Backpack == null)'),
 'loot-offline': (P, 'owner.NetState == null ||', ''),
 'loot-far': (P, '!InRange(owner, c.OwnerRange) ||', ''),
 'loot-no-cap': (P, 'if (moved >= c.MaxPerTick)', 'if (false)'),
 'harness-never': (P, 'ClockworkLoadHarness) >= 3 ? m : null', 'ClockworkLoadHarness) >= 99 ? m : null'),
 'harness-tier-two': (P, 'ClockworkLoadHarness) >= 3 ? m : null', 'ClockworkLoadHarness) >= 2 ? m : null'),
 'harness-still-partial': (D, 'MuleModuleState.Built), // cc-P808', 'MuleModuleState.Partial), // cc-P808'),
 'release-keeps-it': (P, 'public override bool DeleteOnRelease => true;', 'public override bool DeleteOnRelease => false;'),
 'filter-unsaved': (P, '[SerializableField(1, setter: "private")]\n        private List<string> _filterList;', 'private List<string> _filterList;'),
 'builder-unsaved': (P, '[SerializableField(0, setter: "private")]\n        [SerializedCommandProperty(AccessLevel.GameMaster, readOnly: true)]\n        private Mobile _builder;\n\n        [SerializableField(1, setter: "private")]\n        private List<string> _filterList;',
     'private Mobile _builder;\n        public Mobile Builder => _builder;\n\n        [SerializableField(0, setter: "private")]\n        private List<string> _filterList;'),
 'config-accepts-bad': (C, 'if (errors.Count > 0)', 'if (false)'),
 'config-not-written': (C, 'File.WriteAllText(path, ToJson(new ClockworkScavengerConfig()));', ''),
 'config-any-part': (C, 'errors.Add($"part \\"{p?.Type}\\" is not an item type");', ''),
 'gump-no-toggle': (P, '_s.ToggleFilter(MuleModules.PickupCategories[i]);', ''),
}
shutil.rmtree(OUT, ignore_errors=True)
for name, ((src, target), old, new) in M.items():
    text = open(S + src, encoding='utf-8', newline='').read()
    n = text.count(old)
    assert n == 1, f'{name}: found {n}'
    d = OUT + name + '/'
    os.makedirs(os.path.dirname(d + target), exist_ok=True)
    open(d + target, 'w', encoding='utf-8', newline='').write(text.replace(old, new))
    open(d + 'target', 'w').write(target)
print(len(M), 'mutants')
