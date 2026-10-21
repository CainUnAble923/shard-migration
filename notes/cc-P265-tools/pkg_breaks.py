"""cc-P265: the package fact's red run: two mutations, and their restore.

    python -P pkg_breaks.py apply|restore <ShatteredLegacy repo> <pristine dir> [a|b|ab]
"""
import hashlib
import os
import shutil
import sys

V = "player-package/vendor/shattered-legacy-art/"
BREAKS = [
    # a: the vat's front band one taller in records.json than in GuildHallDecorArt
    (V + "records.json", '{ "id": 28048, "name": "bubbling vat", "flags": "0x00044040", "weight": 255, "layer": 0, "count": 0, "animId": 0, "hue": 0, "light": 0, "height": 8 }',
     '{ "id": 28048, "name": "bubbling vat", "flags": "0x00044040", "weight": 255, "layer": 0, "count": 0, "animId": 0, "hue": 0, "light": 0, "height": 9 }'),
    # b: a marble railing row loses its EA-derived mark
    (V + "registry.csv", 'credit Outlands in the shard credits, ship inside the player package (D:\\UO\\third-party\\marble-railings\\SOURCE.txt); EA-derived',
     'credit Outlands in the shard credits, ship inside the player package (D:\\UO\\third-party\\marble-railings\\SOURCE.txt); P265-BREAK'),
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


cmd, repo, pristine = sys.argv[1:4]
if len(sys.argv) > 4:                       # only the named mutations (a, b)
    BREAKS = [b for k, b in zip("ab", BREAKS) if k in sys.argv[4]]
files = sorted({f for f, _, _ in BREAKS})
if cmd == "apply":
    os.makedirs(pristine, exist_ok=True)
    for f in files:
        shutil.copyfile(os.path.join(repo, f), os.path.join(pristine, os.path.basename(f)))
    for f, old, new in BREAKS:
        p = os.path.join(repo, f)
        s = open(p, encoding="utf-8").read()
        assert s.count(old) >= 1, (f, old[:60])
        open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new, 1))
    print("applied", len(BREAKS))
else:
    for f in files:
        src = os.path.join(pristine, os.path.basename(f))
        shutil.copyfile(src, os.path.join(repo, f))
        assert sha(src) == sha(os.path.join(repo, f))
    print("restored", len(files), "files, SHA-256 equal")
