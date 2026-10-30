"""cc-P734: which way OSI's stair pieces climb, and where wall corners and posts stand, read from the classic house
multis (MultiCollection.uop). For each stair piece: its tile and Z inside the multi and the Z of the stair piece on each
side, so "rises toward" is the side whose neighbour stands 5 higher. Prints a summary per stair ID.

    set PYTHONPATH=scripts & set MAPBUILD_CLIENT=D:\\UO\\tool-trials\\client-data-copy
    python -P notes/cc-P734-tools/stair_survey.py
"""
import collections
import os
import struct
import zlib

from mapbuild import uofiles

CLIENT = os.environ.get('MAPBUILD_CLIENT', r'D:\UO\tool-trials\client-data-copy')
land, items = uofiles.read_tiledata(CLIENT)
ver, ents, data, _ = uofiles.uop_by_name(os.path.join(CLIENT, 'MultiCollection.uop'), 'multicollection', '.bin', 0x2000, 6)


def comps(mid):
    e = ents[mid] if not isinstance(ents, dict) else ents.get(mid)
    if not e:
        return []
    d = data[e['off'] + e['hl']:e['off'] + e['hl'] + e['cl']]
    if e['flag'] == 1:
        d = zlib.decompress(d)
    c = struct.unpack_from('<I', d, 4)[0]
    p = 8
    out = []
    for _ in range(c):
        tid, x, y, z, fl = struct.unpack_from('<HhhhH', d, p)
        p += 10
        n = struct.unpack_from('<I', d, p)[0]
        p += 4 + 4 * n
        out.append((x, y, z, tid))
    return out


def name(t):
    return items[t]['name']


def main():
    rises = collections.defaultdict(collections.Counter)
    where = collections.defaultdict(collections.Counter)
    DIRS = {'north': (0, -1), 'south': (0, 1), 'west': (-1, 0), 'east': (1, 0)}
    for mid in range(0x60, 0xA0):
        try:
            cs = comps(mid)
        except Exception:
            continue
        if not cs:
            continue
        stairs = {}
        for x, y, z, t in cs:
            if 'stairs' in name(t):
                stairs.setdefault((x, y), []).append((z, t))
        for (x, y), lst in stairs.items():
            for z, t in lst:
                for dn, (dx, dy) in DIRS.items():
                    for z2, t2 in stairs.get((x + dx, y + dy), []):
                        if z2 == z + 5:
                            rises[t][dn] += 1
        # walls: which corner of the building's wall box each corner/post piece takes
        walls = [(x, y, z, t) for x, y, z, t in cs if items[t]['height'] >= 20 and ('wall' in name(t) or 'post' in name(t))]
        if walls:
            z0 = min(w[2] for w in walls)
            base = [w for w in walls if w[2] == z0]
            xs = [w[0] for w in base]
            ys = [w[1] for w in base]
            for x, y, z, t in base:
                if x == min(xs) and y == min(ys):
                    where[t]['NW'] += 1
                if x == max(xs) and y == max(ys):
                    where[t]['SE'] += 1
                if x == max(xs) and y == min(ys):
                    where[t]['NE'] += 1
                if x == min(xs) and y == max(ys):
                    where[t]['SW'] += 1

    print('Stair pieces: the side toward which the next piece stands 5 higher (count of tiles)')
    for t in sorted(rises):
        print('  0x%04X %-14s h%-2d rises %s' % (t, name(t), items[t]['height'], dict(rises[t])))
    print('Wall pieces at the corners of each house multi\'s lowest wall course (count of multis)')
    for t in sorted(where):
        print('  0x%04X %-14s %s' % (t, name(t), dict(where[t])))


if __name__ == '__main__':
    main()
