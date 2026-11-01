"""cc-P714: survey of the two initiation sites on the SoS land (P708's p281sos copy of P281's hall tools).

    SL_SHARD_REPO=D:/UO/golems/Iron/ShatteredLegacy python -u -P -W ignore notes/cc-P714-tools/sites.py

For each site: the spawners and decoration within the box (what a beginner would meet), then each candidate tile:
standable at its Z, under open sky, and joined on foot to the site's way in (the author's points), and the tiles
reached. Candidates are the spots the initiation places (ClusterFInitiation*.cs): the teachers, the ankh, the patrol,
the field sites.
"""
import os
import sys

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P708-tools', 'p281sos'))
import hallbase as H  # noqa: E402
from walk import Walk  # noqa: E402

SITES = {
    'whitestone': {
        'box': (760, 980, 1100, 1200),
        'look': (850, 1000, 960, 1120),
        'from': [('Yew Forest Guardpost', (1047, 1080, 0)), ('fort stop', (890, 1058, 30))],
        'spots': {},
    },
    'dhampire': {
        'box': (1380, 2420, 1700, 2620),
        'look': (1420, 2460, 1530, 2570),
        'from': [('Shrine of Spirituality', (1602, 2490, 5))],
        'spots': {},
    },
}


def at(W, x, y, z, slack=3):
    hs = [h for h in W.heights(x, y) if abs(h - z) <= slack]
    return min(hs, key=lambda h: abs(h - z)) if hs else None


def survey(name, spots):
    s = SITES[name]
    x0, y0, x1, y1 = s['look']
    print('== %s' % name)
    sp = H.spawns_in('Trammel', x0, y0, x1, y1)
    print('spawners in %s: %d' % (s['look'], len(sp)))
    for e in sp:
        print('   (%d,%d,%d) range %s: %s  [%s]' % (e[1], e[2], e[3], e[4], ', '.join(n or '?' for n in e[5]), e[6]))
    dec = [d for d in H.decoration_in(1, x0, y0, x1, y1) if 'ankh' in d[3].lower() or 'Ankh' in d[4]]
    print('ankhs in decoration: %s' % dec)
    W = Walk(1, s['box'], pad=0)
    reach = None
    for label, p in s['from']:
        g = at(W, p[0], p[1], p[2], 6)
        if g is None:
            print('   from %s %s: not standable (%s)' % (label, p, W.heights(p[0], p[1])))
            continue
        r = W.flood((p[0], p[1], g))
        print('   from %s %s: %d tiles reached' % (label, p, len(r)))
        reach = r if reach is None else reach & r
    for key, (x, y, z) in spots.items():
        g = at(W, x, y, z)
        F = W.F
        if g is None:
            print('   %-14s (%d,%d,%d): NOT standable, heights %s' % (key, x, y, z, W.heights(x, y)))
            continue
        roof = F.roof_over(x, y, g)
        joined = reach is not None and (x, y, g) in reach
        print('   %-14s (%d,%d,%d): z %d, roof %s, joined %s  %s' % (key, x, y, z, g, roof, joined,
              'OK' if joined else 'NOT JOINED'))


if __name__ == '__main__':
    import json
    spots = json.load(open(os.path.join(os.path.dirname(__file__), 'spots.json'), encoding='utf-8'))
    for name in SITES:
        survey(name, {k: tuple(v) for k, v in spots.get(name, {}).items()})
