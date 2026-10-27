"""cc-P674: copies of the built zip, each with one thing gate 4 must refuse, and a check script for each.
    python -P gate4_mutants.py <built zip> <out folder>"""
import os
import sys
import zipfile

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
top = zipfile.ZipFile(src).namelist()[0].split('/')[0]


def mutant(name, change=None, extra=None):
    dst = os.path.join(out, name + '.zip')
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zo:
        for i in zi.infolist():
            if i.filename.endswith('/'):
                continue
            data = zi.read(i.filename)
            if change and i.filename.endswith(change[0]):
                data = change[1](data)
            zo.writestr(i.filename, data)
        for n, d in (extra or []):
            zo.writestr(top + '/' + n, d)
    return dst


def flip(d):
    b = bytearray(d)
    b[1000] ^= 1
    return bytes(b)


mutant('changed-map', change=('app/map/base-statics1.mul', flip))
mutant('ea-named-map', extra=[('app/map/statics1.mul', b'x' * 70)])
mutant('stray-mul', extra=[('app/extra/statics9.mul', b'x' * 70)])
print('top', top)
