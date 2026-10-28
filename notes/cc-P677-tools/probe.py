"""cc-P677: what the SoS land holds at a spot, for re-placing it.

    python -P probe.py <SoS map folder> x,y[,z] [x,y[,z] ...] [--r 1] [--near 12]

For each spot: the land (id, Z, name) and every static on the (2r+1)^2 tiles round it (x, y, z, height, id, name,
flags), spots.check's verdict, and the open standing spots within --near tiles, nearest first (x, y, standing Z).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import spots  # noqa: E402
from mapbuild import uofiles  # noqa: E402


def main():
    folder = sys.argv[1]
    args = sys.argv[2:]
    r = int(args[args.index('--r') + 1]) if '--r' in args else 1
    near = int(args[args.index('--near') + 1]) if '--near' in args else 12
    pts = [a for a in args if ',' in a]
    land = spots.Land(folder)
    for p in pts:
        v = [int(t) for t in p.split(',')]
        x, y, z = v[0], v[1], (v[2] if len(v) > 2 else None)
        lid = int(land.ids[x, y])
        print('== %d,%d,%s  verdict: %s' % (x, y, z, land.check(x, y, z)))
        print('   land 0x%04X z%d %s' % (lid, int(land.zs[x, y]), land.land[lid][2]))
        for s in sorted(uofiles.statics_in(folder, 1, x - r, y - r, x + r, y + r)):
            it = land.items[s[3]]
            print('   %d,%d z%d h%d 0x%04X %-20s flags 0x%X' % (s[0], s[1], s[2], it['height'], s[3], it['name'], it['flags']))
        found = []
        for dx in range(-near, near + 1):
            for dy in range(-near, near + 1):
                tops, sts, why = land.surfaces(x + dx, y + dy)
                for t in tops:
                    if land.check(x + dx, y + dy, t) == 'ok':
                        found.append((abs(dx) + abs(dy), x + dx, y + dy, t))
        found.sort()
        print('   open nearby:', ', '.join('%d,%d,%d' % (a, b, c) for _, a, b, c in found[:12]))


if __name__ == '__main__':
    main()
