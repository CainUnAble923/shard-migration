# cc-P16 Part A 4 (read only). Lists every top-level Trammel item and every mobile in a box around the
# mine camp in a COPY of a ModernUO save (run in a folder holding SerializedTypes.db, Items.idx/.bin,
# Mobiles.idx/.bin). Items are decoded by pinned Item.Serialize (Projects/Server/Items/Item.cs:816-1080,
# SaveFlag :4280-4310). Mobiles by the P15 tool's Mobile.Serialize scan (notes/cc-P15-tools/nh_mobiles.py).
# Then reports which of them stand on a layout component tile or an NPC destination tile.
import json, struct, sys
X0, X1, Y0, Y1 = 3485, 3525, 2735, 2765

def enc(b, p):
    v = 0; sh = 0
    while True:
        x = b[p]; p += 1; v |= (x & 0x7f) << sh; sh += 7
        if x < 0x80: return v, p
def rstr(b, p):
    f = b[p]; p += 1
    if f == 0: return None, p
    n, p = enc(b, p); return b[p:p + n].decode('utf8', 'replace'), p + n
def types():
    b = open('SerializedTypes.db', 'rb').read()
    ver, cnt = struct.unpack_from('<ii', b, 0); p = 8; t = {}
    for _ in range(cnt):
        h, = struct.unpack_from('<Q', b, p); p += 8
        n, p = enc(b, p); t[h] = b[p:p + n].decode(); p += n
    return t
T = types()
def idx(name):
    b = open(name + '.idx', 'rb').read(); ver, cnt = struct.unpack_from('<ii', b, 0); p = 8; out = []
    for _ in range(cnt):
        p += 1; h, = struct.unpack_from('<Q', b, p); p += 8
        s, c, pos, ln = struct.unpack_from('<IqqI', b, p); p += 24
        out.append((T.get(h, hex(h)), s, pos, ln))
    return out

def item(blob):
    p = 0
    ver, flags = struct.unpack_from('<ii', blob, p); p = 8
    _, p = enc(blob, p)                       # last moved minutes
    if flags & 0x1: p += 1                    # direction
    if flags & 0x2:
        return None                           # bounce info: not decoded (reported as undecoded)
    if flags & 0x4: p += 1                    # loot type
    x = y = z = 0
    if flags & 0x8:
        x, p = enc(blob, p); y, p = enc(blob, p); z, p = enc(blob, p)
    else:
        if flags & 0x80000: x, y = blob[p], blob[p + 1]; p += 2
        elif flags & 0x40000: x, y = struct.unpack_from('<hh', blob, p); p += 4
        if flags & 0x20000: z, = struct.unpack_from('<b', blob, p); p += 1
    iid = 0
    if flags & 0x10: iid, p = enc(blob, p)
    if flags & 0x20: _, p = enc(blob, p)      # hue
    if flags & 0x40: _, p = enc(blob, p)      # amount
    if flags & 0x80: p += 1                   # layer
    name = None
    if flags & 0x100: name, p = rstr(blob, p)
    parent = 0
    if flags & 0x200: parent, = struct.unpack_from('<I', blob, p); p += 4
    if flags & 0x400:
        n, = struct.unpack_from('<i', blob, p); p += 4 + 4 * n
    if flags & 0x1000000: _, p = enc(blob, p)
    elif flags & 0x800: p += 8
    mp = blob[p] if flags & 0x1000 else 0x7F  # Map.Internal index is 0x7F
    return x, y, z, iid, name, parent, mp

if __name__ == '__main__':
    L = json.load(open(r'D:/ShatteredLegacy/design/mine-camp-tents/layout.json'))
    comp = {}
    for a in L['addons']:
        for c in a['components']:
            comp.setdefault((c['x'], c['y']), []).append(f"{a['name']} {c['id']} {c['name']}")
    for n in L['npcs']:
        comp.setdefault(tuple(n['to'][:2]), []).append(f"NPC destination {n['type']}")
    east = {(3498, 2744): 'east of MinersCompactTent opening', (3496, 2754): 'east of SurveyArchivistTent opening'}

    ib = open('Items.bin', 'rb').read(); undecoded = 0; rows = []
    for tname, s, pos, ln in idx('Items'):
        r = item(ib[pos:pos + ln])
        if r is None: undecoded += 1; continue
        x, y, z, iid, name, parent, mp = r
        if mp == 1 and parent == 0 and X0 <= x <= X1 and Y0 <= y <= Y1:
            rows.append((x, y, z, iid, tname.split('.')[-1], name, s))
    print(f'items decoded; bounce-flagged (undecoded) items anywhere: {undecoded}')
    print(f'top-level Trammel items in x {X0}-{X1}, y {Y0}-{Y1}: {len(rows)}')
    for x, y, z, iid, t, name, s in sorted(rows):
        hit = comp.get((x, y)) or ([east[(x, y)]] if (x, y) in east else None)
        print(f'  {x},{y},{z} 0x{iid:04X} {t} {name or ""} serial 0x{s:X}' + (f'   <-- ON {hit}' if hit else ''))

    mb = open('Mobiles.bin', 'rb').read(); mrows = []
    for tname, s, pos, ln in idx('Mobiles'):
        blob = mb[pos:pos + ln]
        for q in range(0, min(len(blob) - 20, 400)):
            x, y, z = struct.unpack_from('<iii', blob, q)
            if not (X0 <= x <= X1 and Y0 <= y <= Y1 and -128 <= z <= 127): continue
            try:
                body, = struct.unpack_from('<i', blob, q + 12)
                name, r = rstr(blob, q + 16)
                gt, r = rstr(blob, r); r += 1 + 4 + 16
                lang, r = rstr(blob, r); r += 3 + 1 + 4 + 24
                mp = blob[r]
                if 0 < body < 0x10000 and mp == 1:
                    mrows.append((x, y, z, tname.split('.')[-1], name, s)); break
            except Exception:
                pass
    print(f'Trammel mobiles in the box: {len(mrows)}')
    for x, y, z, t, name, s in sorted(mrows):
        hit = comp.get((x, y)) or ([east[(x, y)]] if (x, y) in east else None)
        print(f'  {x},{y},{z} {t} {name or ""} serial 0x{s:X}' + (f'   <-- ON {hit}' if hit else ''))
