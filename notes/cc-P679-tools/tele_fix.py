"""cc-P679 (SoS swap S4): decide every Trammel and Felucca teleporter of pinned's Data/teleporters.json on the SoS
land, and write our Data/ShatteredLegacy/teleporters-sos.json.

    python -P tele_fix.py <overlay> <code copy> [--write]

Each end on Trammel or Felucca is graded (tele.py's rule: P677's standing rule, and a source must fire):
  ok        it passes on SoS;
  as stock  it fails the same way on EA's own Trammel and SoS left its 3 x 3 alone (stock's quirk, not the swap's). A
            Felucca end counts only when pinned has the very same end on Trammel and it is "as stock" there: Felucca
            reads the SoS Trammel files (P675), so its own EA land (map0, e.g. x 6900 and beyond) is gone;
  broken    anything else.
A broken end is re-placed: first the same x, y at the floor nearest the stock Z; else the nearest open tile within 3,
at the floor nearest the stock Z. A source takes the floor's own Z, so it fires. An entry with an end that cannot be
re-placed, or one DROP names, is dropped with its reason. MOVE overrides the automatic choice for an end.
Writes out-tele-decisions.csv; --write also writes <code copy>/server/data/teleporters-sos.json: every pinned entry with
an end on Trammel or Felucca, as decided, in pinned's order (the patch to GenTeleporter puts it in place of those).
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import changed  # noqa: E402
import tele  # noqa: E402

SOS_MAPS = tele.SOS_MAPS

# Entries dropped by hand, by pinned index (0-based in teleporters.json), with the reason (cc-P679's review).
WATER = ("both ends water on EA's own Trammel too: a Felucca-only stock link (on its own map0, which Felucca no longer "
         "reads since P675); dead on Trammel, and no land for it on SoS")
BUCS = ("Buccaneer's Den: the author kept the Z -20 tunnel but rebuilt the town over it; no floor stands at Z 38-39 "
        "above the tunnel any more, so its ladders have no top end")
BLACKTHORN = ("Blackthorn's entrance: off on this land (P677, BlackthornRegions.OnThisLand); its land end is water and its "
              "dungeon end is the author's Bleak Wind Tunnels, sealed until S18. P691 gives Blackthorn its way in")
HAVEN_CAVE = ("the cave mouth south of the old New Haven plaza is solid rock on SoS (13 x 13 round it); the cave beyond "
              "(5912,355) has no other teleporter")
MAP0 = ("Felucca-only land of EA's map0 (x 6900 and beyond, or a place Felucca drew differently): Felucca reads the SoS "
        "Trammel files since P675, where this end is void, rock or another place")
DROP = {}
for _i in (4, 137, 437, 574, 68, 327, 507, 750):
    DROP[_i] = WATER
for _i in (63, 64, 65, 502, 503, 504):
    DROP[_i] = BUCS
for _i in (456, 457, 458, 459, 460, 828, 829, 830, 831, 832):
    DROP[_i] = BLACKTHORN
DROP[508] = HAVEN_CAVE
for _i in (141, 176, 328, 339, 340, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 1288, 1289, 1290, 1291,
           1362):
    DROP[_i] = MAP0
# (index, 'src'|'dst') -> (x, y, z): a re-placement chosen by hand. The Lost Lands pass at 5126,3143 (to the cave at
# 5850,432 and on to Britain, 1987,2062): the author kept the pass's shape but lowered it from Z ~98 to -5.
MOVE = {}
for _i in (85, 527):
    MOVE[(_i, 'src')] = (5126, 3143, -5)
for _i in (263, 264, 265, 266, 687, 688, 689, 690):
    MOVE[(_i, 'dst')] = (5127, 3143, -5)
# Deceit's mouth (4110-4112, 430) is cave-mouth land pinned ignores, and SoS dropped stock's cave floor (0x53C, Z 5) there,
# so nobody can stand in it: its entrance moves one row out (the automatic choice, 4110-4112, 431, 5) and the way out
# of the dungeon lands one row further (432), off the entrance row.
for _i, _x in ((117, 4110), (118, 4110), (119, 4111), (120, 4112), (555, 4110), (556, 4110), (557, 4111), (558, 4112)):
    MOVE[(_i, 'dst')] = (_x, 432, 5)


def end_verdict(L, which, x, y, z):
    v = L.check(x, y, z)
    if v == 'ok' and which == 'src' and not tele.fires(L, x, y, z):
        v = 'never fires'
    return v


def replace(L, which, x, y, z):
    """(x, y, z, how) or None."""
    tops = L.open_tops(x, y)
    if tops:
        t = min(tops, key=lambda t: abs(t - z))
        if abs(t - z) <= 20:
            return x, y, t, 'z %+d' % (t - z)
    best = None
    for r in (1, 2, 3):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if max(abs(dx), abs(dy)) != r:
                    continue
                for t in L.open_tops(x + dx, y + dy):
                    if abs(t - z) > 20:
                        continue
                    key = (r, abs(t - z), abs(dx) + abs(dy))
                    if best is None or key < best[0]:
                        best = (key, (x + dx, y + dy, t))
        if best:
            nx, ny, t = best[1]
            return nx, ny, t, 'moved %d,%d z %+d' % (nx - x, ny - y, t - z)
    return None


def decide(folder, code):
    both = changed.Both(folder)
    S, K = both.sos, both.stock
    data = json.load(open(os.path.join(tele.PINNED, 'teleporters.json'), encoding='utf-8'))
    out, rows = [], []
    tram_as_stock = set()
    for e in data:
        for which in ('src', 'dst'):
            w = e[which]
            if w['map'] == 'Trammel':
                x, y, z = w['loc']
                v = end_verdict(S, which, x, y, z)
                if v != 'ok' and v == end_verdict(K, which, x, y, z) and not both.changed(x, y):
                    tram_as_stock.add((which, x, y, z))
    for i, e in enumerate(data):
        if e['src']['map'] not in SOS_MAPS and e['dst']['map'] not in SOS_MAPS:
            continue
        e = json.loads(json.dumps(e))
        notes, drop = [], DROP.get(i)
        for which in ('src', 'dst'):
            w = e[which]
            if w['map'] not in SOS_MAPS:
                continue
            x, y, z = w['loc']
            v = end_verdict(S, which, x, y, z)
            status, how = 'ok', ''
            if v != 'ok':
                vs = end_verdict(K, which, x, y, z)
                if vs == v and not both.changed(x, y) and (w['map'] == 'Trammel' or (which, x, y, z) in tram_as_stock):
                    status = 'as stock'
                else:
                    status = 'broken'
            new = None
            if (i, which) in MOVE:
                new = MOVE[(i, which)] + ('by hand',)
            elif status == 'broken' and not drop:
                new = replace(S, which, x, y, z)
                if new is None:
                    drop = 'no open floor within 3 tiles of the %s (%s)' % (which, v)
            if new and not drop:
                w['loc'] = [new[0], new[1], new[2]]
                how = new[3]
                status = 'fixed' if status in ('broken', 'ok') else status
            rows.append(dict(index=i, end=which, map=w['map'], stock='%d,%d,%d' % (x, y, z), verdict=v, status=status,
                             now='%d,%d,%d' % tuple(w['loc']), how=how, changed=both.changed(x, y)))
        if drop:
            for r in rows:
                if r['index'] == i:
                    r['status'], r['how'] = 'dropped', drop
            continue
        out.append(e)
    return out, rows


def main():
    folder, code = sys.argv[1], sys.argv[2]
    out, rows = decide(folder, code)
    with open(os.path.join(HERE, 'out-tele-decisions.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    print('entries kept', len(out), Counter((r['map'], r['status']) for r in rows))
    if '--write' in sys.argv:
        path = os.path.join(code, 'server', 'data', 'teleporters-sos.json')
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('[\n' + ',\n'.join('  ' + json.dumps(e) for e in out) + '\n]\n')
        print('wrote', path)


if __name__ == '__main__':
    main()
