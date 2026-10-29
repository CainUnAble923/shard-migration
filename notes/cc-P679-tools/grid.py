"""cc-P679: a top-down grid of the SoS land round a spot, to pick a gate or teleporter tile.

    python -P grid.py <overlay> x y [radius]

Each tile: '.' a person stands there (spots.Land.check) with no static on it, ',' stands there on or among small statics,
'o' blocked by a rock or boulder, 'T' a tree, '#' blocked by something else, '~' water, ' ' void, '^' land impassable,
'"' ignored land (a cave mouth's no-draw tile) with no static floor.
The centre tile is bracketed. Below: each open tile's standing Zs for the 7 x 7 round the centre.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sosland  # noqa: E402


def glyph(L, x, y):
    v = L.check(x, y, None)
    tops, sts, why = L.surfaces(x, y)
    if v == 'ok':
        return ',' if sts else '.'
    if v == 'water':
        return '~'
    if v == 'void':
        return ' '
    if v == 'land ignored':
        return '"'
    if v.startswith('land imp'):
        return '^'
    n = v.lower()
    if 'rock' in n or 'boulder' in n or 'stone' in n:
        return 'o'
    if 'tree' in n or 'leaves' in n or 'trunk' in n:
        return 'T'
    return '#'


def main():
    folder, x, y = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    r = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    L = sosland.land(folder)
    print('     ' + ''.join('%-2s' % (str(abs(dx) % 10)) for dx in range(-r, r + 1)))
    for dy in range(-r, r + 1):
        row = ''
        for dx in range(-r, r + 1):
            g = glyph(L, x + dx, y + dy)
            row += ('[' + g) if (dx, dy) == (0, 0) else (g + ']' if (dx, dy) == (1, 0) else ' ' + g)
        print('%5d%s' % (y + dy, row))
    for dy in range(-3, 4):
        print('%5d ' % (y + dy) + ' '.join('%-7s' % ','.join(str(t) for t in L.open_tops(x + dx, y + dy)) for dx in range(-3, 4)))


if __name__ == '__main__':
    main()
