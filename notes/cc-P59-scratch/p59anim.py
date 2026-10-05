# P59, read-only: resolve a body ID the way the classic client does and decode its frames.
# Sources, in client order: AnimationFrame*.uop (legacy frames), Bodyconv.def -> anim2..anim6.mul,
# anim.mul, then Body.def fallback (body redrawn as another body with a hue).
# Reuses the UOP hash and AMOU decoder from notes\cc-P49-scratch\uopanim.py.
import struct, os, re, zlib, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cc-P49-scratch'))
from uopanim import hashlittle2, read_uop_index
from PIL import Image

CLIENT = r'D:\UO\UltimaOnlineVanilla'

# Layouts: actions per direction block, and stand/walk action for each anim type.
LAYOUT = {'MONSTER': 22, 'ANIMAL': 13, 'HUMAN': 35}
STAND = {'MONSTER': 1, 'SEA_MONSTER': 1, 'ANIMAL': 2, 'HUMAN': 4, 'EQUIPMENT': 4}
WALK = {'MONSTER': 0, 'SEA_MONSTER': 0, 'ANIMAL': 0, 'HUMAN': 0, 'EQUIPMENT': 0}

def _num(s):
    s = s.strip()
    return int(s, 0) if s else None

def load_mobtypes():
    out = {}
    for ln in open(os.path.join(CLIENT, 'mobtypes.txt'), encoding='latin-1'):
        m = re.match(r'\s*(\d+)\s+([A-Z_]+)\s+([0-9A-Fa-f]+)?\s*(#.*)?', ln)
        if m:
            out[int(m.group(1))] = (m.group(2), (m.group(4) or '').lstrip('#').strip(), int(m.group(3) or '0', 16))
    return out

def load_bodyconv():
    out = {}
    for i, ln in enumerate(open(os.path.join(CLIENT, 'Bodyconv.def'), encoding='latin-1'), 1):
        s = ln.split('#')[0].strip().strip('"')
        if not s: continue
        parts = s.split()
        try: vals = [int(p) for p in parts]
        except ValueError: continue
        if len(vals) < 2: continue
        out[vals[0]] = (vals[1:], i)
    return out

def load_bodydef():
    out = {}
    for i, ln in enumerate(open(os.path.join(CLIENT, 'Body.def'), encoding='latin-1'), 1):
        s = ln.split('#')[0].strip()
        m = re.match(r'(\d+)\s*\{([^}]*)\}\s*(-?\d+)', s)
        if m:
            out[int(m.group(1))] = ([int(x) for x in m.group(2).split(',') if x.strip()], int(m.group(3)), i)
    return out

MOBTYPES = load_mobtypes(); BODYCONV = load_bodyconv(); BODYDEF = load_bodydef()

_uop = None
BAD = []
def uop_idx():
    global _uop
    if _uop is None:
        _uop = []
        for i in range(1, 7):
            p = os.path.join(CLIENT, f'AnimationFrame{i}.uop')
            if os.path.exists(p): _uop.append((p, read_uop_index(p)))
    return _uop

_mul = {}
def mul_idx(n):
    if n not in _mul:
        name = 'anim' if n == 1 else f'anim{n}'
        raw = open(os.path.join(CLIENT, name + '.idx'), 'rb').read()
        _mul[n] = (os.path.join(CLIENT, name + '.mul'), [struct.unpack_from('<iii', raw, k) for k in range(0, len(raw) - 11, 12)])
    return _mul[n]

def mul_layout(fileno, g):
    """(type, base index) for body slot g in anim{fileno}.mul, per ClassicUO's AnimationsLoader."""
    if fileno == 3:
        if g < 300: return 'ANIMAL', g * 65
        if g < 400: return 'MONSTER', 33000 + (g - 300) * 110
        return 'HUMAN', 35000 + (g - 400) * 175
    if fileno == 2:
        if g < 200: return 'MONSTER', g * 110
        return 'ANIMAL', 22000 + (g - 200) * 65
    if g < 200: return 'MONSTER', g * 110
    if g < 400: return 'ANIMAL', 22000 + (g - 200) * 65
    return 'HUMAN', 35000 + (g - 400) * 175

def rgb(c):
    return (((c >> 10) & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, (c & 31) * 255 // 31)

def decode_runs(data, q, pal):
    px = []
    while True:
        header, = struct.unpack_from('<I', data, q); q += 4
        if header == 0x7FFF7FFF: break
        run = header & 0xFFF
        x = (header >> 22) & 0x3FF
        if x & 0x200: x -= 0x400
        y = (header >> 12) & 0x3FF
        if y & 0x200: y -= 0x400
        for j in range(run):
            px.append((x + j, y, pal[data[q + j]] & 0x7FFF))
        q += run
    return px

def uop_action(body, action):
    key = hashlittle2(f'build/animationlegacyframe/{body:06d}/{action:02d}.bin')
    for p, idx in uop_idx():
        if key in idx:
            off, cl, dl, flag = idx[key]
            with open(p, 'rb') as fh:
                fh.seek(off); raw = fh.read(cl)
            if flag in (1, 3): raw = zlib.decompress(raw)
            return os.path.basename(p), raw
    return None, None

def uop_frames(raw):
    """Return list of 5 directions, each a list of frames (pixel lists), padded like ClassicUO."""
    frame_count, data_start = struct.unpack_from('<ii', raw, 32)
    slots = []
    p = data_start
    for i in range(frame_count):
        group, frame_id = struct.unpack_from('<Hh', raw, p)
        pix_off, = struct.unpack_from('<I', raw, p + 12)
        while len(slots) + 1 < frame_id: slots.append(None)
        slots.append(p + pix_off)
        p += 16
    while len(slots) < 50: slots.append(None)
    fpd = len(slots) // 5
    dirs = []
    for d in range(5):
        fr = []
        for fp in slots[d * fpd:(d + 1) * fpd]:
            if fp is None: continue
            try:
                pal = struct.unpack_from('<256H', raw, fp)
                fr.append(decode_runs(raw, fp + 512 + 8, pal))
            except (IndexError, struct.error):
                BAD.append(fp)  # a few UOP frames overrun their entry; skipped and counted

        dirs.append(fr)
    return dirs

def mul_frames(fileno, index):
    path, idx = mul_idx(fileno)
    if index >= len(idx): return None
    off, ln, _ = idx[index]
    if off < 0 or ln <= 0: return None
    with open(path, 'rb') as fh:
        fh.seek(off); data = fh.read(ln)
    pal = struct.unpack_from('<256H', data, 0)
    n, = struct.unpack_from('<i', data, 512)
    offs = struct.unpack_from(f'<{n}i', data, 516)
    return [decode_runs(data, 512 + o + 8, pal) for o in offs]

def resolve(body):
    """Where the client gets this body's art. Returns dict(kind, file, slot, type, note)."""
    mt = MOBTYPES.get(body, (None, ''))[0]
    # UOP first: the 7.x client prefers UOP legacy frames.
    for a in range(0, 35):
        f, raw = uop_action(body, a)
        if raw: return dict(kind='uop', file=f, slot=body, type=mt or 'MONSTER', note='')
    if body in BODYCONV:
        cols, line = BODYCONV[body]
        for k, v in enumerate(cols):
            if v is not None and v >= 0:
                fileno = k + 2
                t, base = mul_layout(fileno, v)
                return dict(kind='mul', file=f'anim{fileno}.mul', fileno=fileno, slot=v, base=base, type=t,
                            note=f'Bodyconv.def:{line}')
    t, base = mul_layout(1, body)
    path, idx = mul_idx(1)
    acts = LAYOUT[t]
    if any(base + k < len(idx) and idx[base + k][0] >= 0 and idx[base + k][1] > 0 for k in range(acts * 5)):
        return dict(kind='mul', file='anim.mul', fileno=1, slot=body, base=base, type=t, note='')
    if body in BODYDEF:
        new, hue, line = BODYDEF[body]
        return dict(kind='bodydef', target=new[0], hue=hue, note=f'Body.def:{line}', type=mt)
    return dict(kind='none', note='no art')

def frames(body, action, direction=1):
    """Frames (list of pixel lists) for one action and direction, following Body.def fallback."""
    r = resolve(body)
    if r['kind'] == 'bodydef':
        return frames(r['target'], action, direction)
    if r['kind'] == 'uop':
        _, raw = uop_action(body, action)
        if not raw: return []
        return uop_frames(raw)[direction]
    if r['kind'] == 'mul':
        fr = mul_frames(r['fileno'], r['base'] + action * 5 + direction)
        return fr or []
    return []

def actions_present(body):
    r = resolve(body)
    if r['kind'] == 'bodydef': return actions_present(r['target'])
    out = {}
    if r['kind'] == 'uop':
        for a in range(0, 100):
            _, raw = uop_action(body, a)
            if raw:
                fc, = struct.unpack_from('<i', raw, 32)
                out[a] = fc
    elif r['kind'] == 'mul':
        path, idx = mul_idx(r['fileno'])
        for a in range(LAYOUT[r['type']]):
            n = 0
            for d in range(5):
                i = r['base'] + a * 5 + d
                if i < len(idx) and idx[i][0] >= 0 and idx[i][1] > 0:
                    with open(path, 'rb') as fh:
                        fh.seek(idx[i][0] + 512); n += struct.unpack('<i', fh.read(4))[0]
            if n: out[a] = n
    return out

# --- hues (for Body.def recolors) ---
_hues = None
def hue_table():
    global _hues
    if _hues is None:
        raw = open(os.path.join(CLIENT, 'hues.mul'), 'rb').read()
        _hues = []
        p = 0
        while p + 4 <= len(raw):
            p += 4
            for _ in range(8):
                if p + 88 > len(raw): break
                cols = struct.unpack_from('<32H', raw, p); _hues.append(cols); p += 88
    return _hues

def apply_hue(c, hue):
    if not hue: return c
    h = hue_table()[(hue & 0x3FFF) - 1]
    r = (c >> 10) & 31
    return h[r] & 0x7FFF

def to_img(px, hue=0, scale=1):
    if not px: return None
    xs = [p[0] for p in px]; ys = [p[1] for p in px]
    mx, my = min(xs), min(ys)
    W, H = max(xs) - mx + 1, max(ys) - my + 1
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    put = im.putpixel
    for x, y, c in px:
        put((x - mx, y - my), rgb(apply_hue(c, hue)) + (255,))
    if scale != 1: im = im.resize((W * scale, H * scale), Image.NEAREST)
    return im

def frame_img(body, action, direction=1, index=0, scale=1):
    r = resolve(body)
    hue = r.get('hue', 0) if r['kind'] == 'bodydef' else 0
    fr = frames(body, action, direction)
    fr = [f for f in fr if f]
    if not fr: return None
    return to_img(fr[min(index, len(fr) - 1)], hue, scale)

# --- UOFiddler .vd export ---
# Layout (verified by reading the bytes of all five files): int16 6 (file tag), int16 type
# (0 = high/monster, 22 actions; 1 = low/animal, 13; 2 = people, 35), then actions*5 index entries of
# (int32 offset, int32 length, int32 extra) with offsets absolute in the file, then per entry an anim.mul
# block: 256-entry ushort palette, int32 frame count, int32 offsets (relative to the palette end), frames.
VD_TYPES = {0: 'MONSTER', 1: 'ANIMAL', 2: 'HUMAN'}
def vd_load(path):
    data = open(path, 'rb').read()
    tag, t = struct.unpack_from('<hh', data, 0)
    typ = VD_TYPES[t]; n = LAYOUT[typ] * 5
    ents = [struct.unpack_from('<iii', data, 4 + 12 * i) for i in range(n)]
    def block(i):
        off, ln, _ = ents[i]
        if off <= 0 or ln <= 0: return []
        pal = struct.unpack_from('<256H', data, off)
        cnt, = struct.unpack_from('<i', data, off + 512)
        offs = struct.unpack_from(f'<{cnt}i', data, off + 516)
        return [decode_runs(data, off + 512 + o + 8, pal) for o in offs]
    return dict(tag=tag, type=typ, entries=ents, block=block, actions=LAYOUT[typ])

def uop_style(body):
    """mobtypes flag 0x10000: the body uses the UOP-era action set (walk 22, stand 25), per ClassicUO."""
    mt = MOBTYPES.get(body)
    return bool(mt and mt[2] & 0x10000 and resolve(body)['kind'] == 'uop')

def stand_walk(body):
    r = resolve(body)
    if r['kind'] == 'bodydef': return stand_walk(r['target'])
    if uop_style(body): return 25, 22
    t = r['type'] if r['kind'] == 'mul' else (MOBTYPES.get(body, ('MONSTER',))[0] or 'MONSTER')
    return STAND.get(t, 1), WALK.get(t, 0)
