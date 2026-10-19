# dump statics in a rect of a facet as an ASCII grid of wall pieces (one char per tile) plus a per-tile listing.
# usage: python -P dump_walls.py <facet> x1 y1 x2 y2 [--all] [--csv out.csv]
import sys, struct, collections
sys.path.insert(0, r'D:\UO\shard-migration\notes\cc-P36-tools')
import uodata
folder = uodata.NEW
fi = int(sys.argv[1]); x1, y1, x2, y2 = map(int, sys.argv[2:6])
show_all = '--all' in sys.argv
csv_out = sys.argv[sys.argv.index('--csv') + 1] if '--csv' in sys.argv else None
land, items = uodata.read_tiledata(folder)
WALL = 1 << 4
idx, sta = uodata.load_statics_index(folder, fi)
name, w, h = uodata.FACETS[fi]
bh = h >> 3
tiles = collections.defaultdict(list)
for bx in range(x1 >> 3, (x2 >> 3) + 1):
    for by in range(y1 >> 3, (y2 >> 3) + 1):
        for (tid, cx, cy, z, hue) in uodata.block_statics(idx, sta, bx * bh + by):
            x, y = bx * 8 + cx, by * 8 + cy
            if x1 <= x <= x2 and y1 <= y <= y2:
                tiles[(x, y)].append((tid, z))
lm = uodata.load_land(folder, fi) if False else None
# letters per wall id
walls = collections.Counter()
for c, lst in tiles.items():
    for tid, z in lst:
        if items[tid]['flags'] & WALL or show_all:
            walls[tid] += 1
letters = {}
alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
for i, (tid, n) in enumerate(sorted(walls.items(), key=lambda kv: -kv[1])):
    letters[tid] = alpha[i] if i < len(alpha) else '?'
print('%s x %d-%d y %d-%d: %d statics on %d tiles' % (name, x1, x2, y1, y2, sum(len(v) for v in tiles.values()), len(tiles)))
print('legend (wall-flagged pieces unless --all):')
for tid, ch in sorted(letters.items(), key=lambda kv: kv[1]):
    r = items[tid]
    print('  %s = 0x%04X %-20s h=%-2d n=%-4d %s' % (ch, tid, r['name'], r['height'], walls[tid], uodata.flagstr(r['flags'])))
print()
print('     ' + ''.join(str(x % 10) for x in range(x1, x2 + 1)))
for y in range(y1, y2 + 1):
    row = []
    for x in range(x1, x2 + 1):
        chs = [letters[tid] for tid, z in tiles.get((x, y), []) if tid in letters]
        if not chs:
            row.append('.' if (x, y) in tiles else ' ')
        elif len(chs) == 1:
            row.append(chs[0])
        else:
            row.append('*')
    print('%4d ' % y + ''.join(row))
if csv_out:
    with open(csv_out, 'w') as f:
        f.write('x,y,z,id_hex,name,height,flags\n')
        for (x, y) in sorted(tiles):
            for tid, z in tiles[(x, y)]:
                r = items[tid]
                f.write('%d,%d,%d,0x%04X,%s,%d,%s\n' % (x, y, z, tid, r['name'], r['height'], uodata.flagstr(r['flags'])))
