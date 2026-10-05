# P62 red run for Build-PlayerPackage.ps1 gate 4: doctored copies of the real zip, one break each.
import json, struct, sys, zipfile, os
SRC = sys.argv[1]
OUT = r'D:\UO\cc-p62-work\pkg-red'
os.makedirs(OUT, exist_ok=True)
top = zipfile.ZipFile(SRC).namelist()[0].split('/')[0]


def variant(name, change):
    dst = os.path.join(OUT, name + '.zip')
    with zipfile.ZipFile(SRC) as zi, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zo:
        for e in zi.infolist():
            rel = e.filename[len(top) + 1:]
            data = zi.read(e)
            r = change(rel, data)
            if r is not None:
                zo.writestr(e, r)
    print(dst)


def drop(path):
    return lambda rel, d: None if rel == path else d


def recs(fn):
    def ch(rel, d):
        if rel != 'app/art-records.json':
            return d
        j = json.loads(d)
        fn(j)
        return json.dumps(j, indent=2).encode('ascii')
    return ch


def idx(fn):
    def ch(rel, d):
        if rel != 'app/sl-anim7-idx.bin':
            return d
        b = bytearray(d)
        fn(b)
        return bytes(b)
    return ch


variant('r1-no-gump', drop('app/tazuo/ExternalImages/gumps/64783.png'))
variant('r2-anim-unregistered', recs(lambda j: j['equipAnims'][0].update(anim=4784)))
variant('r3-block-outside-slot', idx(lambda b: struct.pack_into('<iii', b, 100 * 12, 0, 10, 0)))
variant('r4-no-mul', drop('app/sl-anim7.bin'))
variant('r5-block-past-end', idx(lambda b: struct.pack_into('<iii', b, (35000 + 5) * 12, 0, 999999, 0)))
variant('r6-no-equipanims', recs(lambda j: j.pop('equipAnims')))
