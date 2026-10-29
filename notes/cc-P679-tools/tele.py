"""cc-P679 (SoS swap S4): every Trammel and Felucca teleporter end of pinned's Data/teleporters.json, graded on the
land the server reads.

    python -P tele.py <overlay> <code copy> [--out out-tele.csv]

An end on Trammel or Felucca (both read the SoS files, SosMaps.cs) is graded with P677's spot rule (spots.Land.check:
a standing surface, nothing impassable in the 16 Z above, its Z within 5 of the surface). Each end also gets the
region it lies in from P676's regions-trammel.json (the author's dungeons are named there) and whether that region is
one of pinned's own Trammel regions (stock) or new (the author's).

A source end must also fire: pinned Mobile.Move hands OnMoveOver to an item at the new tile when item.Z == newZ, or
item.Z + height > newZ and newZ + 15 > item.Z (Mobile.cs:4224-4228). A teleporter (0x1BC3) is 1 high, so its Z must
lie from the walker's floor to 14 above it. A source below every floor it could be walked onto never fires.
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sosland  # noqa: E402

PINNED = r'D:\UO\ModernUO-pinned\Distribution\Data'
SOS_MAPS = ('Trammel', 'Felucca')


def load_regions(code):
    ours = json.load(open(os.path.join(code, 'server', 'data', 'regions-trammel.json'), encoding='utf-8'))
    pinned = json.load(open(os.path.join(PINNED, 'regions.json'), encoding='utf-8'))
    stock = {r['Name'] for r in pinned if r.get('Map') == 'Trammel' and r.get('Name')}
    return ours, stock


def region_at(regions, x, y, z):
    """The highest-priority region whose rect holds (x, y, z): (name, type)."""
    best = None
    for r in regions:
        for a in r.get('Area', []):
            if a['x1'] <= x <= a['x2'] and a['y1'] <= y <= a['y2'] and a.get('z1', -128) <= z <= a.get('z2', 127):
                if best is None or r.get('Priority', 0) > best.get('Priority', 0):
                    best = r
    return (best['Name'], best['$type']) if best else ('', '')


def fires(L, x, y, z):
    """A source end at z fires for someone standing on one of this tile's open floors."""
    return any(top <= z <= top + 14 for top in L.open_tops(x, y))


def ends(entry):
    yield 'src', entry['src']
    yield 'dst', entry['dst']


def grade(folder, code):
    L = sosland.land(folder)
    regions, stock = load_regions(code)
    tele = json.load(open(os.path.join(PINNED, 'teleporters.json'), encoding='utf-8'))
    rows = []
    for i, e in enumerate(tele):
        for which, w in ends(e):
            if w['map'] not in SOS_MAPS:
                continue
            x, y, z = w['loc']
            v = L.check(x, y, z)
            if v == 'ok' and which == 'src' and not fires(L, x, y, z):
                v = 'never fires: floors %s' % ','.join(str(o) for o in L.open_tops(x, y))
            name, typ = region_at(regions, x, y, z)
            rows.append(dict(index=i, end=which, map=w['map'], x=x, y=y, z=z, back=e['back'], verdict=v, region=name,
                             rtype=typ, stock_region=(name in stock) if name else '',
                             other='%s %d,%d,%d' % ((e['dst'] if which == 'src' else e['src'])['map'],
                                                     *(e['dst'] if which == 'src' else e['src'])['loc'])))
    return rows


def main():
    folder, code = sys.argv[1], sys.argv[2]
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'out-tele.csv')
    rows = grade(folder, code)
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    bad = [r for r in rows if r['verdict'] != 'ok']
    print('ends', len(rows), 'not ok', len(bad))
    for m in SOS_MAPS:
        print(' ', m, sum(r['map'] == m for r in rows), 'not ok', sum(r['map'] == m for r in bad))


if __name__ == '__main__':
    main()
