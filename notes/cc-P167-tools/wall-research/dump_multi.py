# dump a house multi from MultiCollection.uop (pinned MultiData.LoadUOP's format) as an ASCII wall grid
import sys, struct, collections, zlib
sys.path.insert(0, r'D:\UO\shard-migration\notes\cc-P36-tools')
import uodata
folder = uodata.NEW
land, items = uodata.read_tiledata(folder)
WALL = 1 << 4
path = folder + r'\MultiCollection.uop'
ver, ents, data, allents = uodata.uop_by_name(path, 'multicollection', '.bin', 0x2000, 6)
def comps(mid):
    e = ents.get(mid)
    if not e: return None
    d = data[e['off'] + e['hl']:e['off'] + e['hl'] + e['cl']]
    if e['flag'] == 1:
        d = zlib.decompress(d)
    count = struct.unpack_from('<I', d, 4)[0]
    p = 8; out = []
    for i in range(count):
        tid, x, y, z, fl = struct.unpack_from('<HhhhH', d, p); p += 10
        n = struct.unpack_from('<I', d, p)[0]; p += 4 + 4 * n
        out.append((tid, x, y, z, fl))
    return out
for a in sys.argv[1:]:
    mid = int(a, 16)
    c = comps(mid)
    if c is None:
        print('multi 0x%04X: none' % mid); continue
    xs = [t[1] for t in c]; ys = [t[2] for t in c]
    x1, x2, y1, y2 = min(xs), max(xs), min(ys), max(ys)
    tiles = collections.defaultdict(list)
    for tid, x, y, z, fl in c:
        tiles[(x, y)].append((tid, z, fl))
    walls = collections.Counter(tid for lst in tiles.values() for tid, z, fl in lst if items[tid]['flags'] & WALL)
    alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letters = {tid: alpha[i] for i, (tid, n) in enumerate(sorted(walls.items(), key=lambda kv: -kv[1]))}
    print('multi 0x%04X: %d components, x %d..%d y %d..%d; z values %s' % (mid, len(c), x1, x2, y1, y2, sorted(set(t[3] for t in c))))
    for tid, ch in sorted(letters.items(), key=lambda kv: kv[1]):
        r = items[tid]; print('  %s = 0x%04X %-16s h=%-2d n=%-3d %s' % (ch, tid, r['name'], r['height'], walls[tid], uodata.flagstr(r['flags'])))
    others = collections.Counter(items[tid]['name'] for lst in tiles.values() for tid, z, fl in lst if not items[tid]['flags'] & WALL)
    print('  other pieces:', dict(others.most_common(8)))
    for zz in sorted(set(t[3] for t in c)):
        if zz > 7: continue
        print('  z=%d:' % zz)
        print('       ' + ''.join('%2d' % x for x in range(x1, x2 + 1)))
        for y in range(y1, y2 + 1):
            row = []
            for x in range(x1, x2 + 1):
                lst = [(tid, fl) for tid, z, fl in tiles.get((x, y), []) if z == zz]
                w = [letters[tid] for tid, fl in lst if tid in letters]
                if w: row.append((' ' + w[0]) if len(w) == 1 else ' *')
                elif lst: row.append(' .')
                else: row.append('  ')
            print('  %4d ' % y + ''.join(row))
    # list wall tiles with ids for z=min
    z0 = min(t[3] for t in c)
    print('  wall pieces at z=%d:' % z0, ' '.join('(%d,%d)=0x%04X' % (x, y, tid) for (x, y), lst in sorted(tiles.items()) for tid, z, fl in lst if z == z0 and items[tid]['flags'] & WALL))
