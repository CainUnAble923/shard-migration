"""cc-P691: copy EA's Blackthorn dungeon from stock Trammel into site A, in two pieces (Chase, 2026-10-30: "All of
it, two offsets"), and remake trammel.mapops on the SoS base.

    python -P build_fold.py <work folder> [--ship]

  <work folder>  gets sos/ (pristine SoS facet 1, hash-checked), edited/ (sos + today's patch + Blackthorn),
                 trammel.mapops (the new patch) and pieces.json (the two pieces, their offsets and boxes).
  --ship         writes the new patch over the code copy's player-package/vendor/shattered-legacy-map/trammel.mapops.

The source is one connected piece on stock Trammel (x 6177-6490, y 2315-2803, joined within 3 tiles; occ.py), cut in
two along the invasion block's south edge (y 2587/2588), where the cave of the invasion block meets the dungeon's
north corridor (x 6355-6371):
  north     the invasion block: x 6248-6490, y 2315-2587 (the eight town rooms round the central cave)
  dungeon   the rest of the piece: the dungeon proper, its north corridor from y 2588 and the north-west cave
The filler block at 6176-6303, 2752-2847 (land 0x0245 only, no statics) is a separate piece and is not copied.
Both offsets are multiples of 8, so every source block lands on one destination block with its cells in place.
"""
import collections, json, os, shutil, struct, sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(DOCS, 'scripts'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P675-tools'))
from mapbuild import mapops, uofiles  # noqa: E402
import rebase  # noqa: E402  (pristine(), SHIPPED)
import numpy as np  # noqa: E402

STOCK = r"D:/UO/UltimaOnlineVanilla"
FACET, BH = 1, 512
SRC = (6150, 2300, 6500, 2860)            # search box on stock Trammel
NORTH_BOX = (6248, 2315, 6490, 2587)      # the invasion block, inclusive
OFFSETS = {'dungeon': (40, 1248), 'north': (656, 1480)}
SITE_A = (6160, 3744, 7167, 4095)         # the Fold's empty room (FoldMirrorRegion.Area)
ISLE = (6594, 3905, 6865, 4049)           # the isle's drawn box with its sea (P673 1.3)
MARGIN = 24


def pieces():
    """{name: set of (x, y)} on stock Trammel: the connected piece split at the invasion block's south edge."""
    ids, zs = uofiles.load_land(STOCK, FACET)
    x1, y1, x2, y2 = SRC
    occ = ids[x1:x2 + 1, y1:y2 + 1] != uofiles.VOID
    st = uofiles.statics_in(STOCK, FACET, x1, y1, x2, y2)
    for s in st:
        occ[s[0] - x1, s[1] - y1] = True
    W, H = occ.shape
    seen = np.zeros_like(occ, bool)
    comps = []
    for sx, sy in zip(*np.nonzero(occ)):
        if seen[sx, sy]:
            continue
        q, cells = deque([(sx, sy)]), []
        seen[sx, sy] = True
        while q:
            x, y = q.popleft()
            cells.append((x + x1, y + y1))
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    a, b = x + dx, y + dy
                    if 0 <= a < W and 0 <= b < H and occ[a, b] and not seen[a, b]:
                        seen[a, b] = True
                        q.append((a, b))
        comps.append(cells)
    main = max(comps, key=len)
    xs, ys = [c[0] for c in main], [c[1] for c in main]
    assert (min(xs), max(xs), min(ys), max(ys)) == (6177, 6490, 2315, 2803), (min(xs), max(xs), min(ys), max(ys))
    nx1, ny1, nx2, ny2 = NORTH_BOX
    north = {c for c in main if nx1 <= c[0] <= nx2 and ny1 <= c[1] <= ny2}
    dungeon = set(main) - north
    # the block is solid but for its ragged south rows (2586-2587: 389 void cells round the corridor mouth)
    assert len(north) >= 0.99 * (nx2 - nx1 + 1) * (ny2 - ny1 + 1), len(north)
    # where the two pieces touch (8-neighbours): only the corridor mouth on rows 2587/2588
    touch = {(x, y) for (x, y) in dungeon for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (x + dx, y + dy) in north}
    assert all(y == 2588 and 6350 <= x <= 6372 for x, y in touch), sorted(touch)
    return {'north': north, 'dungeon': dungeon}, ids, zs, st


def bbox(cells):
    xs, ys = [c[0] for c in cells], [c[1] for c in cells]
    return int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))


def main():
    work = sys.argv[1]
    sos = rebase.pristine(work)
    shipped = open(rebase.SHIPPED).read()
    edited = os.path.join(work, 'edited')
    d0, m0 = mapops.apply(shipped, sos, edited, FACET)
    print("today's patch on SoS: drifted", len(d0), 'missing', len(m0))
    assert not d0 and not m0

    parts, sids, szs, sst = pieces()
    cur_ids, cur_zs = uofiles.load_land(edited, FACET)
    cidx, csta = uofiles.load_statics_index(edited, FACET)
    sidx, ssta = uofiles.load_statics_index(STOCK, FACET)
    report = {}
    land = {}
    new_blocks = {}
    for name, cells in parts.items():
        dx, dy = OFFSETS[name]
        assert dx % 8 == 0 and dy % 8 == 0
        sb = bbox(cells)
        db = (sb[0] + dx, sb[1] + dy, sb[2] + dx, sb[3] + dy)
        # inside site A, clear of the isle by the margin
        assert SITE_A[0] <= db[0] and db[2] <= SITE_A[2] and SITE_A[1] <= db[1] and db[3] <= SITE_A[3], db
        gap = max(ISLE[0] - db[2], db[0] - ISLE[2], ISLE[1] - db[3], db[1] - ISLE[3])
        assert gap >= MARGIN, (name, gap)
        # the destination, with a block of margin all round, is empty on the SoS + patch file
        ex = (db[0] - 8, db[1] - 8, db[2] + 8, db[3] + 8)
        sub = cur_ids[ex[0]:ex[2] + 1, ex[1]:ex[3] + 1]
        assert (sub == uofiles.VOID).all(), (name, 'land not void', collections.Counter(sub.flatten().tolist()).most_common(3))
        for bx in range(ex[0] >> 3, (ex[2] >> 3) + 1):
            for by in range(ex[1] >> 3, (ex[3] >> 3) + 1):
                assert not uofiles.block_statics(cidx, csta, bx * BH + by), (name, 'statics in', bx, by)
        # land: every cell of the piece, as it is on stock
        for (x, y) in cells:
            land[(x + dx, y + dy)] = (int(sids[x, y]), int(szs[x, y]))
        # statics: per source block, the rows on the piece's cells, order and hue kept
        nst = 0
        for b in sorted({(x >> 3) * BH + (y >> 3) for (x, y) in cells}):
            bx, by = divmod(b, BH)
            rows = [r for r in uofiles.block_statics(sidx, ssta, b) if (bx * 8 + r[1], by * 8 + r[2]) in cells]
            if rows:
                nb = (bx + dx // 8) * BH + (by + dy // 8)
                assert nb not in new_blocks
                new_blocks[nb] = rows
                nst += len(rows)
        report[name] = {'offset': [dx, dy], 'source': sb, 'dest': db, 'land_cells': len(cells), 'statics': nst,
                        'isle_gap': int(gap)}
        print(name, report[name])

    uofiles.write_land(edited, FACET, land)
    idx_path, sta_path = os.path.join(edited, 'staidx1.mul'), os.path.join(edited, 'statics1.mul')
    idx = bytearray(open(idx_path, 'rb').read())
    sta = bytearray(open(sta_path, 'rb').read())
    for b, rows in sorted(new_blocks.items()):
        look, ln, extra = struct.unpack_from('<iii', idx, b * 12)
        assert look < 0 or ln <= 0, b
        newlook = len(sta)
        for r in rows:
            sta += struct.pack('<HBBbh', *r)
        struct.pack_into('<iii', idx, b * 12, newlook, len(rows) * 7, extra)
    open(idx_path, 'wb').write(idx)
    open(sta_path, 'wb').write(sta)

    # re-read with the other reader and compare every cell and static with stock
    mf = uofiles.MapFile(edited, FACET)
    eidx, esta = uofiles.load_statics_index(edited, FACET)
    for name, cells in parts.items():
        dx, dy = OFFSETS[name]
        bad = sum(1 for (x, y) in cells if mf.get(x + dx, y + dy) != (int(sids[x, y]), int(szs[x, y])))
        want = collections.Counter((s[0] + dx, s[1] + dy, s[2], s[3]) for s in sst if (s[0], s[1]) in cells)
        db = report[name]['dest']
        have = collections.Counter(uofiles.statics_in(edited, FACET, *db))
        print(name, 'reread: land mismatches', bad, 'statics equal', want == have, sum(have.values()))
        assert bad == 0 and want == have

    new = mapops.diff(sos, edited, FACET)
    out = os.path.join(work, 'trammel.mapops')
    open(out, 'w', newline='\n').write(new)
    drifted, missing, land_equal, badb = mapops.check(new, sos, edited, FACET, scratch=os.path.join(work, 'check'))
    print('check: drifted', len(drifted), 'missing', len(missing), 'land identical', land_equal, 'blocks differing', len(badb))
    assert (drifted, missing, land_equal, badb) == ([], [], True, [])

    def ops(text):
        return {l for l in text.splitlines() if l[:1] in ('L', 'S')}
    old_ops, new_ops = ops(shipped), ops(new)
    gone = old_ops - new_ops
    extra = new_ops - old_ops
    outside = [l for l in extra if not any(
        report[n]['dest'][0] <= int(l.split()[1]) <= report[n]['dest'][2] and
        report[n]['dest'][1] <= int(l.split()[2]) <= report[n]['dest'][3] for n in report)]
    print('old ops kept', len(old_ops) - len(gone), 'of', len(old_ops), '; new', len(extra), '; new outside the boxes', len(outside))
    assert not gone and not outside
    report['patch_bytes'] = {'before': len(shipped.encode()), 'after': len(new.encode())}
    print('patch bytes', report['patch_bytes'])
    json.dump(report, open(os.path.join(work, 'pieces.json'), 'w'), indent=1)
    if '--ship' in sys.argv:
        shutil.copyfile(out, rebase.SHIPPED)
        print('shipped ->', rebase.SHIPPED)


if __name__ == '__main__':
    main()
