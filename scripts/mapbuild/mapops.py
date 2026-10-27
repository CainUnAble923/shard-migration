"""cc-P188: map ops, the shard's map patch format (designed and measured in cc-P40 section B.2). A patch holds only
what we changed, one line per changed land cell and per static added or removed, so the player package never
carries a byte of EA's map:

    # comment
    F <facet> <touched block count>
    B <block> <fingerprint>          sha256[:16] of EA's land (192 bytes) + statics rows of that block when the
                                     patch was made; the applier reports a block EA changed since, and applies anyway
    L x y tile z                     the land cell becomes tile at z
    S+ x y z id hue                  add one static
    S- x y z id hue                  remove one EA static (matched exactly; if EA moved it, the applier says so)

Two uses, both here so one implementation makes and checks the patch:
    diff(base, edited, facet) -> ops text        from the pristine client folder and the scratch build
    apply(ops_text, base, out, facet)            copies the facet's three files from base to out and applies the ops
    check(ops_text, base, edited, facet)         apply to a scratch copy and compare with the edited files block by block

player-package/payload/app/Apply-MapOps.ps1 is the player-side applier (PowerShell 5.1, no inline C#); the shard's test
suite (shard-migration tools/tests/test_mapops.py) runs both on the same files and compares the output byte for byte.

    python -P mapops.py diff <base folder> <edited folder> <facet> <out .mapops>
    python -P mapops.py apply <ops> <base folder> <out folder> <facet>
    python -P mapops.py check <ops> <base folder> <edited folder> <facet>
    python -P mapops.py pack <map MUL> <out .uop> <facet>          cc-P674: a whole map (the SoS Map1.mul) as a UOP
    python -P mapops.py rename <in .uop> <out .uop> <from> <to>     cc-P674: the same UOP under another facet's names
"""
import collections, hashlib, os, shutil, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from mapbuild import uofiles  # noqa: E402

BLOCK_BYTES = 196


def _files(fi):
    return 'map%dLegacyMUL.uop' % fi, 'statics%d.mul' % fi, 'staidx%d.mul' % fi


def _block_rows(idx, sta, b):
    if b * 12 + 12 > len(idx):
        return []       # EA's last map chunk runs past the facet's last index row
    look, ln = struct.unpack_from('<ii', idx, b * 12)
    if look < 0 or ln <= 0:
        return []
    return [struct.unpack_from('<HBBbh', sta, p) for p in range(look, look + (ln // 7) * 7, 7)]


def fingerprint(land192, rows):
    return hashlib.sha256(bytes(land192) + b''.join(struct.pack('<HBBbh', *r) for r in rows)).hexdigest()[:16]


def diff(base, edited, fi):
    """The ops text for everything edited changed against base on facet fi."""
    mb, me = uofiles.MapFile(base, fi), uofiles.MapFile(edited, fi)
    bh = mb.bh
    ib, sb = _read(base, fi)
    ie, se = _read(edited, fi)
    lines, touched = [], {}
    for b in blocks_present(mb):
        ob, oe = mb.block_offset(b), me.block_offset(b)
        rb, re_ = mb.data[ob + 4:ob + BLOCK_BYTES], me.data[oe + 4:oe + BLOCK_BYTES]
        bx, by = divmod(b, bh)
        if rb != re_:
            touched[b] = True
            for i in range(64):
                if rb[i * 3:i * 3 + 3] != re_[i * 3:i * 3 + 3]:
                    t, z = struct.unpack_from('<Hb', re_, i * 3)
                    lines.append(('L', bx * 8 + i % 8, by * 8 + i // 8, t, z))
        rowsb, rowse = _block_rows(ib, sb, b), _block_rows(ie, se, b)
        if rowsb != rowse:
            touched[b] = True
            cb, ce = collections.Counter(rowsb), collections.Counter(rowse)
            for r, k in (cb - ce).items():
                lines += [('S-', bx * 8 + r[1], by * 8 + r[2], r[3], r[0], r[4])] * k
            for r, k in (ce - cb).items():
                lines += [('S+', bx * 8 + r[1], by * 8 + r[2], r[3], r[0], r[4])] * k
    fps = []
    for b in sorted(touched):
        ob = mb.block_offset(b)
        fps.append((b, fingerprint(mb.data[ob + 4:ob + BLOCK_BYTES], _block_rows(ib, sb, b))))
    order = {'L': 0, 'S-': 1, 'S+': 2}
    lines.sort(key=lambda l: (order[l[0]], l[1], l[2], l[3:]))
    out = ['# Shattered Legacy map patch, facet %d. Ours only: every line is a change we made (scripts/mapbuild/mapops.py).' % fi,
           '# L x y tile z  |  S+ x y z id hue (add)  |  S- x y z id hue (remove one EA static)  |  B block fingerprint',
           'F %d %d' % (fi, len(fps))]
    out += ['B %d %s' % fp for fp in fps]
    out += [' '.join(str(v) for v in l) for l in lines]
    return '\n'.join(out) + '\n'


def blocks_present(mf):
    """The block ids a map file holds (EA's Trammel: all 458,752; a synthetic test facet: one chunk of 4,096)."""
    out = []
    for s, e, fo in mf.starts:
        out += range(s // BLOCK_BYTES, e // BLOCK_BYTES)
    return out


def write_map_uop(path, fi, land, table_size=100):
    """cc-P674: write <land> (raw 196-byte blocks, a map MUL's bytes) as facet fi's UOP the way the client and the
    server read it: entries build/map<fi>legacymul/<chunk, 8 digits>.dat of 4,096 blocks each (the last may be
    shorter), uncompressed, found by the Jenkins hash of that name, in tables of at most <table_size> entries (EA uses
    100) chained by their next pointers, all tables first and the data after them. Returns the entry count."""
    per = 4096 * BLOCK_BYTES
    assert len(land) % BLOCK_BYTES == 0, 'not a whole number of map blocks'
    bodies = [land[o:o + per] for o in range(0, len(land), per)]
    groups = [bodies[g:g + table_size] for g in range(0, len(bodies), table_size)]
    table_pos = 28
    data_pos = table_pos + sum(12 + 34 * len(g) for g in groups)
    out = bytearray(struct.pack('<IiIqii', 0x50594D, 5, 0xFD23EC43, table_pos, table_size, len(bodies)))  # 28-byte header
    off, pos, c = data_pos, table_pos, 0
    for gi, g in enumerate(groups):
        pos += 12 + 34 * len(g)
        out += struct.pack('<iq', len(g), pos if gi + 1 < len(groups) else 0)
        for body in g:
            name = 'build/map%dlegacymul/%08d.dat' % (fi, c)
            out += struct.pack('<qiiiQIh', off, 0, len(body), len(body), uofiles.hashlittle2(name), 0, 0)
            off += len(body)
            c += 1
    assert len(out) == data_pos
    with open(path, 'wb') as f:
        f.write(out)
        for body in bodies:
            f.write(body)
    return len(bodies)


def pack(mul, out, fi):
    """cc-P674: a map MUL (the Siege of Sosaria Map1.mul) packed as facet fi's UOP. -> entries written."""
    return write_map_uop(out, fi, open(mul, 'rb').read())


def rename_uop(src, dst, frm, to):
    """cc-P674: copy facet frm's UOP map as facet to's: same bytes, each entry's name hash rewritten to the to name.
    The Python twin of Apply-MapOps.ps1's Copy-UopRenamed (the launcher's Felucca copy). -> entries renamed."""
    data = bytearray(open(src, 'rb').read())
    names = {uofiles.hashlittle2('build/map%dlegacymul/%08d.dat' % (frm, c)): c for c in range(4096)}
    nxt = struct.unpack_from('<q', data, 12)[0]
    done = 0
    while nxt:
        cnt, nxt2 = struct.unpack_from('<iq', data, nxt)
        for i in range(cnt):
            p = nxt + 12 + 34 * i
            if struct.unpack_from('<q', data, p)[0] == 0:
                continue
            h = struct.unpack_from('<Q', data, p + 20)[0]
            if h not in names:
                raise ValueError('%s holds an entry that is not a map%d chunk' % (src, frm))
            struct.pack_into('<Q', data, p + 20, uofiles.hashlittle2('build/map%dlegacymul/%08d.dat' % (to, names[h])))
            done += 1
        nxt = nxt2
    open(dst, 'wb').write(data)
    return done


def synthetic_facet(folder, fi, chunks=1, fill=(0x0003, 0)):
    """Test support: write a facet's three files with the real layout but only the first <chunks> map chunks (4,096
    blocks each, so chunk 0 is x 0-63 for every y of facet fi), every cell <fill> and no statics. Returns the folder."""
    m, s, i = _files(fi)
    os.makedirs(folder, exist_ok=True)
    block = struct.pack('<I', 0) + struct.pack('<Hb', *fill) * 64
    write_map_uop(os.path.join(folder, m), fi, block * (4096 * chunks))
    nblocks = 4096 * chunks
    open(os.path.join(folder, i), 'wb').write(struct.pack('<iii', -1, -1, 0) * nblocks)
    open(os.path.join(folder, s), 'wb').write(b'')
    return folder


def _read(folder, fi):
    m, s, i = _files(fi)
    return open(os.path.join(folder, i), 'rb').read(), open(os.path.join(folder, s), 'rb').read()


def parse(text):
    """-> (facet, {block: fingerprint}, [(x, y, tile, z)], {block: [rows to add]}, {block: [rows to remove]})"""
    facet, fps, land, adds, removes = None, {}, [], collections.defaultdict(list), collections.defaultdict(list)
    bh = None
    for line in text.splitlines():
        if not line or line.startswith('#'):
            continue
        p = line.split()
        if p[0] == 'F':
            facet = int(p[1])
            bh = uofiles.FACETS[facet][2] >> 3
        elif p[0] == 'B':
            fps[int(p[1])] = p[2]
        elif p[0] == 'L':
            land.append((int(p[1]), int(p[2]), int(p[3]), int(p[4])))
        elif p[0] in ('S+', 'S-'):
            x, y, z, tid, hue = (int(v) for v in p[1:6])
            (adds if p[0] == 'S+' else removes)[(x >> 3) * bh + (y >> 3)].append((tid, x & 7, y & 7, z, hue))
        else:
            raise ValueError(line)
    return facet, fps, land, adds, removes


def apply(text, base, out, fi=None):
    """Copy base's three files to out and apply the ops. Returns (drifted blocks, removals not found)."""
    facet, fps, land, adds, removes = parse(text)
    fi = facet if fi is None else fi
    assert fi == facet, (fi, facet)
    os.makedirs(out, exist_ok=True)
    for name in _files(fi):
        shutil.copyfile(os.path.join(base, name), os.path.join(out, name))
    mf = uofiles.MapFile(out, fi)
    idx, sta = _read(out, fi)
    drifted = [b for b, h in fps.items() if fingerprint(mf.data[mf.block_offset(b) + 4:mf.block_offset(b) + BLOCK_BYTES], _block_rows(idx, sta, b)) != h]
    uofiles.write_land(out, fi, {(x, y): (t, z) for x, y, t, z in land})
    idx, sta = bytearray(idx), bytearray(sta)
    missing = []
    for b in sorted(set(adds) | set(removes)):
        rows = _block_rows(idx, sta, b)
        for r in removes.get(b, []):
            if r in rows:
                rows.remove(r)
            else:
                missing.append((b, r))
        rows += adds.get(b, [])
        look, ln, extra = struct.unpack_from('<iii', idx, b * 12)
        if rows:
            struct.pack_into('<iii', idx, b * 12, len(sta), len(rows) * 7, extra)
            for r in rows:
                sta += struct.pack('<HBBbh', *r)
        else:
            struct.pack_into('<iii', idx, b * 12, -1, -1, extra)
    m, s, i = _files(fi)
    open(os.path.join(out, i), 'wb').write(idx)
    open(os.path.join(out, s), 'wb').write(sta)
    return drifted, missing


def compare(a, b, fi):
    """Land byte for byte, statics block by block as multisets of rows. -> (land equal, blocks that differ)."""
    ma, mb = uofiles.MapFile(a, fi), uofiles.MapFile(b, fi)
    land_equal = ma.data == mb.data
    ia, sa = _read(a, fi)
    ib, sb = _read(b, fi)
    bad = [bk for bk in blocks_present(ma) if collections.Counter(_block_rows(ia, sa, bk)) != collections.Counter(_block_rows(ib, sb, bk))]
    return land_equal, bad


def check(text, base, edited, fi, scratch=None):
    scratch = scratch or os.path.join(os.environ.get('TEMP', '/tmp'), 'mapops-check')
    drifted, missing = apply(text, base, scratch, fi)
    land_equal, bad = compare(scratch, edited, fi)
    return drifted, missing, land_equal, bad


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'diff':
        text = diff(sys.argv[2], sys.argv[3], int(sys.argv[4]))
        open(sys.argv[5], 'w', newline='\n').write(text)
        c = collections.Counter(l.split()[0] for l in text.splitlines() if l and not l.startswith('#'))
        print('wrote', sys.argv[5], dict(c), len(text), 'bytes')
    elif cmd == 'apply':
        d, m = apply(open(sys.argv[2]).read(), sys.argv[3], sys.argv[4], int(sys.argv[5]))
        print('applied; drifted blocks', len(d), 'removals not found', len(m))
    elif cmd == 'pack':
        n = pack(sys.argv[2], sys.argv[3], int(sys.argv[4]))
        print('packed', sys.argv[2], 'as', sys.argv[3], 'facet', sys.argv[4], n, 'entries')
    elif cmd == 'rename':
        n = rename_uop(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
        print('renamed', n, 'entries')
    elif cmd == 'check':
        d, m, le, bad = check(open(sys.argv[2]).read(), sys.argv[3], sys.argv[4], int(sys.argv[5]))
        print('drifted', len(d), 'missing', len(m), 'land identical', le, 'statics blocks differing', len(bad))
        sys.exit(0 if le and not bad and not d and not m else 1)
