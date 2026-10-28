"""cc-P675 (SoS swap S2, part 3): re-base trammel.mapops onto the Siege of Sosaria map.

    python -P rebase.py <work folder> [--ship]

  <work folder>  gets sos/ (the pristine SoS facet 1, under the client's names, checked against
                 notes/cc-P675-tools/sos-base/ORIGINAL-SHA256.txt), edited/ (sos + the kept lines) and trammel.mapops.
  --ship         writes the new patch over the code copy's player-package/vendor/shattered-legacy-map/trammel.mapops.

1. measure: today's patch (made against stock Trammel) applied to SoS, drift and misses split by area.
2. keep: every line of the Burrows and the isle as it is; drop the Old Haven way in (its 2 blocks, x 3608-3623,
   y 2616-2623: the author's Haven, S7 makes the new way in) and the tutorial farm's 4 tree removals (the farm is on
   the isle now; on SoS that spot is the author's forest, and an S- there could only miss or take his tree).
3. diff(sos, edited) is the new patch, with every fingerprint SoS's; check must read drifted 0, missing 0, land
   identical, 0 blocks differing.
"""
import collections, hashlib, os, shutil, sys

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(DOCS, 'scripts'))
from mapbuild import mapops  # noqa: E402

SHARD = os.environ.get('SL_SHARD_REPO', r'D:\UO\golems\Iron\ShatteredLegacy')
SHIPPED = os.path.join(SHARD, 'player-package', 'vendor', 'shattered-legacy-map', 'trammel.mapops')
VENDOR = os.path.join(SHARD, 'player-package', 'vendor', 'sos-trammel-map', 'files')
HASHES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sos-base', 'ORIGINAL-SHA256.txt')
FACET, BH = 1, 512
NAMES = ('map1LegacyMUL.uop', 'statics1.mul', 'staidx1.mul')

AREAS = {
    'burrows': (5136, 1128, 5247, 1263),
    'way_in': (3608, 2616, 3623, 2623),     # its 2 blocks, whole
    'farm': (3384, 2600, 3399, 2623),       # its 2 blocks, whole (the fence is 3381-3399, 2603-2619)
    'isle': (6592, 3904, 6871, 4055),       # the isle's blocks, whole
}
DROP = ('way_in', 'farm')


def area(x, y):
    for k, (x0, y0, x1, y1) in AREAS.items():
        if x0 <= x <= x1 and y0 <= y <= y1:
            return k
    return 'other'


def block_area(b):
    return area((b // BH) * 8, (b % BH) * 8)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def pristine(work):
    """sos/ = the shipped base files under the client's names, each at its ORIGINAL-SHA256.txt hash."""
    want = {}
    for line in open(HASHES):
        h, _, name = line.strip().partition(' *')
        if name:
            want[name] = h
    sos = os.path.join(work, 'sos')
    os.makedirs(sos, exist_ok=True)
    for n in NAMES:
        dst = os.path.join(sos, n)
        if not os.path.exists(dst) or sha(dst) != want[n]:
            shutil.copyfile(os.path.join(VENDOR, 'base-' + n.lower()), dst)
        h = sha(dst)
        assert h == want[n], ('not the pristine SoS file', n, h, want[n])
        print('pristine', n, h[:16])
    return sos


def split(text):
    """-> {area: [ops lines]} for the L/S lines, and {area: [B lines]}."""
    ops, fps = collections.defaultdict(list), collections.defaultdict(list)
    for line in text.splitlines():
        p = line.split()
        if not p or p[0].startswith('#') or p[0] == 'F':
            continue
        if p[0] == 'B':
            fps[block_area(int(p[1]))].append(line)
        else:
            ops[area(int(p[1]), int(p[2]))].append(line)
    return ops, fps


def main():
    work = sys.argv[1]
    sos = pristine(work)
    old = open(SHIPPED).read()
    ops, fps = split(old)
    print('today:', {k: (len(v), len(fps[k])) for k, v in ops.items()}, '(lines, blocks)')
    assert set(ops) <= set(AREAS) and set(fps) <= set(AREAS), (sorted(ops), sorted(fps))

    # 1. measure today's patch on SoS
    drifted, missing = mapops.apply(old, sos, os.path.join(work, 'measure'), FACET)
    print('today on SoS: drifted', collections.Counter(block_area(b) for b in drifted),
          'missing', collections.Counter(block_area(b) for b, r in missing))
    for b, r in missing:
        print('  missing', block_area(b), 'S- %d %d %d %d %d' % ((b // BH) * 8 + r[1], (b % BH) * 8 + r[2], r[3], r[0], r[4]))

    # 2. keep the Burrows and the isle
    kept_ops = [l for k in AREAS if k not in DROP for l in ops[k]]
    kept_fps = [l for k in AREAS if k not in DROP for l in fps[k]]
    kept = 'F 1 %d\n' % len(kept_fps) + '\n'.join(kept_fps + kept_ops) + '\n'
    edited = os.path.join(work, 'edited')
    d2, m2 = mapops.apply(kept, sos, edited, FACET)
    print('kept on SoS: drifted', collections.Counter(block_area(b) for b in d2), 'missing', len(m2))
    assert not m2, m2

    # 3. the new patch
    new = mapops.diff(sos, edited, FACET)
    out = os.path.join(work, 'trammel.mapops')
    open(out, 'w', newline='\n').write(new)
    drifted, missing, land_equal, bad = mapops.check(new, sos, edited, FACET, scratch=os.path.join(work, 'check'))
    print('check: drifted', len(drifted), 'missing', len(missing), 'land identical', land_equal, 'blocks differing', len(bad))
    assert (drifted, missing, land_equal, bad) == ([], [], True, [])

    nops, nfps = split(new)
    for k in AREAS:
        same = sorted(nops[k]) == sorted(ops[k]) if k not in DROP else None
        print('%-8s today %6d lines %4d blocks -> new %6d lines %4d blocks; ops lines identical: %s'
              % (k, len(ops[k]), len(fps[k]), len(nops[k]), len(nfps[k]), same))
        if k not in DROP and not same:
            gone, extra = set(ops[k]) - set(nops[k]), set(nops[k]) - set(ops[k])
            print('   gone %d (e.g. %s), new %d (e.g. %s)' % (len(gone), sorted(gone)[:3], len(extra), sorted(extra)[:3]))
    if '--ship' in sys.argv:
        shutil.copyfile(out, SHIPPED)
        print('shipped ->', SHIPPED)


if __name__ == '__main__':
    main()
