# cc-P281: per hall, a floor map of the P151 building (or plot) with doors, pinned spawners and pinned decoration
# marked, so the guildmaster, sign, decor and travel tiles can be picked. Read only.
#   python -P survey_halls.py [key ...]      writes survey-<key>.txt beside this file (git-ignored scratch)
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hallbase as H  # noqa: E402

# key, facet index, P151 rectangle (x1, y1, x2, y2), kind. Chase's picks of 2026-10-21 (cc-P281 prompt).
HALLS = [
    ('league', 1, (1320, 1586, 1366, 1665), 'reuse'),
    ('warriors', 1, (1352, 3696, 1376, 3720), 'reuse'),
    ('arcane', 1, (4278, 915, 4336, 1017), 'reuse'),
    ('healers', 1, (623, 816, 647, 856), 'reuse'),
    ('rangers', 1, (552, 2136, 576, 2160), 'share'),
    ('mining', 1, (2416, 520, 2440, 536), 'reuse'),
    ('smithing', 1, (3018, 3372, 3045, 3399), 'new'),
    ('tinkers', 1, (2880, 736, 2904, 752), 'reuse'),
    ('thieves', 0, (2655, 2072, 2681, 2096), 'reuse'),
    ('dojo', 4, (735, 1296, 789, 1316), 'share'),
    ('keepers', 3, (1983, 1351, 1999, 1365), 'reuse'),
    ('foresters', 1, (544, 808, 567, 831), 'reuse'),
    ('tailoring', 1, (3760, 1184, 3783, 1207), 'reuse'),
    ('merchants', 1, (3704, 2170, 3725, 2191), 'new'),
    ('bards', 1, (1440, 1576, 1460, 1600), 'reuse'),
    ('artificers', 5, (809, 3344, 841, 3373), 'reuse'),
    ('alembic', 1, (5723, 3182, 5762, 3209), 'share'),
    ('custodians', 1, (1447, 1701, 1474, 1716), 'reuse'),
]

_F = {}
# signs.cfg map column (pinned SignParser.cs): 0 Britannia (Felucca and Trammel), 1 Felucca, 2 Trammel, 3 Ilshenar,
# 4 Malas, 5 Tokuno. Ter Mur has none.
SIGN_MAPS = {0: (0, 1), 1: (0,), 2: (1,), 3: (2,), 4: (3,), 5: (4,)}
_SIGNS = None


def signs_in(fi, x1, y1, x2, y2):
    global _SIGNS
    if _SIGNS is None:
        _SIGNS = []
        for line in open(H.PINNED + '/Distribution/Data/signs.cfg'):
            p = line.split(' ', 5)
            if len(p) < 6:
                continue
            m, iid, x, y, z = (int(v) for v in p[:5])
            for f in SIGN_MAPS.get(m, ()):
                _SIGNS.append((f, x, y, z, iid, p[5].strip()))
    return [s for s in _SIGNS if s[0] == fi and x1 <= s[1] <= x2 and y1 <= s[2] <= y2]


def facet(fi):
    if fi not in _F:
        _F[fi] = H.Facet(fi)
    return _F[fi]


def floor_levels(F, x1, y1, x2, y2):
    """Counts of standable surface tops under a roof, by z (the building's floors)."""
    c = collections.Counter()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for sid, sz in F.statics(x, y):
                if H.iflags(sid) & H.SURF and not H.iflags(sid) & H.IMP:
                    tz = sz + H.calch(sid)
                    if F.roof_over(x, y, tz):
                        c[tz] += 1
    return c


def survey(key, fi, rect, kind, pad=4):
    F = facet(fi)
    x1, y1, x2, y2 = rect
    bx1, by1, bx2, by2 = x1 - pad, y1 - pad, x2 + pad, y2 + pad
    out = ['%s (%s) facet %d %s rect %s' % (key, kind, fi, H.FNAME[fi], rect)]
    levels = floor_levels(F, x1, y1, x2, y2)
    out.append('floors under a roof (z: tiles): %s' % dict(levels.most_common(6)))
    land = collections.Counter(F.avgz(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1))
    out.append('land avg z (z: tiles): %s' % dict(land.most_common(6)))
    doors = H.generated_doors(F, bx1, by1, bx2, by2)
    sdoors = H.static_doors(F, bx1, by1, bx2, by2)
    out.append('generated doors: %s' % doors)
    out.append('static doors: %s' % sdoors)
    sp = H.spawns_in(H.FNAME[fi], bx1, by1, bx2, by2)
    for s in sp:
        out.append('spawner %d,%d,%d range %d %s (%s)' % (s[1], s[2], s[3], s[4], s[5], s[6]))
    dec = H.decoration_in(fi, bx1, by1, bx2, by2)
    for d in dec:
        out.append('decoration %d,%d,%d %s %s (%s)' % d)
    for sg in signs_in(fi, bx1, by1, bx2, by2):
        out.append('sign %d,%d,%d 0x%04X %s facing %s' % (sg[1], sg[2], sg[3], sg[4], sg[5], ('North', 'West')[(sg[4] - 0xB95) % 2]))
    tele = H.teleporters_in(H.FNAME[fi], bx1, by1, bx2, by2)
    for t in tele:
        out.append('teleporter %s' % (t,))
    zs = [z for z, _ in levels.most_common(3)] or [land.most_common(1)[0][0]]
    for fz in sorted(zs):
        marks = {}
        for (x, y, z, f) in doors:
            if abs(z - fz) <= 3:
                marks[(x, y)] = 'D'
        for s in sp:
            if abs(s[3] - fz) <= 5:
                marks[(s[1], s[2])] = 'S'
        for d in dec:
            if abs(d[2] - fz) <= 5:
                marks.setdefault((d[0], d[1]), 'd')
        out.append('')
        out.append('floor z%d (# wall, D door, t blocker, . floor, ~ ground, S spawner, d decoration item)' % fz)
        out.append(H.floormap(F, bx1, by1, bx2, by2, fz, marks=marks))
    return '\n'.join(out)


if __name__ == '__main__':
    want = set(sys.argv[1:])
    for key, fi, rect, kind in HALLS:
        if want and key not in want:
            continue
        text = survey(key, fi, rect, kind)
        open('survey-%s.txt' % key, 'w').write(text + '\n')
        print(text.split('\n')[0], '|', text.split('\n')[1])
