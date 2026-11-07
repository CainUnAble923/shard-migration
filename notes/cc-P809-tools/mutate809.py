# cc-P809: writes one folder per break under mutants/, each with the one mutated Pets file. Each break must turn a fact red.
import os, shutil, sys
SRC = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Pets'
OUT = 'D:/UO/golems/Iron/shard-migration/notes/cc-P809-tools/mutants'
M = [
 ('absorb10', 'HorseBarding.cs', 'AbsorbPercent { get; set; } = 5;', 'AbsorbPercent { get; set; } = 10;'),
 ('iron750', 'HorseBarding.cs', 'IronIngots { get; set; } = 400;', 'IronIngots { get; set; } = 750;'),
 ('smithtwice', 'HorseBarding.cs', '        _registered = true;\n        smith.AddCraft', '        smith.AddCraft'),
 ('anyowner', 'HorseBarding.cs', 'else if (!horse.Controlled || horse.ControlMaster != from)', 'else if (!horse.Controlled)'),
 ('anyhorse', 'HorseBarding.cs', 'm is Horse && m.GetType() == typeof(Horse);', 'm is Horse;'),
 ('pvp', 'HorseBarding.cs', 'if (from?.Player == true || m?.Player != true', 'if (m?.Player != true'),
 ('exceptional5', 'HorseBarding.cs', 'exceptional ? S.AbsorbPercentExceptional : S.AbsorbPercent', 'S.AbsorbPercent'),
 ('nolookback', 'HorseBarding.cs', '        horse.Body = r.OldBody;\n', ''),
 ('nowear', 'HorseBarding.cs', '        r.HP -= absorbed;\n', ''),
 ('keepdead', 'HorseBarding.cs', '            Rows.Remove(serial);\n        }\n\n        writer', '        }\n\n        writer'),
 ('anyversion', 'HorseBarding.cs', 'if (version is < 0 or > CurrentVersion)', 'if (version < 0)'),
 ('loseresource', 'HorseBarding.cs', '    [Constructible]\n    public CraftedHorseBarding()', '    [AfterDeserialization]\n    private void Lose() => _resource = CraftResource.Iron;\n\n    [Constructible]\n    public CraftedHorseBarding()'),
 ('novalidate', 'HorseBarding.cs', '        PetSettingsFile.Range(s.AbsorbPercent, 0, 100,', '        PetSettingsFile.Range(s.AbsorbPercent, 0, 1000,'),
 ('anykind', 'PetPerch.cs', '    public bool Takes(Mobile m)\n    {', '    public bool Takes(Mobile m)\n    {\n        return true;'),
 ('anyhouse', 'PetPerch.cs', '        if (house?.IsCoOwner(from) != true)\n        {\n            from.SendMessage("Pets can only be placed on perches in houses where you are an owner or co-owner.");\n            return null;\n        }\n\n        if (perch.Pet', '        if (perch.Pet'),
 ('keepfollower', 'PetPerch.cs', '        pet.SetControlMaster(null);\n', ''),
 ('notfrozen', 'PetPerch.cs', '        Frozen = true;\n        Blessed = true;', '        Blessed = true;'),
 ('twopets', 'PetPerch.cs', '        if (perch.Pet is { Deleted: false })\n        {\n            from.SendMessage("That perch already has a pet.");\n            return null;\n        }\n\n        if (target', '        if (target'),
 ('nofollow', 'PetPerch.cs', '            _pet.Location = new Point3D(X, Y, Z + PetPerch.S.PetHeight);', '            _pet.Location = _pet.Location;'),
 ('keepdeedpet', 'PetPerch.cs', '            _pet.Delete();\n        }\n    }\n}', '        }\n    }\n}'),
 ('logs50', 'PetPerch.cs', 'public int Logs { get; set; } = 100;', 'public int Logs { get; set; } = 50;'),
 ('nokindcheck', 'PetPerch.cs', 'errors.Add($"kind \\"{kind}\\" is not a creature.");', '_ = kind;'),
 ('rawkind', 'PetPerch.cs', '        var name = defaultName ?? "pet";\n', '        return defaultName ?? "pet";\n        var name = defaultName ?? "pet";\n'),
 ('losebirth', 'PetPerch.cs', '    private void AfterDeserialization()\n    {\n        Frozen = true;', '    private void AfterDeserialization()\n    {\n        _birth = Core.Now;\n        Frozen = true;'),
 ('losepet', 'PetPerch.cs', '    public override BaseAddon Addon => new PetPerchAddon(_pet);', '    [AfterDeserialization]\n    private void Lose() => _pet = null;\n\n    public override BaseAddon Addon => new PetPerchAddon(_pet);'),
 ('noname', 'PetPerch.cs', '            Name = from.Name;\n', ''),
]
shutil.rmtree(OUT, ignore_errors=True)
for name, f, old, new in M:
    s = open(os.path.join(SRC, f), encoding='utf-8').read()
    if s.count(old) != 1:
        print('NO MATCH', name, s.count(old)); continue
    d = os.path.join(OUT, name); os.makedirs(d)
    open(os.path.join(d, f), 'w', encoding='utf-8', newline='').write(s.replace(old, new))
print(len(os.listdir(OUT)), 'mutants')
