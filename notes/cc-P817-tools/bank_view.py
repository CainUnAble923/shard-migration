"""cc-P817: the Wakening Isle bank as the map holds it: every static in and around it (doubles flagged), and an isorender
with the roof cut away (statics above Z 19 left out), plus optional extra pieces drawn in (server items: the lesson
signpost, the practice bank box, the fountain) so a mockup shows what a player sees.

    python -P bank_view.py <map folder> <out.png> [--list] [--extra x,y,z,0xID ...] [--drop x,y,z,0xID ...]

Run with PYTHONPATH=<shard-migration>/scripts, MAPBUILD_CLIENT and MAPBUILD_ART set (guide section 8)."""
import collections
import sys

from mapbuild import uofiles, isorender

X1, Y1, X2, Y2 = 6754, 3970, 6772, 3988   # the bank, its apron, the fountain's pad and the road round them


def parse(args, flag):
    out = []
    if flag in args:
        i = args.index(flag) + 1
        while i < len(args) and not args[i].startswith('--'):
            x, y, z, t = args[i].split(',')
            out.append((int(x), int(y), int(z), int(t, 16)))
            i += 1
    return out


def main():
    folder, out = sys.argv[1], sys.argv[2]
    extra, drop = parse(sys.argv, '--extra'), parse(sys.argv, '--drop')
    st = uofiles.statics_in(folder, 1, X1, Y1, X2, Y2)
    if '--list' in sys.argv:
        names = uofiles.read_tiledata()
        cells = collections.defaultdict(list)
        for x, y, z, t in st:
            cells[(x, y)].append((z, t))
        for (x, y), items in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            ids = [t for _, t in items]
            dup = [t for t, n in collections.Counter((z, t) for z, t in items).items() if n > 1]
            print('%d,%d: %s%s' % (x, y, ', '.join('0x%04X@%d' % (t, z) for z, t in sorted(items)),
                                   '   DOUBLE ' + str(dup) if dup else ''))
    sc = isorender.Scene.from_map(folder, 1, X1, Y1, X2, Y2)
    keep = []
    for s in sc.statics:
        x, y, z, t = s[0], s[1], s[2], s[3]
        if z > 19 or (x, y, z, t) in drop:
            continue
        keep.append(s)
    for (x, y, z, t) in extra:
        keep.append(tuple([x, y, z, t] + list(sc.statics[0][4:])) if sc.statics and len(sc.statics[0]) > 4 else (x, y, z, t))
    sc.statics = keep
    print(out, isorender.save(isorender.render(sc, X1, Y1, X2, Y2), out))


if __name__ == '__main__':
    main()
