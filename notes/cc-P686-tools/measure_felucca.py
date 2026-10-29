"""cc-P686 (SoS swap S13): how much of each stock Felucca region the SoS land changed, and how it relates to S3's
Trammel work.

Felucca reads Trammel's files since P675 (SosMaps sets its file index to 1), so Felucca stands on the SoS land too.
Its change share is P669's measure (sosdiff.regions), taken against stock FELUCCA: the percent of the 8 x 8 blocks
under a region whose land (id, Z) or statics differ between stock Felucca (map0, the vanilla client) and the SoS land
the server reads (the SoS base with this branch's trammel.mapops, made by docker/uo/Build-MapOverlay.ps1).

    python -P measure_felucca.py <SoS overlay folder>   -> out-felucca-measure.csv

Columns: index in pinned's Felucca list, name, type, parent, rects, blocks, blocksChanged, percentChanged, sameAsTrammel
(the Felucca entry's rects equal pinned Trammel's entry of the same name, or of the same rects when unnamed),
trammelDecision (P676's decision for that Trammel entry, notes/cc-P676-tools/out-decisions.csv).
"""
import collections, csv, json, os, struct, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
REPO = os.path.dirname(NOTES)
sys.path.insert(0, os.path.join(REPO, 'scripts'))
from mapbuild import uofiles  # noqa: E402

PINNED = r'D:/UO/ModernUO-pinned/Distribution/Data/regions.json'
VANILLA = r'D:/UO/UltimaOnlineVanilla'
DECISIONS = os.path.join(NOTES, 'cc-P676-tools', 'out-decisions.csv')
W, H = 7168, 4096
BW, BH = W // 8, H // 8


def static_keys(folder, fi):
    """Every static as one int64 key (block, cell, z, id), as P669's sosdiff.static_keys."""
    idx = np.frombuffer(open(os.path.join(folder, 'staidx%d.mul' % fi), 'rb').read(), dtype='<i4').reshape(-1, 3)[:BW * BH]
    sta = open(os.path.join(folder, 'statics%d.mul' % fi), 'rb').read()
    rec = np.dtype([('id', '<u2'), ('x', 'u1'), ('y', 'u1'), ('z', 'i1'), ('hue', '<u2')])
    keys = []
    for b in np.nonzero((idx[:, 0] >= 0) & (idx[:, 1] > 0))[0]:
        look, ln = int(idx[b, 0]), int(idx[b, 1]) // 7 * 7
        a = np.frombuffer(sta, dtype=rec, count=ln // 7, offset=look)
        cell = a['x'].astype(np.int64) * 8 + a['y'].astype(np.int64)
        keys.append((np.int64(b) << 30) | (cell << 24) | ((a['z'].astype(np.int64) + 128) << 16) | a['id'].astype(np.int64))
    return np.unique(np.concatenate(keys))


def changed_blocks(sos):
    """[bx, by] True where stock Felucca and the SoS land differ (land or statics)."""
    fid, fz = uofiles.load_land(VANILLA, 0)
    sid, sz = uofiles.load_land(sos, 1)
    land = ((fid != sid) | (fz != sz)).reshape(BW, 8, BH, 8).any(axis=(1, 3))
    kf, ks = static_keys(VANILLA, 0), static_keys(sos, 1)
    d = np.concatenate([np.setdiff1d(kf, ks, assume_unique=True), np.setdiff1d(ks, kf, assume_unique=True)])
    st = np.zeros(BW * BH, bool)
    st[np.unique(d >> 30)] = True
    return land | st.reshape(BW, BH)


def rects_of(r):
    return [(a['x1'], a['y1'], a['x2'], a['y2']) for a in r.get('Area', [])]


def share(m, rects):
    tiles = changed = 0
    for (x1, y1, x2, y2) in rects:
        bx1, bx2, by1, by2 = max(0, x1 // 8), min(BW - 1, x2 // 8), max(0, y1 // 8), min(BH - 1, y2 // 8)
        if bx2 < bx1 or by2 < by1:
            continue
        sub = m[bx1:bx2 + 1, by1:by2 + 1]
        tiles += sub.size
        changed += int(sub.sum())
    return tiles, changed, round(100.0 * changed / tiles, 1) if tiles else 0.0


def main():
    sos = sys.argv[1]
    pinned = json.load(open(PINNED, encoding='utf-8'))
    fel = [r for r in pinned if r['Map'] == 'Felucca']
    tram = [r for r in pinned if r['Map'] == 'Trammel']
    dec = list(csv.DictReader(open(DECISIONS, newline='')))
    # P676's log rows are in pinned's Trammel order for the stock entries (one row each, unnamed as "(unnamed)")
    stock_dec = dec[:len(tram)]
    assert all((d['region'] == (t.get('Name') or '(unnamed)')) for d, t in zip(stock_dec, tram)), 'decision order'
    m = changed_blocks(sos)
    rows = []
    for i, r in enumerate(fel):
        name = r.get('Name')
        if name:
            js = [j for j, t in enumerate(tram) if t.get('Name') == name]
        else:
            js = [j for j, t in enumerate(tram) if not t.get('Name') and rects_of(t) == rects_of(r)]
        same = bool(js) and rects_of(tram[js[0]]) == rects_of(r)
        tiles, ch, pct = share(m, rects_of(r))
        p = r.get('Parent')
        rows.append([i, name or '(unnamed)', r.get('$type'), p['Name'] if isinstance(p, dict) else '',
                     len(rects_of(r)), tiles, ch, pct, same, stock_dec[js[0]]['decision'] if js else ''])
    out = os.path.join(HERE, 'out-felucca-measure.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['index', 'name', 'type', 'parent', 'rects', 'blocks', 'blocksChanged', 'percentChanged',
                    'sameAsTrammel', 'trammelDecision'])
        w.writerows(rows)
    print('Felucca regions', len(rows), 'rects', sum(r[4] for r in rows))
    print('changed 75+', sum(1 for r in rows if r[7] >= 75), '25-75', sum(1 for r in rows if 25 <= r[7] < 75),
          'under 25', sum(1 for r in rows if r[7] < 25))
    print('same rects as Trammel', sum(1 for r in rows if r[8]), 'by Trammel decision',
          dict(collections.Counter(r[9] for r in rows)))
    print('blocks changed, stock Felucca vs SoS:', int(m.sum()))


if __name__ == '__main__':
    main()
