"""cc-P708: the SoS client folder the hall checks read, D:/UO/golems/Iron/p708-work/sosclient: P677's folder (stock client
files, hard links) with Trammel's three map files rebuilt from the pristine SoS base (the code copy's
player-package/vendor/sos-trammel-map/files, hashes in notes/cc-P675-tools/sos-base/ORIGINAL-SHA256.txt) plus today's
trammel.mapops, so P687's boulders, P691 and P741 are in. Facet 0's map file is a copy of facet 1's, as P677 had it
(the server reads Felucca from Trammel's files, P675).
    python -P make_sosclient.py
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(DOCS, 'scripts'))
from mapbuild import mapops  # noqa: E402

CODE = 'D:/UO/golems/Iron/ShatteredLegacy'
SRC = 'D:/UO/golems/Iron/p677-work/sosclient'
OUT = 'D:/UO/golems/Iron/p708-work/sosclient'
VENDOR = CODE + '/player-package/vendor/sos-trammel-map/files'
PATCH = CODE + '/player-package/vendor/shattered-legacy-map/trammel.mapops'
HASHES = os.path.join(DOCS, 'notes', 'cc-P675-tools', 'sos-base', 'ORIGINAL-SHA256.txt')
NAMES = ('map1LegacyMUL.uop', 'statics1.mul', 'staidx1.mul')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


want = {}
for line in open(HASHES):
    if line.strip():
        h, n = line.split()
        want[n.lstrip('*').lower()] = h

base = os.path.join(os.path.dirname(OUT), 'sosbase')
os.makedirs(base, exist_ok=True)
for n in NAMES:
    src = os.path.join(VENDOR, 'base-' + n.lower())
    dst = os.path.join(base, n)
    shutil.copyfile(src, dst)
    assert sha(dst) == want[n.lower()], n
print('base ok: the pristine SoS files')

if not os.path.exists(OUT):
    os.makedirs(OUT)
    for root, dirs, files in os.walk(SRC):
        rel = os.path.relpath(root, SRC)
        os.makedirs(os.path.join(OUT, rel), exist_ok=True)
        for f in files:
            os.link(os.path.join(root, f), os.path.join(OUT, rel, f))
for n in NAMES + ('map0LegacyMUL.uop',):
    p = os.path.join(OUT, n)
    if os.path.exists(p):
        os.remove(p)  # unlink, never write through a hard link
drifted, missing = mapops.apply(open(PATCH).read(), base, OUT, 1)
assert not drifted and not missing, (drifted[:5], missing[:5])
mapops.rename_uop(os.path.join(OUT, 'map1LegacyMUL.uop'), os.path.join(OUT, 'map0LegacyMUL.uop'), 1, 0)
print('wrote', OUT, 'patch', sha(PATCH)[:16], 'map1', sha(os.path.join(OUT, 'map1LegacyMUL.uop'))[:16])
