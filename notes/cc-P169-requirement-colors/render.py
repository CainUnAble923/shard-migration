"""cc-P169: render dumped gumps (GUMPJSON lines from a test log) to PNG, roughly as TazUO draws them.

Usage: render.py LOG OUTDIR PREFIX
Gump art from gumpartLegacyMUL.uop (gumppng.py's reader), label glyphs from unifont1.mul (TazUO draws server labels and
HTML in unicode font 1, cc-P57), colours from hues.mul (a label of hue N uses entry N + 1, 0-based index N; its
brightest colour). Approximations: an alpha region is black at 50% over a busy backdrop (it is see-through in the
client); HTML is plain BASEFONT COLOR and <BR> with word wrap; a hued gump image maps each pixel's brightness onto the
hue's ramp. Page 0 and page 1 only.
"""
import json, os, re, runpy, struct, sys, zlib

SCRATCH = os.path.dirname(os.path.abspath(__file__))
G = runpy.run_path(os.path.join(SCRATCH, 'gumppng.py'), run_name='lib')
DATA = r'D:\ShatteredLegacy\client-data\classic-client-7.0.117.0'

_art = {}


def art(gid):
    if gid not in _art:
        d = G['load'](G['u'], gid)
        _art[gid] = G['decode'](d) if d else (0, 0, [])
    return _art[gid]


HUES = open(os.path.join(DATA, 'hues.mul'), 'rb').read()


def hue_ramp(index):
    off = (index // 8) * 708 + 4 + (index % 8) * 88
    cols = struct.unpack_from('<32H', HUES, off)
    return [(((c >> 10) & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, (c & 31) * 255 // 31) for c in cols]


def label_rgb(h):
    return hue_ramp(h)[31] if h > 0 else (255, 255, 255)


FONT = open(os.path.join(DATA, 'unifont1.mul'), 'rb').read()


def glyph(ch):
    o = struct.unpack_from('<i', FONT, ord(ch) * 4)[0] if ord(ch) < 0x10000 else 0
    if o <= 0 or o >= len(FONT) - 4:
        return None
    xo, yo, w, h = struct.unpack_from('<bbBB', FONT, o)
    rows = []
    stride = (w - 1) // 8 + 1 if w else 0
    p = o + 4
    for y in range(h):
        bits = FONT[p:p + stride]
        rows.append([bool(bits[x // 8] & (0x80 >> (x % 8))) for x in range(w)])
        p += stride
    return xo, yo, w, h, rows


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        # A busy backdrop (stripes and blocks), so a see-through window shows it.
        self.px = [[((40 + (x // 24 % 2) * 60 + (y // 30 % 3) * 20), 70 + (x + y) // 9 % 40, 50) for x in range(w)] for y in range(h)]
        for y in range(0, h, 46):
            for x in range(0, w):
                for k in range(3):
                    if y + k < h:
                        self.px[y + k][x] = (200, 190, 120)

    def blit(self, x0, y0, gid, hue=0, tw=None, th=None):
        w, h, p = art(gid)
        if not w:
            return
        ramp = hue_ramp(hue) if hue else None
        tw, th = tw or w, th or h
        for y in range(th):
            for x in range(tw):
                c = p[y % h][x % w]
                if c[3]:
                    X, Y = x0 + x, y0 + y
                    if 0 <= X < self.w and 0 <= Y < self.h:
                        rgb = c[:3]
                        if ramp:
                            rgb = ramp[min(31, (rgb[0] + rgb[1] + rgb[2]) // 3 * 32 // 256)]
                        self.px[Y][X] = rgb

    def background(self, x, y, w, h, gid):
        tl, t, tr, l, c, r, bl, b, br = (art(gid + i) for i in range(9))
        self.blit(x + tl[0], y + t[1], gid + 4, tw=w - tl[0] - tr[0], th=h - t[1] - b[1])
        self.blit(x + tl[0], y, gid + 1, tw=w - tl[0] - tr[0], th=t[1])
        self.blit(x + tl[0], y + h - b[1], gid + 7, tw=w - bl[0] - br[0], th=b[1])
        self.blit(x, y + tl[1], gid + 3, tw=l[0], th=h - tl[1] - bl[1])
        self.blit(x + w - r[0], y + tr[1], gid + 5, tw=r[0], th=h - tr[1] - br[1])
        self.blit(x, y, gid)
        self.blit(x + w - tr[0], y, gid + 2)
        self.blit(x, y + h - bl[1], gid + 6)
        self.blit(x + w - br[0], y + h - br[1], gid + 8)

    def alpha(self, x0, y0, w, h):
        for y in range(y0, min(self.h, y0 + h)):
            for x in range(x0, min(self.w, x0 + w)):
                r, g, b = self.px[y][x]
                self.px[y][x] = (r // 2, g // 2, b // 2)

    def text(self, x0, y0, s, rgb, maxw=None):
        """One line of font 1 with the client's black border; returns its width."""
        x = x0
        for ch in s:
            if ch == ' ':
                x += 8
                continue
            gl = glyph(ch)
            if not gl:
                x += 8
                continue
            xo, yo, w, h, rows = gl
            for yy in range(h):
                for xx in range(w):
                    if rows[yy][xx]:
                        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                            X, Y = x + xo + xx + dx + 1, y0 + yo + yy + dy + 1
                            if 0 <= X < self.w and 0 <= Y < self.h and not (0 <= xx + dx < w and 0 <= yy + dy < h and rows[yy + dy][xx + dx]):
                                self.px[Y][X] = (8, 8, 8)
            for yy in range(h):
                for xx in range(w):
                    if rows[yy][xx]:
                        X, Y = x + xo + xx + 1, y0 + yo + yy + 1
                        if 0 <= X < self.w and 0 <= Y < self.h:
                            self.px[Y][X] = rgb
            x += xo + w + 1
        return x - x0

    def width(self, s):
        x = 0
        for ch in s:
            gl = glyph(ch) if ch != ' ' else None
            x += 8 if not gl else gl[0] + gl[2] + 1
        return x

    def html(self, x0, y0, w, h, src):
        # Runs of (colour, text) with <BR> as newline, wrapped word by word at w.
        rgb = (255, 255, 255)
        x, y = 0, 0
        for tok in re.split(r'(<[^>]+>)', src):
            if not tok:
                continue
            if tok.startswith('<'):
                m = re.match(r'<BASEFONT COLOR=#([0-9A-Fa-f]{6})', tok, re.I)
                if m:
                    v = int(m.group(1), 16)
                    rgb = (v >> 16, (v >> 8) & 255, v & 255)
                elif re.match(r'<BR>', tok, re.I):
                    x, y = 0, y + 18
                continue
            for word in re.split(r'( )', tok):
                if word == ' ':
                    x += 8
                    continue
                ww = self.width(word)
                if x > 0 and x + ww > w:
                    x, y = 0, y + 18
                if y + 16 <= h:
                    self.text(x0 + x, y0 + y, word, rgb)
                x += ww

    def save(self, path, scale=1):
        G['png'](path, self.w, self.h, [[c + (255,) for c in row] for row in self.px], scale=scale)


def render(entries, path):
    bg = next(e for e in entries if e['type'] == 'GumpBackground')
    W, H = bg['Width'] + 40, bg['Height'] + 40
    c = Canvas(W, H)
    page = 0
    for e in entries:
        t = e['type']
        if t == 'GumpPage':
            page = e.get('Page', 0)
            continue
        if page > 1:
            continue
        X, Y = e.get('X', 0) + 20, e.get('Y', 0) + 20
        if t == 'GumpBackground':
            c.background(X, Y, e['Width'], e['Height'], e['GumpID'])
        elif t == 'GumpAlphaRegion':
            c.alpha(X, Y, e['Width'], e['Height'])
        elif t == 'GumpImageTiled':
            c.blit(X, Y, e['GumpID'], tw=e['Width'], th=e['Height'])
        elif t == 'GumpImage':
            c.blit(X, Y, e['GumpID'], hue=e.get('Hue', 0))
        elif t == 'GumpButton':
            c.blit(X, Y, e['NormalID'])
        elif t == 'GumpLabel':
            c.text(X, Y, e['Text'], label_rgb(e['Hue']))
        elif t == 'GumpHtml':
            c.html(X, Y, e['Width'], e['Height'], e['Text'])
    c.save(path)


if __name__ == '__main__':
    log, out, prefix = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    for line in open(log, encoding='utf-8', errors='replace'):
        m = re.search(r'GUMPJSON (\S+) (\[.*\])\s*$', line)
        if m:
            p = os.path.join(out, '%s-%s.png' % (prefix, m.group(1).replace("'", '').replace('(', '').replace(')', '')))
            render(json.loads(m.group(2)), p)
            print(p)
