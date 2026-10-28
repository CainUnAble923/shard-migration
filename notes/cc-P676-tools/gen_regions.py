"""cc-P676 (SoS swap S3): Trammel's regions on the Siege of Sosaria land.

Writes the whole Trammel part of the server's regions as ModernUO JSON (the format of pinned
Distribution/Data/regions.json), which the server loads in place of pinned's Trammel regions
(server/patches/RegionJsonSerializer-shard-maps.patch).

    python -P gen_regions.py <SoS map folder> <code copy> [--check-only]

<SoS map folder> holds map1LegacyMUL.uop, statics1.mul and staidx1.mul: the SoS base with today's trammel.mapops
(notes/cc-P675-tools/rebase.py writes one). Inputs, all read only:
  pinned regions.json (Trammel's 145)          D:/UO/ModernUO-pinned/Distribution/Data/regions.json
  P669's change share per stock region          notes/cc-P669-tools/out/stock-regions.csv (same order as pinned)
  the author's Regions.xml (facet "Trammel")    D:/UO/third-party/sos-trammel-map/.../Data/Regions.xml
  P669's islands                                notes/cc-P669-tools/out/new-islands.csv
  the author's dock spots                       notes/sos-map-author-spots.md

The rules (notes/cc-P676-*.md says why):
  1. A stock region whose area changed under 25 percent stays exactly as pinned has it.
  2. One changed 25 percent or more, that the author drew under the same name (the article and apostrophes aside),
     takes his rectangles and keeps everything else of pinned's (type, priority, music, rune name, entrance, children
     that still fit). Its go location is his, else pinned's if it is still inside, else the middle of its largest rect.
  3. One changed that the author did not draw keeps only its rectangles whose own area changed under 25 percent;
     with none left it is dropped. New Haven, Haven Island and old Haven with every shop in them stay for S7 (P673),
     which moves New Haven into the author's Haven.
  4. The author's regions with no stock match are added: his 7 new towns guarded (TownRegion), his keeps and other
     towns unguarded with no housing, his dungeons DungeonRegion, his named wild areas BaseRegion.
  5. Wild regions for the new islands P669 found that no other region covers, drawn over their dry 8 x 8 blocks.
  6. Dock regions (no housing) round each of his town docks, drawn over the dock's planks.
  7. A no-housing region over each unfinished area on S14's list (P673 section 2).
"""
import collections, csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
REPO = os.path.dirname(NOTES)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, os.path.join(NOTES, 'cc-P481-tools'))
import numpy as np  # noqa: E402
import authorregions  # noqa: E402
import islands  # noqa: E402
from mapbuild import uofiles  # noqa: E402

PINNED = r'D:/UO/ModernUO-pinned/Distribution/Data/regions.json'
AUTHOR = (r'D:/UO/third-party/sos-trammel-map/Siege of Sosaria Trammel Map (3.0)/'
          r'Siege of Sosaria Trammel Map (UNFINISHED)/Data/Regions.xml')
CHANGED = os.path.join(NOTES, 'cc-P669-tools', 'out', 'stock-regions.csv')
ISLANDS = os.path.join(NOTES, 'cc-P669-tools', 'out', 'new-islands.csv')
SPOTS = os.path.join(NOTES, 'sos-map-author-spots.md')
MUSIC = set(open(os.path.join(HERE, 'musicnames.txt')).read().split())
OUT_REL = os.path.join('server', 'data', 'regions-trammel.json')
W, H = 7168, 4096
REDRAW = 25.0

NEW_TOWNS = ['Valunstead', 'Hammerhill', 'Kameron Kove', 'Elmhaven', 'Kettleburg', 'Fort Yondall', 'Elandrim Nur Shaz']
# the stock families S7 moves (P673 section 2, S7): kept as pinned has them here
S7_ROOTS = {'Haven Island', 'Haven'}
# S14's unfinished areas (P673 section 2, S14 item 1), x1, y1, x2, y2 inclusive
UNFINISHED = [('the rooster island', 2840, 1324, 3039, 1523), ('the north-east snow isles', 4224, 256, 4479, 767),
              ('the bare land east of Haven', 3072, 2304, 3199, 2559),
              ('the cells round Echoback and Darkfathom', 4096, 2560, 4223, 2815)]
# the author's region types ModernUO has no class for: their areas are small event spots of a ServUO system
SKIP_TYPES = {'PoisonedTree', 'AcidRiver', 'CrystalField', 'IcyRiver'}


def norm(s):
    s = s.lower().replace("'", '').strip()
    return s[4:] if s.startswith('the ') else s


def area(rects):
    return [{'x1': a, 'y1': b, 'x2': c, 'y2': d} for (a, b, c, d) in rects]


def rects_of(r):
    """Pinned region rects as (x1, y1, x2, y2), end exclusive."""
    return [(a['x1'], a['y1'], a['x2'], a['y2']) for a in r.get('Area', [])]


class Land:
    """The SoS land, light: kind[x, y] (0 dry, 1 water, 2 void) from the land tiles (wet flag; P481's void ids), and
    statics per 8 x 8 block straight from staidx (a block's length / 7). About 100 MB."""

    def __init__(self, folder):
        self.folder = folder
        ids, _ = uofiles.load_land(folder, 1)
        lf = islands.flags()[0]
        wet = (lf[ids.astype(np.int64)] & np.uint64(int(uofiles.WET))) != 0
        self.kind = np.zeros((W, H), dtype=np.uint8)
        self.kind[wet] = 1
        self.kind[np.isin(ids, islands.VOID_IDS)] = 2
        del ids, wet
        k = self.kind.reshape(W // 8, 8, H // 8, 8)
        self.blk_dry = (k == 0).sum(axis=(1, 3))
        idx = np.frombuffer(open(os.path.join(folder, 'staidx1.mul'), 'rb').read(), dtype='<i4').reshape(-1, 3)
        n = idx[:(W // 8) * (H // 8), 1].astype(np.int64)
        n[idx[:(W // 8) * (H // 8), 0] < 0] = 0
        self.blk_statics = (n // 7).reshape(W // 8, H // 8)

    def share(self, rects, what):
        n = hit = 0
        for (x1, y1, x2, y2) in rects:
            sub = self.kind[max(0, x1):min(W, x2), max(0, y1):min(H, y2)]
            n += sub.size
            hit += int((sub == what).sum())
        return hit / n if n else 0.0


class Stock:
    """Stock Trammel (the vanilla client's), read a rect at a time, for the change share of one rect."""

    def __init__(self, sos):
        self.sos = sos
        self.stock = islands.VANILLA

    def changed_share(self, rect):
        """Percent of the 8 x 8 blocks under rect whose land (id, z) or statics differ, P669's measure."""
        x1, y1, x2, y2 = rect
        bx1, by1, bx2, by2 = max(0, x1 // 8), max(0, y1 // 8), min(W // 8 - 1, (x2 - 1) // 8), min(H // 8 - 1, (y2 - 1) // 8)
        if bx2 < bx1 or by2 < by1:
            return 0.0
        X1, Y1, X2, Y2 = bx1 * 8, by1 * 8, bx2 * 8 + 7, by2 * 8 + 7
        a = uofiles.MapFile(self.stock, 1).region(X1, Y1, X2, Y2)
        b = uofiles.MapFile(self.sos, 1).region(X1, Y1, X2, Y2)
        sa = collections.Counter((s[0], s[1], s[2], s[3]) for s in uofiles.statics_in(self.stock, 1, X1, Y1, X2, Y2))
        sb = collections.Counter((s[0], s[1], s[2], s[3]) for s in uofiles.statics_in(self.sos, 1, X1, Y1, X2, Y2))
        diff = {(c[0] // 8, c[1] // 8) for c in set(a) | set(b) if a.get(c) != b.get(c)}
        diff |= {(k[0] // 8, k[1] // 8) for k in set(sa) | set(sb) if sa.get(k) != sb.get(k)}
        total = (bx2 - bx1 + 1) * (by2 - by1 + 1)
        return 100.0 * len(diff) / total


def block_rects(blocks):
    """Greedy cover of a set of 8 x 8 blocks (bx, by) by rectangles of whole blocks: [(x1, y1, x2, y2)] tiles, end
    exclusive."""
    left = set(blocks)
    out = []
    while left:
        bx, by = min(left)
        w = 1
        while (bx + w, by) in left:
            w += 1
        h = 1
        while all((bx + i, by + h) in left for i in range(w)):
            h += 1
        for i in range(w):
            for j in range(h):
                left.discard((bx + i, by + j))
        out.append((bx * 8, by * 8, (bx + w) * 8, (by + h) * 8))
    return out


def dock_spots():
    out, town = [], None
    for line in open(SPOTS, encoding='utf-8'):
        m = re.match(r'### Trammel / Towns / (.+)', line)
        if m:
            town = m.group(1).split(' / ')[0].strip()
        m = re.match(r'- (?:(East|West) )?Docks: (\d+), (\d+), (-?\d+)', line)
        if m and town:
            out.append((town, m.group(1), int(m.group(2)), int(m.group(3))))
    return out


def dock_rect(land, td, sx, sy, r=24):
    """The planks round a dock spot: the 8-connected tiles holding a dock or plank static, from the spot's nearest such
    tile, within r. (x1, y1, x2, y2) end exclusive, or None."""
    names = {}
    x1, y1, x2, y2 = sx - r, sy - r, sx + r, sy + r
    for s in uofiles.statics_in(land.folder, 1, x1, y1, x2, y2):
        nm = (td[s[3]]['name'] or '').lower()
        if 'plank' in nm or 'dock' in nm:
            names[(s[0], s[1])] = nm
    if not names:
        return None
    start = min(names, key=lambda c: abs(c[0] - sx) + abs(c[1] - sy))
    seen, q = {start}, [start]
    while q:
        c = q.pop()
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                n = (c[0] + a, c[1] + b)
                if n in names and n not in seen:
                    seen.add(n)
                    q.append(n)
    xs = [c[0] for c in seen]; ys = [c[1] for c in seen]
    return (min(xs), min(ys), max(xs) + 1, max(ys) + 1), len(seen)


def main():
    folder, code = sys.argv[1], sys.argv[2]
    pinned = json.load(open(PINNED, encoding='utf-8'))
    stock = [r for r in pinned if r['Map'] == 'Trammel']
    rows = list(csv.DictReader(open(CHANGED, newline='')))
    assert len(rows) == len(stock) and all(r['name'] == (s.get('Name') or '') for r, s in zip(rows, stock)), 'P669 csv order'
    pct = [float(r['percentChanged']) for r in rows]
    land = Land(folder)
    cmp = Stock(folder)
    td = uofiles.read_tiledata(uofiles.CLIENT)[1]
    author = [r for r in authorregions.regions(AUTHOR) if r[0] == 'Trammel']
    a_top = {}
    for r in author:
        if not r[3] and r[2]:
            a_top.setdefault(norm(r[2]), r)
    log = []

    def parent_name(r):
        p = r.get('Parent')
        return p['Name'] if isinstance(p, dict) else None

    def family_root(i):
        r = stock[i]
        seen = 0
        while parent_name(r) and seen < 10:
            r = next(s for s in stock if s.get('Name') == parent_name(r))
            seen += 1
        return r.get('Name')

    out = []
    kept_names, dropped = set(), set()
    for i, s in enumerate(stock):
        name = s.get('Name') or '(unnamed)'
        r = json.loads(json.dumps(s))
        pn = parent_name(s)
        if pn in dropped:
            dropped.add(name); log.append(('dropped', name, pct[i], 'its parent was dropped')); continue
        if family_root(i) in S7_ROOTS:
            out.append(r); kept_names.add(name); log.append(('kept for S7', name, pct[i], 'New Haven moves (P673 S7)')); continue
        if pct[i] < REDRAW:
            out.append(r); kept_names.add(name); log.append(('kept', name, pct[i], 'under 25 percent changed')); continue
        a = a_top.get(norm(name)) if s.get('Name') and not pn else None
        if a:
            rects = [(x1, y1, x2 + 1, y2 + 1) for (x1, y1, x2, y2) in a[4] if x2 >= x1]
            r['Area'] = area(rects)
            go = r.get('GoLocation')
            if a[5]:
                r['GoLocation'] = {'x': int(a[5]['x']), 'y': int(a[5]['y']), 'z': int(a[5].get('z', 0))}
            elif go and not any(x1 <= go['x'] < x2 and y1 <= go['y'] < y2 for (x1, y1, x2, y2) in rects):
                big = max(rects, key=lambda q: (q[2] - q[0]) * (q[3] - q[1]))
                r['GoLocation'] = {'x': (big[0] + big[2]) // 2, 'y': (big[1] + big[3]) // 2, 'z': go.get('z', 0)}
            if a[6] and 'Entrance' in r:
                r['Entrance'] = {'x': int(a[6]['x']), 'y': int(a[6]['y']), 'z': int(a[6].get('z', 0))}
            out.append(r); kept_names.add(name)
            log.append(('redrawn from the author', name, pct[i], '%d rects (pinned %d)' % (len(rects), len(rects_of(s)))))
            continue
        keep = [q for q in rects_of(s) if cmp.changed_share(q) < REDRAW]
        if keep:
            r['Area'] = area(keep)
            go = r.get('GoLocation')
            if go and not any(x1 <= go['x'] < x2 and y1 <= go['y'] < y2 for (x1, y1, x2, y2) in keep):
                big = max(keep, key=lambda q: (q[2] - q[0]) * (q[3] - q[1]))
                r['GoLocation'] = {'x': (big[0] + big[2]) // 2, 'y': (big[1] + big[3]) // 2, 'z': go.get('z', 0)}
            out.append(r); kept_names.add(name)
            log.append(('clipped', name, pct[i], '%d of %d rects kept (each under 25 percent changed)' % (len(keep), len(rects_of(s)))))
        else:
            dropped.add(name)
            log.append(('dropped', name, pct[i], 'the land under it changed and the author drew no region of that name'))
    stock_norm = {norm(s.get('Name') or '') for s in stock}

    # 4. the author's regions with no stock match (top level, named)
    taken = {r.get('Name') for r in out}
    for r in author:
        typ, name, parents, rects = r[1], r[2], r[3], [(a, b, c + 1, d + 1) for (a, b, c, d) in r[4] if c >= a]
        if parents or not name or norm(name) in stock_norm or name in taken or typ in SKIP_TYPES or not rects:
            if typ in SKIP_TYPES and not parents:
                log.append(('not added', name, '', 'type %s has no ModernUO class (a ServUO event spot)' % typ))
            continue
        e = {'Map': 'Trammel', 'Name': name, 'Priority': 50, 'Area': area(rects)}
        if typ == 'TownRegion' and name in NEW_TOWNS + ['Lord British Castle']:
            e = {'$type': 'TownRegion', **e}
            why = 'the author\'s town, guarded'
        elif typ == 'TownRegion':
            e = {'$type': 'NoHousingRegion', **e}
            why = 'the author\'s keep or hamlet: no housing, no guards (S10 decides its people)'
        elif typ in ('DungeonRegion', 'MondainRegion'):
            e = {'$type': 'DungeonRegion', **e}
            mus = r[7] if r[7] in MUSIC else 'Dungeon9'
            e['Music'] = mus
            if r[6]:
                e['Entrance'] = {'x': int(r[6]['x']), 'y': int(r[6]['y']), 'z': int(r[6].get('z', 0))}
            why = 'the author\'s dungeon (sealed by S14 until S18 opens it)'
        elif typ == 'NoHousingRegion':
            e = {'$type': 'NoHousingRegion', **e}
            why = 'the author\'s no-housing area'
        elif typ in ('', 'Jail', 'GreenAcres'):
            if typ:
                continue
            e = {'$type': 'BaseRegion', **e, 'Priority': 10}
            why = 'the author\'s named wild area, under the towns'
        else:
            log.append(('not added', name, '', 'type %s not mapped' % typ))
            continue
        if r[5]:
            e['GoLocation'] = {'x': int(r[5]['x']), 'y': int(r[5]['y']), 'z': int(r[5].get('z', 0))}
        else:
            big = max(rects, key=lambda q: (q[2] - q[0]) * (q[3] - q[1]))
            e['GoLocation'] = {'x': (big[0] + big[2]) // 2, 'y': (big[1] + big[3]) // 2, 'z': 0}
        out.append(e); taken.add(name)
        log.append(('added', name, '', why))

    # 6. docks
    town_regions = {r['Name']: r for r in out if r.get('$type') in ('TownRegion',) and 'Parent' not in r}
    for (town, side, x, y) in dock_spots():
        tn = next((n for n in town_regions if norm(n) == norm(town.replace('Buccaneers', "Buccaneer's"))), None)
        d = dock_rect(land, td, x, y)
        if not d:
            log.append(('not added', 'docks of %s' % town, '', 'no plank statics within 24 of %d,%d' % (x, y))); continue
        rect, n = d
        name = 'the %sdocks in %s' % ((side.lower() + ' ') if side else '', town)
        if name in taken:
            continue
        e = {'$type': 'NoHousingRegion', 'Map': 'Trammel', 'Name': name, 'Priority': 50, 'Area': area([rect]),
             'GoLocation': {'x': x, 'y': y, 'z': 0}}
        inside = tn and any(a['x1'] <= rect[0] and rect[2] <= a['x2'] and a['y1'] <= rect[1] and rect[3] <= a['y2']
                            for a in town_regions[tn]['Area'])
        if inside:
            e = {'$type': 'NoHousingRegion', 'Map': 'Trammel', 'Parent': {'Name': tn, 'Map': 'Trammel'},
                 **{k: v for k, v in e.items() if k not in ('$type', 'Map')}}
        out.append(e); taken.add(name)
        log.append(('added', name, '', 'dock, %d plank tiles%s' % (n, ', inside ' + tn if inside else '')))

    # 7. unfinished land
    for (nm, x1, y1, x2, y2) in UNFINISHED:
        name = 'Unfinished land: ' + nm
        out.append({'$type': 'NoHousingRegion', 'Map': 'Trammel', 'Name': name, 'Priority': 20,
                    'Area': area([(x1, y1, x2 + 1, y2 + 1)])})
        log.append(('added', name, '', 'S14\'s list: no housing'))

    # 5. new islands no region covers
    def covered(x1, y1, x2, y2):
        for r in out:
            for a in r['Area']:
                if a['x1'] < x2 and x1 < a['x2'] and a['y1'] < y2 and y1 < a['y2']:
                    return True
        return False
    for row in csv.DictReader(open(ISLANDS, newline='')):
        if row['verdict'] != 'new':
            continue
        x1, y1, x2, y2 = (int(row[k]) for k in ('x1', 'y1', 'x2', 'y2'))
        blocks = [(bx, by) for bx in range(x1 // 8, x2 // 8 + 1) for by in range(y1 // 8, y2 // 8 + 1)
                  if land.blk_dry[bx, by] >= 32]
        rects = [q for q in block_rects(blocks) if not covered(*q)]
        if not rects:
            log.append(('not added', 'isle %s' % row['id'], '', 'covered by another region')); continue
        name = 'an isle at %d,%d' % ((x1 + x2) // 2, (y1 + y2) // 2)
        out.append({'$type': 'BaseRegion', 'Map': 'Trammel', 'Name': name, 'Priority': 10, 'Area': area(rects)})
        log.append(('added', name, '', 'P669 new island %s, %d dry blocks' % (row['id'], len(blocks))))

    # children after their parents (pinned order already is; added ones are top level or name a parent above)
    names = [r.get('Name') for r in out]
    for r in out:
        pn = parent_name(r)
        assert not pn or pn in names[:names.index(r.get('Name'))], ('parent after child', r.get('Name'), pn)
    named = collections.Counter(r.get('Name') for r in out if r.get('Name'))
    assert all(v == 1 for v in named.values()), [k for k, v in named.items() if v > 1]
    path = os.path.join(code, OUT_REL)
    if '--check-only' not in sys.argv:
        text = '[\n' + ',\n'.join('  ' + json.dumps(r, ensure_ascii=True) for r in out) + '\n]\n'
        open(path, 'w', encoding='ascii', newline='\n').write(text)
    with open(os.path.join(HERE, 'out-decisions.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['decision', 'region', 'percentChanged', 'why'])
        w.writerows(log)
    print(collections.Counter(l[0] for l in log))
    print('regions', len(out), 'written to', path)


if __name__ == '__main__':
    main()
