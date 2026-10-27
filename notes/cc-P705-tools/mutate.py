"""cc-P705 red runs: one copy of the edited Tutorial folder and CharacterCreation.cs per fix, with that fix's old
behaviour put back behind the new API (the new API does not exist before the change, so the facts cannot compile
there). The copies go to m-<name>/Tutorial and m-<name>/CharacterCreation.cs beside this file.

    python -P mutate.py <code copy>/server
"""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRV = sys.argv[1]
MUTANTS = {
    'surface': {'Tutorial/TutorialWorld.cs': [(
        "        var best = landAvg;\n        foreach",
        "        var best = landAvg;\n        return best; // P663: the land's average Z only\n        foreach")]},
    'havenoff': {'CharacterCreation.cs': [(
        "new(\"New Haven\", \"The Bountiful Harvest Inn\", 1150168, Server.Tutorial.HavenSpots.Start.X,\n            Server.Tutorial.HavenSpots.Start.Y, Server.Tutorial.HavenSpots.Start.Z, Server.Tutorial.HavenSpots.Map)",
        "new(\"New Haven\", \"The Bountiful Harvest Inn\", 1150168, 3503, 2574, 14, Map.Trammel)")]},
    'staff': {'Tutorial/TutorialStart.cs': [(
        "return ChoiceOf(city) == Choice.Isle ? (HavenSpots.Start, HavenSpots.Map) : (city.Location, city.Map);",
        "return (city.Location, city.Map);")]},
    'missing': {'Tutorial/TutorialStart.cs': [(
        "&& TutorialWorld.Isle != null && TutorialWorld.IsleReady()", "&& TutorialWorld.Isle != null"), (
        "if (outcome == Outcome.Isle && !TutorialWorld.IsleReady())", "if (false)")],
                'Tutorial/TutorialWorld.cs': [(
        "public static Func<bool> IsleReady { get; set; } = () => Isle is { } isle && isle.CanFit(Arrival, 16, false, false);",
        "public static Func<bool> IsleReady { get; set; } = () => true;")]},
}

for name, files in MUTANTS.items():
    out = os.path.join(HERE, 'm-' + name)
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(os.path.join(SRV, 'customizations', 'Tutorial'), os.path.join(out, 'Tutorial'))
    shutil.copyfile(os.path.join(SRV, 'customizations', 'CharacterCreation.cs'), os.path.join(out, 'CharacterCreation.cs'))
    for rel, pairs in files.items():
        p = os.path.join(out, rel)
        s = open(p, encoding='utf-8', newline='').read()
        crlf = '\r\n' in s
        s = s.replace('\r\n', '\n')
        for old, new in pairs:
            assert s.count(old) == 1, (name, rel, old[:60])
            s = s.replace(old, new)
        open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', '\r\n') if crlf else s)
    print('mutant', name)
