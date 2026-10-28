# cc-P678 read only: the tiles SoS Haven keeps clear on top of P237's and P267's own sources, shared by the
# Halloween (hw_*.py) and community art (art_*.py) checks:
#   stock    placer.stock_tiles(): every pinned spawner (all folders), every pinned Trammel decoration cfg item and
#            every HavenSpots spot; a decoration item alone keeps only its own tile (as P237 and P267 had it)
#   home     every NPC home in out/homes.csv (our seeders' posts in the new town)
#   walk     (a bank's box, given its bankers) soswalk's shortest walk from New Haven's start (3634,2586) and from the
#            docks spot (3650,2653) to each banker, the tiles inside the box and their 8 neighbours: the real way in,
#            open archways included (P267 drew banker paths from door items only, and SoS's Second Bank is entered
#            through an open archway with no door)
#   hatch    the Rootdeep hatch tile in the Second Bank (3619,2620; P678 part 4: the way down and its ladder landing)
# each with its 8 neighbours (an NPC or a spot needs room round it).
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import sosbase as B
import placer

HATCH = (3619, 2620)


def homes():
    return [(int(r['x']), int(r['y']), int(r['z']), r['name'], r['kind']) for r in csv.DictReader(open(os.path.join(HERE, '..', 'out', 'homes.csv')))]


_STOCK = None
def stock():
    global _STOCK
    if _STOCK is None: _STOCK = placer.stock_tiles()
    return _STOCK


_SPOTS = None
def spot(x, y):
    global _SPOTS
    if _SPOTS is None:
        import re
        _SPOTS = {(int(m.group(1)), int(m.group(2))) for m in re.finditer(r'new\((\d{4}), (\d{4}), (-?\d+)\)', open(placer.SPOTS).read())}
    return (x, y) in _SPOTS


def kept_clear():
    """{(x, y): [why]} for every tile SoS Haven keeps clear (the centre tile and its 8 neighbours)."""
    out = {}
    def add(x, y, why):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                out.setdefault((x + dx, y + dy), []).append(why if not (dx or dy) else 'beside ' + why)
    import glob, re
    decor = set()
    for f in glob.glob(placer.PINNED + '/Decoration/Trammel/*.cfg'):
        for line in open(f, errors='replace'):
            m = re.match(r'^\s*(\d+)\s+(\d+)\s+(-?\d+)', line)
            if m: decor.add((int(m.group(1)), int(m.group(2))))
    spawn = {(s[1], s[2]) for s in B.spawns_all()}
    for x, y in stock():
        if (x, y) in decor and (x, y) not in spawn and not spot(x, y):
            out.setdefault((x, y), []).append('stock decoration %d,%d' % (x, y))
        else:
            add(x, y, 'stock %s %d,%d' % ('spawner' if (x, y) in spawn else 'HavenSpots spot', x, y))
    for x, y, z, name, kind in homes(): add(x, y, 'home of %s (%s)' % (name, kind))
    add(HATCH[0], HATCH[1], 'Rootdeep hatch')
    return out


START, DOCK = (3634, 2586), (3650, 2653)
_WALK = None
def walk():
    global _WALK
    if _WALK is None:
        import soswalk
        _WALK = soswalk.Walk((3540, 2440, 3790, 2720))
    return _WALK


def walk_to(bankers, x0, y0, x1, y1):
    out = {}
    w = walk()
    for s in (START, DOCK):
        for b in bankers:
            p = w.path(s, tuple(b)) or []
            for (x, y) in p:
                if x0 <= x <= x1 and y0 <= y <= y1:
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            out.setdefault((x + dx, y + dy), set()).add('walk from %d,%d to the banker at %d,%d' % (s + tuple(b)))
    return out


def protect_sos(P, x0, y0, x1, y1, bankers=()):
    for (x, y), whys in walk_to(bankers, x0, y0, x1, y1).items():
        for wh in sorted(whys): P(x, y, wh)
    for (x, y), whys in kept_clear().items():
        if x0 - 1 <= x <= x1 + 1 and y0 - 1 <= y <= y1 + 1:
            for w in sorted(set(whys)): P(x, y, w)


def spawns_in_all(x0, y0, x1, y1):
    """As sosbase.spawns_in, every folder: [(map, x, y, z, homeRange, names, file)]."""
    return [(m, x, y, z, hr, names, f) for (m, x, y, z, hr, wr, names, f) in B.spawns_all() if x0 <= x <= x1 and y0 <= y <= y1]
