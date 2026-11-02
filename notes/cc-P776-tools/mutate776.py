# cc-P776: makes one mutant copy of server/customizations/Encounters per rule, each with that rule broken, under
# <out>/<name>/Encounters. run-mutants.sh probes each; every one must turn at least one fact red.
# Usage: python -I mutate776.py <out folder>
import os
import shutil
import sys

SRC = r'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Encounters'
F = 'ClusterFEncounters.cs'

MUTANTS = [
    ('off-switch', 'if (!t.Enabled)\n', 'if (false)\n'),
    ('staff', 'if (pm.AccessLevel > AccessLevel.Player)', 'if (false)'),
    ('dead', 'if (!pm.Alive)', 'if (false)'),
    ('young', 'if (pm.Young || pm.Account is Account { Young: true })', 'if (false)'),
    ('trainee', 'if (LoopOf(pm) <= 0)', 'if (false)'),
    ('hidden', 'if (pm.Hidden)', 'if (false)'),
    ('idle', 'if (!Traveled(pm, now))', 'if (false)'),
    ('combat', 'if (InCombat(pm))', 'if (false)'),
    ('already-in-one', 'if (EncounterOf(pm) != null)', 'if (false)'),
    ('cooldown', 'if (_characterCooldown.TryGetValue(pm.Serial, out var until) && now < until)', 'if (false)'),
    ('account-cooldown', '_accountCooldown.TryGetValue(acct.Username, out var acctUntil) && now < acctUntil', 'false'),
    ('crowd', 'Utility.InRange(e.Spot, pm.Location, t.CrowdRange)', 'false'),
    ('isle', 'if (map.MapIndex >= FoldMaps.FoldIndex)', 'if (false)'),
    ('facets', 'if (!t.Facets.Any(f => string.Equals(f, map.Name, StringComparison.OrdinalIgnoreCase)))', 'if (false)'),
    ('deny-regions', 'if (region.IsPartOf(name))', 'if (false)'),
    ('town', 'if (region.GetRegion<GuardedRegion>() is { } guarded && (!guarded.IsDisabled() || guarded is TownRegion))', 'if (false)'),
    ('dungeon', 'if (region.IsPartOf<DungeonRegion>())', 'if (false)'),
    ('house', 'if (BaseHouse.FindHouseAt(pm) != null)', 'if (false)',
     'if (region.IsPartOf<HouseRegion>() || BaseHouse.FindHouseAt(p, map, 16) != null)', 'if (false)'),
    ('boat', 'public static bool NearBoat(Map map, Point3D p)\n    {', 'public static bool NearBoat(Map map, Point3D p)\n    {\n        return false;'),
    ('season', 'return def.Season == null || InSeason(def.Season);', 'return true;'),
    ('league', 'if (def.LeagueOnly && !IsLeague(pm))', 'if (false)'),
    ('night', 'if (def.Time != EncounterTime.Any && IsNight(pm.Map!, pm.Location) != (def.Time == EncounterTime.Night))', 'if (false)'),
    ('toll-cap', 'Math.Min(def.TollCap, gold * def.TollPercent / 100)', 'gold * def.TollPercent / 100'),
    ('toll-deadline', 'case EncounterKind.Toll when e.Stage == EncounterStage.Open && now >= e.TollDeadline:', 'case EncounterKind.Toll when false:'),
    ('follow-into-town', 'if (!bc.Deleted && bc.Alive && WhyNotHere(bc.Map, bc.Location) != null)', 'if (false)'),
    ('leave-late', 'if (now >= e.LeaveAt)', 'if (now > e.LeaveAt + TimeSpan.FromMinutes(1))'),
    ('leave-early', 'if (now >= e.LeaveAt)', 'if (now >= e.LeaveAt - TimeSpan.FromMinutes(2))'),
    ('fighter-removed', 'public static bool Fighting(BaseCreature bc) => bc.Combatant != null;', 'public static bool Fighting(BaseCreature bc) => false;'),
    ('dawn', 'e.LeaveAt = now;\n                        break;', 'break;'),
    ('restart-sweep', 'bc.Delete();\n                removed++;', 'removed++;'),
    ('tamable', 'bc.Tamable = false;', ''),
    ('surveyor-target', 'bc.Combatant = ally;', ''),
]


def main():
    out = sys.argv[1]
    names = []
    for m in MUTANTS:
        name, pairs = m[0], m[1:]
        s = open(os.path.join(SRC, F), encoding='utf-8').read()
        for i in range(0, len(pairs), 2):
            old, new = pairs[i], pairs[i + 1]
            if old not in s:
                raise SystemExit(f'{name}: pattern not found: {old[:60]}')
            s = s.replace(old, new, 1)
        dest = os.path.join(out, name, 'Encounters')
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        shutil.copytree(SRC, dest)
        open(os.path.join(dest, F), 'w', encoding='utf-8').write(s)
        names.append(name)
    open(os.path.join(out, 'mutants.txt'), 'w', encoding='utf-8').write('\n'.join(names) + '\n')
    print(f'{len(names)} mutants in {out}')


main()
