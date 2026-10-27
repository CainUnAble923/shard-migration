"""cc-P713: the map files of a switched-off package against the published 2026.10.26.1648 package.

    python -P compare_1648.py <1648 zip> <new zip>

Map files: everything under app/map/, every .mul/.uop/.idx in the zip, app/trammel.mapops (line by line: only the
isle's lines may be new), and the launcher's map scripts (named, with their sizes; they changed in cc-P674 on purpose).
The README is compared too: with the switch off it must hold no Siege of Sosaria map entry.
"""
import difflib
import hashlib
import sys
import zipfile


def load(path):
    z = zipfile.ZipFile(path)
    out = {}
    for i in z.infolist():
        if i.filename.endswith('/'):
            continue
        out[i.filename.split('/', 1)[1]] = z.read(i)
    return out


old, new = load(sys.argv[1]), load(sys.argv[2])
print(f'1648: {len(old)} files; new: {len(new)} files')


def mapfile(n):
    return n.startswith('app/map/') or n.lower().endswith(('.mul', '.uop', '.idx'))


for label, files in (('1648', old), ('new', new)):
    print(f'{label}: app/map/ and map data files: {sorted(n for n in files if mapfile(n)) or "none"}')

a = old['app/trammel.mapops'].decode('ascii').splitlines()
b = new['app/trammel.mapops'].decode('ascii').splitlines()
sa, sb = set(a), set(b)
removed = [l for l in a if l not in sb]
added = [l for l in b if l not in sa]
print(f'trammel.mapops: 1648 {len(a)} lines, new {len(b)}; lines gone {len(removed)}, lines new {len(added)}')
print(f'  1648 sha256 {hashlib.sha256(old["app/trammel.mapops"]).hexdigest()}')
print(f'  new  sha256 {hashlib.sha256(new["app/trammel.mapops"]).hexdigest()}')
for l in removed[:20]:
    print('  - ' + l)
for l in added[:40]:
    print('  + ' + l)
if len(added) > 40:
    print(f'  ... {len(added) - 40} more new lines')
kinds = {}
for l in added:
    kinds[l.split(' ', 1)[0]] = kinds.get(l.split(' ', 1)[0], 0) + 1
print(f'  new lines by kind: {kinds}')

for n in ('app/Apply-MapOps.ps1', 'app/Build-UoOverrides.ps1'):
    same = old.get(n) == new.get(n)
    print(f'{n}: {"same" if same else "changed"} ({len(old.get(n, b""))} -> {len(new.get(n, b""))} bytes)')

ra = old['README.txt'].decode('ascii').splitlines()
rb = new['README.txt'].decode('ascii').splitlines()
print('README.txt diff (1648 -> new):')
for l in difflib.unified_diff(ra, rb, lineterm='', n=0):
    print('  ' + l)
print('new README names the SoS map:', 'Siege of Sosaria Trammel Map' in '\n'.join(rb))
