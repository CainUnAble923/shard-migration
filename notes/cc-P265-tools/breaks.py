"""cc-P265: the red run's breaks, one per server fact, and their restore.

    python -P breaks.py apply <ShatteredLegacy repo> <pristine dir> [n,m]  copy each file to <pristine dir>, then break
                                                                       it (all breaks, or only those numbered)
    python -P breaks.py restore <ShatteredLegacy repo> <pristine dir>  copy the pristine files back, check SHA-256

Each break is an exact text that must occur once; every changed line carries P265-BREAK.
"""
import hashlib
import os
import shutil
import sys

GEN = "server/customizations/GuildHallDecor/"
BREAKS = [
    # 1. the server's table drifts from the design: the large tower's turret one z higher
    (GEN + "GuildHallDecorTemplates.cs", 'new(0x6E5C, "tower turret", 3, 3, 20, 0, "large-turret")',
     'new(0x6E5C, "tower turret", 3, 3, 21, 0, "large-turret") /* P265-BREAK */'),
    # 2. the catalogue has a gap: the vat's first part claims 3 frames, not 4
    (GEN + "GuildHallDecorArt.cs", 'new("vat-1", 0x6D70, 4,', 'new("vat-1", 0x6D70, /* P265-BREAK */ 3,'),
    # 3. the live shard is not refused
    (GEN + "GuildHallDecorSeeder.cs", "            isTestShard\n                ? null",
     "            isTestShard || true // P265-BREAK\n                ? null"),
    # 4. place forgets what is already standing
    (GEN + "GuildHallDecorSeeder.cs", "                    if (standing.Contains((g.Key, r)))",
     "                    if (false && standing.Contains((g.Key, r))) // P265-BREAK"),
    # 5. the group key is not kept as given
    (GEN + "GuildHallDecorSeeder.cs", "            _groupKey = groupKey;", "            _groupKey = groupKey + \"-\"; // P265-BREAK"),
    # 6. the records are never written
    (GEN + "GuildHallDecorArt.cs", "        foreach (var p in Pieces)\n        {\n            TileData",
     "        foreach (var p in System.Array.Empty<Piece>()) // P265-BREAK\n        {\n            TileData"),
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    cmd, repo, pristine = sys.argv[1:4]
    only = [int(n) for n in sys.argv[4].split(",")] if len(sys.argv) > 4 else None   # 1-based break numbers
    breaks = [b for i, b in enumerate(BREAKS, 1) if only is None or i in only]
    files = sorted({f for f, _, _ in breaks})
    if cmd == "apply":
        os.makedirs(pristine, exist_ok=True)
        for f in files:
            shutil.copyfile(os.path.join(repo, f), os.path.join(pristine, os.path.basename(f)))
        for f, old, new in breaks:
            p = os.path.join(repo, f)
            s = open(p, encoding="utf-8").read()
            assert s.count(old) == 1, (f, old)
            open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
        print("applied", len(breaks), "breaks to", len(files), "files")
    else:
        for f in files:
            src = os.path.join(pristine, os.path.basename(f))
            shutil.copyfile(src, os.path.join(repo, f))
            assert sha(src) == sha(os.path.join(repo, f))
            assert "P265-BREAK" not in open(os.path.join(repo, f), encoding="utf-8").read()
        print("restored", len(files), "files, SHA-256 equal, no P265-BREAK left")


main()
