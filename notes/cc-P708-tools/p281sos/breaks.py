# cc-P281: the red runs' breaks (WRITES the code repo), and "restore" (byte copies, SHA-256 checked).
#   python -P breaks.py apply 1 2 3 4 5     apply those breaks (pristine copies saved first)
#   python -P breaks.py restore              put every touched file back and check its SHA-256
# Each break targets one fact of GuildHallPlacementVerification:
#   1 the table: warriors' guildmaster one tile south in the C# table only            -> TheTableIsTheDesignFile
#   2 the rangers' guildmaster type is pinned's stock RangerGuildmaster              -> EveryGuild...OwnGuildmaster
#   3 Refusal never refuses                                                          -> OnTheLiveShard...
#   4 clear forgets to show the stock sign it hid                                    -> PlaceTwice...ClearRemovesExactly
#   5 the sign's hall key is altered after a load                                    -> TheSign...RoundTrip
#   6 place forgets that a sign already stands (places it twice)                     -> PlaceTwice... (run alone)
import hashlib
import json
import os
import shutil
import sys

REPO = 'D:/UO/golems/Iron/ShatteredLegacy'
KEEP = os.path.join(os.environ.get('P281_SCRATCH', os.path.join(os.environ['TEMP'], 'p281-pristine')))
DATA = 'server/customizations/ClusterFGuildHallPlacementData.cs'
CODE = 'server/customizations/ClusterFGuildHallPlacement.cs'
BREAKS = {
    1: (DATA, 'typeof(WarriorGuildmaster), new Point3D(1362, 3716, 0)', 'typeof(WarriorGuildmaster), new Point3D(1362, 3717, 0)'),
    2: (DATA, 'typeof(OutridersGuildmaster)', 'typeof(RangerGuildmaster)'),
    3: (CODE, '            isTestShard\n                ? null\n', '            isTestShard || true\n                ? null\n'),
    4: (CODE, '                        stock.Visible = true;\n', '                        _ = stock; // P281-BREAK\n'),
    5: (CODE, '        public override bool Decays => false;\n    }\n\n    /// <summary>A new guild hall',
        '        public override bool Decays => false;\n\n        [AfterDeserialization]\n        private void P281Break() => _hallKey += "-";\n    }\n\n    /// <summary>A new guild hall'),
    6: (CODE, '                if (parts.OfType<GuildHallSign>().Any())\n', '                if (false && parts.OfType<GuildHallSign>().Any())\n'),
}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def apply(ns):
    os.makedirs(KEEP, exist_ok=True)
    manifest = os.path.join(KEEP, 'manifest.json')
    m = json.load(open(manifest)) if os.path.exists(manifest) else {}
    for n in ns:
        rel, old, new = BREAKS[n]
        p = os.path.join(REPO, rel)
        if rel not in m:
            shutil.copyfile(p, os.path.join(KEEP, os.path.basename(rel)))
            m[rel] = sha(p)
        src = open(p, newline='').read()
        crlf = '\r\n' in src
        o, w = (old.replace('\n', '\r\n'), new.replace('\n', '\r\n')) if crlf else (old, new)
        assert src.count(o) == 1, 'break %d: anchor found %d times' % (n, src.count(o))
        open(p, 'w', newline='').write(src.replace(o, w))
        print('break %d applied to %s' % (n, rel))
    json.dump(m, open(manifest, 'w'))


def restore():
    manifest = os.path.join(KEEP, 'manifest.json')
    m = json.load(open(manifest))
    for rel, h in m.items():
        p = os.path.join(REPO, rel)
        shutil.copyfile(os.path.join(KEEP, os.path.basename(rel)), p)
        assert sha(p) == h, rel
        print('restored', rel, h[:12])
    os.remove(manifest)


if __name__ == '__main__':
    if sys.argv[1] == 'apply':
        apply([int(v) for v in sys.argv[2:]])
    else:
        restore()
