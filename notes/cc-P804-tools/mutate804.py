# cc-P804: one deliberate break per behaviour, as changed sources under mutants/<name>/. run-mutants-inner.sh builds each in one
# container and runs the Herbalism facts. Each must turn a fact red; see mutants.txt.
import os, shutil
S = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/'
OUT = 'D:/UO/golems/Iron/shard-migration/notes/cc-P804-tools/mutants/'
L = ('Herbalism/HerbalLane.cs', 'Herbalism')
I = ('Herbalism/HerbalItems.cs', 'Herbalism')
H = ('Herbalism/HerbalismSettings.cs', 'Herbalism')
G = ('ClusterFGuildSystem.cs', 'Misc')
T = ('ClusterFGuildStarterPath.cs', 'Misc')
M = {
 'perennial-off': (L, 'var day = DailyYield(plant);\r\n        system.AvailableResources = Math.Min(system.AvailableResources + day, day * S.MaxStoredDays);\r\n        return true;', 'return false;'),
 'no-store-cap': (L, 'Math.Min(system.AvailableResources + day, day * S.MaxStoredDays)', 'system.AvailableResources + day'),
 'tier-no-yield': (L, 'herbs += record.Tier * S.HerbsPerStrainTier;', ''),
 'skill-no-yield': (L, 'herbs *= 1 + S.YieldBonusPercentAt200 / 100.0 * record.TenderSkill / 200.0;', ''),
 'malady-no-yield': (L, 'herbs *= Math.Max(0, 1 - MaladyCount(system) * S.MaladyYieldLossPercent / 100.0);', ''),
 'bed-yields-as-bowl': (L, 'double herbs = plant is RaisedGardenPlantItem ? S.BedHerbsPerDay : S.BowlHerbsPerDay;', 'double herbs = S.BowlHerbsPerDay;'),
 'bed-not-one-unit': (L, 'if (part is GardenAddonComponent { Plant: { } other } && other != plant && IsReagent(other))', 'if (false && part is GardenAddonComponent { Plant: { } other } && other != plant && IsReagent(other))'),
 'stock-pollen-ok': (L, 'public static bool RefusesPollen(PlantItem source, PlantItem target) => IsReagent(source.PlantType) != IsReagent(target.PlantType);', 'public static bool RefusesPollen(PlantItem source, PlantItem target) => false;'),
 'no-mutation': (L, 'tier++;\r\n            mutated = true;', 'mutated = true;'),
 'mutates-across-tiers': (L, 'if (source != target && a == b && tier + 1', 'if (source != target && tier + 1'),
 'no-skill-cap': (L, 'a == b && tier + 1 <= StrainCap(Skill(from)) &&', 'a == b &&'),
 'cross-takes-lower': (L, 'var tier = Math.Max(a, b);', 'var tier = Math.Min(a, b);'),
 'seed-loses-tier': (L, 'return new ReagentSeed(system.SeedType, record.SeedTier >= 0 ? record.SeedTier : record.Tier);', 'return new ReagentSeed(system.SeedType, 0);'),
 'grace-flat': (L, 'S.GraceBaseDays + S.GraceExtraDaysAt200 * skill / 200.0', 'S.GraceBaseDays'),
 'osi-damage-kills': (L, 'public static bool SparesDamage(PlantSystem system) => IsReagent(system.Plant);', 'public static bool SparesDamage(PlantSystem system) => false;'),
 'tier-drops-first': (L, 'var windows = grace > 0 ? (int)(past / grace) : 0;', 'var windows = grace > 0 ? (int)(past / grace) + 1 : 0;'),
 'neglect-no-health': (L, 'system.Hits = Math.Max(1, system.Hits - S.NeglectHitsPerCheck);', ''),
 'neglect-kills': (L, 'system.Hits = Math.Max(1, system.Hits - S.NeglectHitsPerCheck);', 'system.Hits -= 1000;'),
 'tending-keeps-drops': (L, 'record.TierDrops = 0;', ''),
 'gate-off': (L, 'if (AlembicRank(from) >= need)', 'if (true)'),
 'rank-ignores-strain': (L, 'Math.Max(HerbOf(type)?.AlembicRank ?? 0, tier / S.StrainTiersPerAlembicRank)', 'HerbOf(type)?.AlembicRank ?? 0'),
 'no-green-thumb': (L, 'ClusterFAchievementSystem.TryGrant(acct, FirstHarvestAchievement);', ''),
 'no-ledger': (L, 'LogFind(from, herb.Key, total);', ''),
 'no-bundle-bonus': (L, '(int)(S.ReagentsPerBundle * (1 + S.BundleBonusPercentAt200 / 100.0 * skill / 200.0))', 'S.ReagentsPerBundle'),
 'store-version-open': (L, 'if (version is < 0 or > CurrentVersion)', 'if (false)'),
 'store-no-prune': (L, 'if (World.FindItem(pair.Key) is PlantItem { Deleted: false })', 'if (true)'),
 'gain-window-flat': (L, 'var low = Math.Min(((herb?.Tier ?? 1) - 1) * 50.0 + strain * S.GainPerStrainTier, 200.0 - S.GainWindow);', 'var low = 0.0;'),
 'patch-never-hides': (I, 'Visible = false;\r\n            RipeAt = Core.Now + TimeSpan.FromMinutes(s.RespawnMinutes);', 'RipeAt = Core.Now + TimeSpan.FromMinutes(s.RespawnMinutes);'),
 'patch-never-respawns': (I, 'patch.Visible = true;\r\n                count++;', 'count++;'),
 'patch-no-tier': (I, 'if (HerbalLane.Skill(from) < floor)', 'if (false)'),
 'pick-no-ledger': (I, 'HerbalLane.LogFind(from, herb.Key, amount);', ''),
 'process-no-tier': (I, 'if (HerbalLane.Skill(from) < HerbalLane.SkillFloor(herb))', 'if (false)'),
 'process-keeps-herbs': (I, 'Consume(bundles * s.HerbsPerBundle);', ''),
 'bundle-keeps-open': (I, 'from.SendMessage(0x44, $"You open the bundle: {reagent.Amount} reagents.");\r\n        Delete();', 'from.SendMessage(0x44, $"You open the bundle: {reagent.Amount} reagents.");'),
 'seed-twice': (I, 'if (have.Contains(spot.Key))', 'if (false)'),
 'starter-twice': (I, 'if (HadStarter(from) || from.Account is not IAccount acct)', 'if (from.Account is not IAccount acct)'),
 'seed-tier-unsaved': (I, '[InvalidateProperties]\r\n    [SerializableField(0)]\r\n    [SerializedCommandProperty(AccessLevel.GameMaster)]\r\n    private int _strainTier;', 'public int StrainTier { get => _strainTier; set => _strainTier = value; }\r\n    private int _strainTier;'),
 'stock-treated-as-lane': (L, 'public static bool SparesDamage(PlantSystem system) => IsReagent(system.Plant);\r\n\r\n', 'public static bool SparesDamage(PlantSystem system) => IsReagent(system.Plant);\r\n\r\n') if False else (L, 'var bed = BedOf(plant);\r\n        var total = 0;', 'var bed = BedOf(plant);\r\n        var total = 0;'),
 'exotic-grows-wild': (H, 'new() { Key = "Exotic", Name = "exotic herb", Tier = 4, Reagent = "", Stub = true },', 'new() { Key = "Exotic", Name = "exotic herb", Tier = 4, Reagent = "Garlic" },'),
 'stock-hooks-mature': (L, 'if (!IsReagent(plant))\r\n        {\r\n            return false;\r\n        }\r\n\r\n        var day = DailyYield(plant);', 'var day = DailyYield(plant);'),
 'mound-always-tended': (('Services/Plants/Raised Garden Beds/RaisedGardenPlantItem.cs', 'Mound'), 'public override bool RequiresUpkeep => HerbalLane.IsReagent(this);', 'public override bool RequiresUpkeep => true;'),
 'bed-full-maladies': (L, 'IsReagent(system.Plant) && system.Plant is RaisedGardenPlantItem && (roll ?? Utility.RandomDouble()) * 100 >= S.BedMaladyPercent;', 'false;'),
 'hue-not-strain': (L, 'IsReagent(plant.PlantType) && plant.PlantStatus < PlantStatus.DeadTwigs ? StrainHue(Record(plant).Tier) : stockHue;', 'stockHue;'),
 'few-herbs-bundle': (I, 'if (bundles <= 0)', 'if (false)'),
 'starter-farm-rich': (H, 'public int BowlHerbsPerDay { get; set; } = 6;', 'public int BowlHerbsPerDay { get; set; } = 30;'),
 'settings-accept-bad': (H, 'Range(s.MaxStoredDays, 1, 365, nameof(MaxStoredDays), errors);', ''),
 'settings-stub-spot': (H, 'if (s.Herb(spot.Herb) is null or { Stub: true })', 'if (s.Herb(spot.Herb) is null)'),
 'alembic-alchemy-only': (G, 'def.Key == ClusterFAlembicGuild.Key\r\n            ? System.Math.Max', 'false\r\n            ? System.Math.Max'),
 'homeless-skill': (T, ', SkillName.Herbalism]', ']'),
}
M.pop('stock-treated-as-lane')
ONLY = ('few-herbs-bundle',)
M = {k: v for k, v in M.items() if k in ONLY}
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
for name, ((rel, dest), a, b) in M.items():
    s = open(S + rel, encoding='utf-8', newline='').read()
    if '\r\n' not in s:
        a = a.replace('\r\n', '\n'); b = b.replace('\r\n', '\n')
    assert s.count(a) == 1, (name, s.count(a))
    d = OUT + name + '/' + dest
    os.makedirs(d)
    open(d + '/' + os.path.basename(rel), 'w', encoding='utf-8', newline='').write(s.replace(a, b))
    open(OUT + name + '/target', 'w').write(dest + '/' + os.path.basename(rel))
print(len(M), 'mutants')
