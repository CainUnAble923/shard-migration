# cc-P804: edits copies of the patched engine files (base/, from the builder image) and writes server/patches/*.patch with diff -u.
# Each patch is against the tree as apply-patches.sh leaves it before this one runs, so it must apply with --fuzz=0.
import difflib, json, os, subprocess
B = 'D:/UO/golems/Iron/shard-migration/notes/cc-P804-tools/base/'
P = 'D:/UO/golems/Iron/ShatteredLegacy/server/patches/'
PL = 'Projects/UOContent/Engines/Plants/'


def read(name):
    return open(B + name, encoding='utf-8', newline='').read()


def sub(s, a, b, count=1):
    crlf = '\r\n' in s
    if crlf:
        a, b = a.replace('\n', '\r\n'), b.replace('\n', '\r\n')
    assert s.count(a) >= 1, a
    if count == 1:
        assert s.count(a) == 1, (a, s.count(a))
    return s.replace(a, b)


def patch(name, files):
    out = []
    for rel, base, new in files:
        d = difflib.unified_diff(base.splitlines(True), new.splitlines(True), 'a/' + rel, 'b/' + rel, n=3)
        out.append(''.join(x if x.endswith('\n') else x + '\n' for x in d))
    open(P + name, 'w', encoding='utf-8', newline='').write(''.join(out))
    print(name, sum(o.count('\n') for o in out))


# -- The skill
s = read('Skills.cs')
n = sub(s, '    Throwing = 57\n', '    Throwing = 57,\n    Herbalism = 58 // Shattered Legacy (cc-P804, F-51)\n')
n = sub(n, '    public Skill Throwing => this[SkillName.Throwing];\n', '    public Skill Throwing => this[SkillName.Throwing];\n\n    [CommandProperty(AccessLevel.Counselor)]\n    public Skill Herbalism => this[SkillName.Herbalism];\n')
j = read('skills.json')
row = '''  },
  {
    "SkillID": 58,
    "Name": "Herbalism",
    "Title": "Herbalist",
    "StrScale": 0,
    "DexScale": 0.05,
    "IntScale": 0.05,
    "StatTotal": 10,
    "StrGain": 0,
    "DexGain": 0.5,
    "IntGain": 0.5,
    "GainFactor": 1,
    "ProfessionSkillName": "Herbalism",
    "PrimaryStat": "Int",
    "SecondaryStat": "Dex"
  }
]
'''
assert j.endswith('  }\n]\n')
jn = j[:-len('  }\n]\n')] + row
am = read('AntiMacroSystem.cs')
amn = sub(am, '        false, // Throwing = 57\n', '        false, // Throwing = 57\n        false, // Herbalism = 58, Shattered Legacy (cc-P804): the table must hold every SkillName\n')
patch('Skills-herbalism.patch', [('Projects/Server/Skills.cs', s, n), ('Projects/UOContent/Skills/AntiMacroSystem.cs', am, amn)])
patch('skills-json-herbalism.patch', [('Distribution/Data/skills.json', j, jn)])

# -- The lane
t = read('PlantType.cs')
tn = sub(t, '        SugarCanes,\n        CocoaTree\n    }\n', '        SugarCanes,\n        CocoaTree,\n\n        // Shattered Legacy (cc-P804, F-51): the reagent lane (HerbalLane). They cross only each other.\n        Garlic,\n        Ginseng,\n        Mandrake,\n        Nightshade,\n        BloodMoss\n    }\n')
tail = 'PlantType.CocoaTree, false, false, false, false, PlantCategory.Peculiar'
i = tn.index('PlantType.CocoaTree', tn.index('m_Table'))
j2 = tn.index('\n        };', i)
rows = ''.join('\n            new(0x%04X, 0, 0, PlantType.%s, false, false, true, true, PlantCategory.Default),' % (a, b) for a, b in [(0x18E1, 'Garlic'), (0x18E9, 'Ginseng'), (0x18DF, 'Mandrake'), (0x18E5, 'Nightshade'), (0xC9F, 'BloodMoss')])
tn = tn[:j2].rstrip(',') + ',' + rows + tn[j2:]
tn = sub(tn, '        public static PlantType Cross(PlantType first, PlantType second)\n        {\n', '        public static PlantType Cross(PlantType first, PlantType second)\n        {\n            if (HerbalLane.IsReagent(first) || HerbalLane.IsReagent(second))\n            {\n                return HerbalLane.Cross(first, second); // Shattered Legacy (cc-P804)\n            }\n\n')

r = read('PlantResources.cs')
rn = sub(r, '            new(PlantType.CocoaTree, PlantHue.Plain, typeof(CocoaPulp))\n', '            new(PlantType.CocoaTree, PlantHue.Plain, typeof(CocoaPulp)),\n\n            // Shattered Legacy (cc-P804): the lane. HerbalLane.TryHarvest does the gathering; these rows show the count in the gump.\n            new(PlantType.Garlic, PlantHue.Plain, typeof(RawHerb)),\n            new(PlantType.Ginseng, PlantHue.Plain, typeof(RawHerb)),\n            new(PlantType.Mandrake, PlantHue.Plain, typeof(RawHerb)),\n            new(PlantType.Nightshade, PlantHue.Plain, typeof(RawHerb)),\n            new(PlantType.BloodMoss, PlantHue.Plain, typeof(RawHerb))\n')

o = read('PollinateTarget.cs')
on = sub(o, '                    else if (targ == m_Plant)\n', '                    else if (HerbalLane.RefusesPollen(m_Plant, targ))\n                    {\n                        // Shattered Legacy (cc-P804): reagent plants and stock plants do not cross.\n                        targ.LabelTo(from, "These plants will not cross.");\n                    }\n                    else if (targ == m_Plant)\n')
on = sub(on, '                        targ.LabelTo(from, 1053071); // You pollinate the plant with its own pollen.\n', '                        HerbalLane.OnPollinated(from, m_Plant, targ); // Shattered Legacy (cc-P804)\n                        targ.LabelTo(from, 1053071); // You pollinate the plant with its own pollen.\n')
on = sub(on, '                        targ.LabelTo(from, 1053076); // You successfully cross-pollinate the plant.\n', '                        HerbalLane.OnPollinated(from, m_Plant, targ); // Shattered Legacy (cc-P804)\n                        targ.LabelTo(from, 1053076); // You successfully cross-pollinate the plant.\n')

g = read('ReproductionGump.cs')
gn = sub(g, '                    var resInfo = PlantResourceInfo.GetInfo(_plant.PlantType, _plant.PlantHue);\n                    var system = _plant.PlantSystem;\n\n                    if (resInfo == null)\n', '                    if (HerbalLane.TryHarvest(from, _plant)) // Shattered Legacy (cc-P804)\n                    {\n                        break;\n                    }\n\n                    var resInfo = PlantResourceInfo.GetInfo(_plant.PlantType, _plant.PlantHue);\n                    var system = _plant.PlantSystem;\n\n                    if (resInfo == null)\n')
gn = sub(gn, '                        var seed = new Seed(system.SeedType, system.SeedHue, true);\n', '                        var seed = HerbalLane.NewSeed(_plant, system); // Shattered Legacy (cc-P804)\n')

it = read('PlantItem.cs')
inew = sub(it, '            ItemID = PlantTypeInfo.GetInfo(_plantType).ItemID;\n            Hue = PlantHueInfo.GetInfo(_plantHue).Hue;\n', '            ItemID = PlantTypeInfo.GetInfo(_plantType).ItemID;\n            Hue = HerbalLane.PlantHueFor(this, PlantHueInfo.GetInfo(_plantHue).Hue); // Shattered Legacy (cc-P804)\n')
inew = sub(inew, '                $"{health:#}\\t{hueInfo.Name:#}\\t{typeInfo.Name:#}"\n            );\n            return;\n', '                $"{health:#}\\t{hueInfo.Name:#}\\t{typeInfo.Name:#}"\n            );\n            HerbalLane.AddProperties(this, list); // Shattered Legacy (cc-P804)\n            return;\n')
inew = sub(inew, '        else if (RequiresUpkeep && PlantSystem.Water < 2)\n        {\n            LabelTo(from, 1061920); // The dirt needs to be softened first.\n        }\n        else\n        {\n            PlantType = seed.PlantType;\n', '        else if (RequiresUpkeep && PlantSystem.Water < 2)\n        {\n            LabelTo(from, 1061920); // The dirt needs to be softened first.\n        }\n        else if (HerbalLane.MayPlant(from, seed)) // Shattered Legacy (cc-P804): its own message when not\n        {\n            var strain = (seed as ReagentSeed)?.StrainTier ?? 0;\n\n            PlantType = seed.PlantType;\n')
inew = sub(inew, '            PlantSystem.Reset(false);\n\n            LabelTo(from, OnPlantLocalization);', '            PlantSystem.Reset(false);\n            HerbalLane.OnPlanted(from, this, strain);\n\n            LabelTo(from, OnPlantLocalization);')
inew = sub(inew, '            from.PlaySound(0x4E);\n            LabelTo(from, 1061858); // You soften the dirt with water.\n', '            from.PlaySound(0x4E);\n            HerbalLane.Tended(from, this); // Shattered Legacy (cc-P804)\n            LabelTo(from, 1061858); // You soften the dirt with water.\n')
inew = sub(inew, '                from.PlaySound(0x240);\n                from.AddToBackpack(new Bottle());\n', '                from.PlaySound(0x240);\n                from.AddToBackpack(new Bottle());\n                HerbalLane.Tended(from, this); // Shattered Legacy (cc-P804)\n')
inew = sub(inew, '                keg.Held--;\n                from.PlaySound(0x240);\n', '                keg.Held--;\n                from.PlaySound(0x240);\n                HerbalLane.Tended(from, this); // Shattered Legacy (cc-P804)\n')

y = read('PlantSystem.cs')
yn = sub(y, '            NextGrowth = now + CheckDelay;\n\n            if (!Plant.ValidGrowthLocation)\n', '            NextGrowth = now + HerbalLane.GrowthDelay(this); // Shattered Legacy (cc-P804)\n\n            if (!Plant.ValidGrowthLocation)\n')
yn = sub(yn, '            ApplyBeneficialEffects();\n\n            if (!ApplyMaladiesEffects()) // Dead\n', '            HerbalLane.OnGrowthCheck(this); // Shattered Legacy (cc-P804): neglect\n\n            ApplyBeneficialEffects();\n\n            if (!ApplyMaladiesEffects()) // Dead\n')
yn = sub(yn, '            // Shattered Legacy (cc-P128): no water or malady damage without upkeep (ServUO PlantSystem.cs:523).\n            if (!Plant.RequiresUpkeep)\n', '            // Shattered Legacy (cc-P128): no water or malady damage without upkeep (ServUO PlantSystem.cs:523).\n            // cc-P804: the reagent lane owns its plants\' damage (HerbalLane.OnGrowthCheck).\n            if (!Plant.RequiresUpkeep || HerbalLane.SparesDamage(this))\n')
yn = sub(yn, '            // Shattered Legacy (cc-P128): no new maladies without upkeep (ServUO PlantSystem.cs:597).\n            if (!Plant.RequiresUpkeep)\n', '            // Shattered Legacy (cc-P128): no new maladies without upkeep (ServUO PlantSystem.cs:597).\n            // cc-P804: a reagent bed\'s rate is a share of a bowl\'s.\n            if (!Plant.RequiresUpkeep || HerbalLane.SkipsMaladies(this))\n')
yn = sub(yn, '                if (LeftResources > 0 && PlantResourceInfo.GetInfo(Plant.PlantType, Plant.PlantHue) != null)\n', '                if (HerbalLane.OnMature(this))\n                {\n                    // Shattered Legacy (cc-P804): perennial\n                }\n                else if (LeftResources > 0 && PlantResourceInfo.GetInfo(Plant.PlantType, Plant.PlantHue) != null)\n')

patch('Plants-herbalism-lane.patch', [(PL + 'PlantType.cs', t, tn), (PL + 'PlantResources.cs', r, rn), (PL + 'PollinateTarget.cs', o, on), (PL + 'ReproductionGump.cs', g, gn), (PL + 'PlantItem.cs', it, inew), (PL + 'PlantSystem.cs', y, yn)])

f = read('FeatureFlagManager.cs')
fn = sub(f, 'new SkillBlockEntry[58];', 'new SkillBlockEntry[SkillInfo.Table.Length]; // Shattered Legacy (cc-P804): 59 with Herbalism')
patch('FeatureFlagManager-skill-count.patch', [('Projects/UOContent/Engines/FeatureFlags/FeatureFlagManager.cs', f, fn)])
